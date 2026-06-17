from __future__ import annotations

import argparse
import time
from pathlib import Path

import torch
from torch import nn, optim
from tqdm import tqdm

from training.config import DEFAULTS, backend_dir
from training.dataset import create_dataloaders
from training.models import build_model, count_parameters
from training.utils import read_json, select_device, set_seed, write_json


def run_epoch(model, loader, criterion, device, optimizer=None) -> tuple[float, float]:
    is_train = optimizer is not None
    model.train(is_train)
    total_loss = 0.0
    correct = 0
    total = 0
    for images, labels in tqdm(loader, leave=False):
        images, labels = images.to(device), labels.to(device)
        if is_train:
            optimizer.zero_grad(set_to_none=True)
        with torch.set_grad_enabled(is_train):
            logits = model(images)
            loss = criterion(logits, labels)
            if is_train:
                loss.backward()
                optimizer.step()
        total_loss += loss.item() * images.size(0)
        correct += (logits.argmax(dim=1) == labels).sum().item()
        total += images.size(0)
    return total_loss / max(total, 1), correct / max(total, 1)


def train(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    defaults = DEFAULTS[args.model]
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    model_dir = output_dir / "models"
    result_dir = output_dir / "results"
    model_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    device = select_device(args.device)
    train_loader, val_loader, _ = create_dataloaders(args.model, data_dir, args.batch_size, args.num_workers, args.seed)
    model = build_model(args.model, pretrained=args.pretrained, freeze_backbone=args.freeze_backbone).to(device)
    criterion = nn.CrossEntropyLoss()
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = optim.AdamW(trainable, lr=args.learning_rate, weight_decay=args.weight_decay) if defaults.optimizer == "adamw" else optim.Adam(trainable, lr=args.learning_rate, weight_decay=args.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    history = []
    best_acc = -1.0
    patience_left = args.early_stopping_patience
    best_path = model_dir / f"{args.model}_best.pth"
    last_path = model_dir / f"{args.model}_last.pth"

    for epoch in range(1, args.epochs + 1):
        start = time.perf_counter()
        train_loss, train_acc = run_epoch(model, train_loader, criterion, device, optimizer)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, device)
        scheduler.step()
        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_acc,
            "val_loss": val_loss,
            "val_accuracy": val_acc,
            "learning_rate": scheduler.get_last_lr()[0],
            "elapsed_time": time.perf_counter() - start,
        }
        history.append(row)
        print(row)
        if val_acc > best_acc:
            best_acc = val_acc
            patience_left = args.early_stopping_patience
            torch.save(model.state_dict(), best_path)
        else:
            patience_left -= 1
        if patience_left <= 0:
            print("Early stopping triggered.")
            break

    torch.save(model.state_dict(), last_path)
    all_history = read_json(result_dir / "training_history.json", {"cnn": [], "resnet18": [], "status": "not_trained"})
    all_history[args.model] = history
    all_history["status"] = "trained"
    write_json(result_dir / "training_history.json", all_history)
    info = read_json(model_dir / "model_info.json", {"cnn": None, "resnet18": None, "status": "not_trained"})
    info[args.model] = {
        "best_weight": str(best_path.relative_to(output_dir)),
        "last_weight": str(last_path.relative_to(output_dir)),
        "parameters": count_parameters(model),
        "best_val_accuracy": best_acc,
        "epochs_finished": len(history),
        "device": str(device),
    }
    info["status"] = "trained"
    write_json(model_dir / "model_info.json", info)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["cnn", "resnet18"], required=True)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--weight-decay", type=float, default=None)
    parser.add_argument("--data-dir", default=str(backend_dir() / "data"))
    parser.add_argument("--output-dir", default=str(backend_dir()))
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pretrained", action="store_true")
    parser.add_argument("--freeze-backbone", action="store_true")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--early-stopping-patience", type=int, default=5)
    args = parser.parse_args()
    defaults = DEFAULTS[args.model]
    args.epochs = args.epochs or defaults.epochs
    args.batch_size = args.batch_size or defaults.batch_size
    args.learning_rate = args.learning_rate or defaults.learning_rate
    args.weight_decay = args.weight_decay if args.weight_decay is not None else defaults.weight_decay
    return args


if __name__ == "__main__":
    train(parse_args())

