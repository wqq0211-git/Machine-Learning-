from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support, roc_auc_score
from tqdm import tqdm

from app.config import CIFAR10_CLASSES
from training.config import backend_dir
from training.dataset import create_dataloaders
from training.models import build_model, count_parameters
from training.utils import safe_torch_load, select_device, write_json


def evaluate_one(model_name: str, args: argparse.Namespace) -> dict | None:
    root = Path(args.output_dir)
    weights = root / "models" / f"{model_name}_best.pth"
    if not weights.exists():
        print(f"{model_name} 权重不存在，请先训练: {weights}")
        return None
    device = select_device(args.device)
    _, _, test_loader = create_dataloaders(model_name, args.data_dir, args.batch_size, args.num_workers, args.seed)
    model = build_model(model_name, pretrained=False).to(device)
    state = safe_torch_load(weights, device)
    model.load_state_dict(state.get("model_state_dict", state) if isinstance(state, dict) else state)
    model.eval()

    labels_all, preds_all, probs_all = [], [], []
    start_total = time.perf_counter()
    with torch.inference_mode():
        for images, labels in tqdm(test_loader, leave=False):
            images = images.to(device)
            if device.type == "cuda":
                torch.cuda.synchronize()
            logits = model(images)
            if device.type == "cuda":
                torch.cuda.synchronize()
            probs = torch.softmax(logits, dim=1).cpu().numpy()
            probs_all.append(probs)
            preds_all.extend(probs.argmax(axis=1).tolist())
            labels_all.extend(labels.numpy().tolist())
    elapsed = time.perf_counter() - start_total
    y_true = np.array(labels_all)
    y_pred = np.array(preds_all)
    y_prob = np.concatenate(probs_all, axis=0)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    per_p, per_r, per_f, support = precision_recall_fscore_support(y_true, y_pred, average=None, zero_division=0)
    try:
        auc = roc_auc_score(y_true, y_prob, multi_class="ovr", average="macro")
    except ValueError:
        auc = None
    result = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
        "macro_auc": auc,
        "parameters": count_parameters(model),
        "avg_inference_time_ms": elapsed * 1000 / max(len(y_true), 1),
        "test_samples": int(len(y_true)),
    }
    class_rows = []
    for i, cls in enumerate(CIFAR10_CLASSES):
        class_rows.append({
            "index": i,
            "english": cls["english"],
            "chinese": cls["chinese"],
            "precision": float(per_p[i]),
            "recall": float(per_r[i]),
            "f1": float(per_f[i]),
            "support": int(support[i]),
        })
    write_json(root / "results" / f"confusion_matrix_{model_name}.json", {
        "model": model_name,
        "labels": CIFAR10_CLASSES,
        "matrix": confusion_matrix(y_true, y_pred).tolist(),
        "status": "evaluated",
    })
    return {"summary": result, "class_metrics": class_rows}


def main(args: argparse.Namespace) -> None:
    targets = ["cnn", "resnet18"] if args.model == "all" else [args.model]
    root = Path(args.output_dir)
    metrics = {"cnn": None, "resnet18": None, "status": "not_evaluated"}
    class_metrics = {"cnn": None, "resnet18": None, "status": "not_evaluated"}
    for target in targets:
        result = evaluate_one(target, args)
        if result:
            metrics[target] = result["summary"]
            class_metrics[target] = result["class_metrics"]
    metrics["status"] = "evaluated" if any(metrics[m] for m in ("cnn", "resnet18")) else "not_evaluated"
    class_metrics["status"] = metrics["status"]
    write_json(root / "results" / "metrics.json", metrics)
    write_json(root / "results" / "class_metrics.json", class_metrics)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["cnn", "resnet18", "all"], required=True)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--data-dir", default=str(backend_dir() / "data"))
    parser.add_argument("--output-dir", default=str(backend_dir()))
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto")
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())

