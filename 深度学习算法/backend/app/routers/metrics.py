from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config import RESULTS_DIR
from app.routers.models import validate_model_name
from app.schemas import ok
from training.utils import read_json

router = APIRouter(tags=["metrics"])


def result_file(name: str, default):
    return read_json(RESULTS_DIR / name, default)


@router.get("/metrics")
def metrics() -> dict:
    return ok(result_file("metrics.json", {"cnn": None, "resnet18": None, "status": "not_evaluated"}))


@router.get("/training-history")
def training_history() -> dict:
    return ok(result_file("training_history.json", {"cnn": [], "resnet18": [], "status": "not_trained"}))


@router.get("/confusion-matrix/{model_name}")
def confusion_matrix(model_name: str) -> dict:
    validate_model_name(model_name)
    return ok(result_file(f"confusion_matrix_{model_name}.json", {"model": model_name, "matrix": None, "status": "not_evaluated"}))


@router.get("/class-metrics/{model_name}")
def class_metrics(model_name: str) -> dict:
    validate_model_name(model_name)
    data = result_file("class_metrics.json", {"cnn": None, "resnet18": None, "status": "not_evaluated"})
    if model_name not in data:
        raise HTTPException(status_code=404, detail="未找到该模型的类别指标")
    return ok(data[model_name])

