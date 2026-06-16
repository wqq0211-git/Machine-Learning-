from __future__ import annotations

from fastapi import APIRouter

from app.config import CIFAR10_CLASSES, RESULTS_DIR
from app.schemas import ok
from training.utils import read_json

router = APIRouter(tags=["dataset"])


@router.get("/dataset")
def dataset_info() -> dict:
    default = {
        "name": "CIFAR-10",
        "source": "torchvision.datasets.CIFAR10",
        "total_samples": 60000,
        "train_samples": 50000,
        "validation_samples": 5000,
        "test_samples": 10000,
        "image_size": "32x32",
        "channels": 3,
        "classes": CIFAR10_CLASSES,
        "class_distribution": [{"english": item["english"], "chinese": item["chinese"], "count": 6000} for item in CIFAR10_CLASSES],
        "preprocessing": {
            "cnn": "32x32 CIFAR-10 mean/std normalization",
            "resnet18": "224x224 ImageNet mean/std normalization",
        },
    }
    return ok(read_json(RESULTS_DIR / "dataset_info.json", default))

