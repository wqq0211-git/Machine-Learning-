from __future__ import annotations

import torch
from PIL import Image

from app.config import CIFAR10_CLASSES
from app.model_manager import manager
from app.preprocessing import image_to_tensor


def predict_image(image: Image.Image, model_name: str) -> dict:
    tensor = image_to_tensor(image, model_name)
    logits, elapsed_ms = manager.predict_logits(model_name, tensor)
    probabilities = torch.softmax(logits, dim=1).squeeze(0)
    top_prob, top_idx = torch.max(probabilities, dim=0)
    top3_prob, top3_idx = torch.topk(probabilities, k=3)

    def item(index: int, probability: float) -> dict:
        cls = CIFAR10_CLASSES[index]
        return {
            "index": index,
            "english": cls["english"],
            "chinese": cls["chinese"],
            "probability": probability,
        }

    return {
        "model_name": model_name,
        "class_english": CIFAR10_CLASSES[int(top_idx)]["english"],
        "class_chinese": CIFAR10_CLASSES[int(top_idx)]["chinese"],
        "class_index": int(top_idx),
        "confidence": float(top_prob),
        "inference_time_ms": elapsed_ms,
        "top3": [item(int(i), float(p)) for p, i in zip(top3_prob, top3_idx, strict=True)],
        "probabilities": [item(i, float(probabilities[i])) for i in range(len(CIFAR10_CLASSES))],
    }

