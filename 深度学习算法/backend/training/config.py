from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

CIFAR10_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR10_STD = (0.2470, 0.2435, 0.2616)
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


@dataclass(frozen=True)
class TrainDefaults:
    epochs: int
    batch_size: int
    learning_rate: float
    weight_decay: float
    optimizer: str


DEFAULTS: dict[str, TrainDefaults] = {
    "cnn": TrainDefaults(epochs=20, batch_size=128, learning_rate=0.001, weight_decay=0.0001, optimizer="adam"),
    "resnet18": TrainDefaults(epochs=12, batch_size=32, learning_rate=0.0001, weight_decay=0.0001, optimizer="adamw"),
}


def backend_dir() -> Path:
    return Path(__file__).resolve().parents[1]

