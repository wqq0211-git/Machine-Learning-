from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.model_manager import manager
from app.config import MODELS_DIR
from app.schemas import ok
from training.utils import read_json

router = APIRouter(tags=["models"])

MODEL_META = {
    "cnn": {
        "name": "自定义 CNN",
        "description": "面向 CIFAR-10 的三层卷积神经网络",
        "input_size": "3x32x32",
    },
    "resnet18": {
        "name": "ResNet-18",
        "description": "基于 torchvision ResNet-18 的迁移学习模型",
        "input_size": "3x224x224",
    },
}


@router.get("/models")
def list_models() -> dict:
    data = []
    for model_id, meta in MODEL_META.items():
        status = manager.get_status(model_id)
        data.append({
            "id": model_id,
            "name": meta["name"],
            "description": meta["description"],
            "available": status.available,
            "weights_exist": status.weights_exist,
            "parameters": status.parameters,
            "input_size": meta["input_size"],
            "message": status.error,
        })
    return ok(data)


@router.get("/model-info")
def model_info() -> dict:
    return ok(read_json(MODELS_DIR / "model_info.json", {"cnn": None, "resnet18": None, "status": "not_trained"}))


def validate_model_name(model_name: str) -> None:
    if model_name not in MODEL_META:
        raise HTTPException(status_code=400, detail="model_name 仅支持 cnn 或 resnet18")
