from __future__ import annotations

from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[1]
MODELS_DIR: Final[Path] = BASE_DIR / "models"
RESULTS_DIR: Final[Path] = BASE_DIR / "results"
DATA_DIR: Final[Path] = BASE_DIR / "data"

MODEL_FILES: Final[dict[str, Path]] = {
    "cnn": MODELS_DIR / "cnn_best.pth",
    "resnet18": MODELS_DIR / "resnet18_best.pth",
}

CIFAR10_CLASSES: Final[list[dict[str, str | int]]] = [
    {"index": 0, "english": "airplane", "chinese": "飞机"},
    {"index": 1, "english": "automobile", "chinese": "汽车"},
    {"index": 2, "english": "bird", "chinese": "鸟"},
    {"index": 3, "english": "cat", "chinese": "猫"},
    {"index": 4, "english": "deer", "chinese": "鹿"},
    {"index": 5, "english": "dog", "chinese": "狗"},
    {"index": 6, "english": "frog", "chinese": "青蛙"},
    {"index": 7, "english": "horse", "chinese": "马"},
    {"index": 8, "english": "ship", "chinese": "船"},
    {"index": 9, "english": "truck", "chinese": "卡车"},
]

MAX_IMAGE_BYTES: Final[int] = 5 * 1024 * 1024
MAX_BATCH_FILES: Final[int] = 20
ALLOWED_EXTENSIONS: Final[set[str]] = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES: Final[set[str]] = {"image/jpeg", "image/png"}

