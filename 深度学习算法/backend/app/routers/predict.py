from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import MAX_BATCH_FILES
from app.model_manager import manager
from app.prediction import predict_image
from app.preprocessing import load_valid_image
from app.routers.models import validate_model_name
from app.schemas import ok

router = APIRouter(tags=["predict"])


def ensure_available(model_name: str) -> None:
    status = manager.get_status(model_name)
    if not status.available:
        raise HTTPException(status_code=503, detail=status.error or "模型不可用，请先训练并放置权重文件")


@router.post("/predict")
async def predict(file: UploadFile = File(...), model_name: str = Form(...)) -> dict:
    validate_model_name(model_name)
    ensure_available(model_name)
    image = await load_valid_image(file)
    return ok(predict_image(image, model_name))


@router.post("/predict/compare")
async def predict_compare(file: UploadFile = File(...)) -> dict:
    image = await load_valid_image(file)
    result: dict = {}
    for name in ("cnn", "resnet18"):
        ensure_available(name)
        result[name] = predict_image(image, name)
    result["same_prediction"] = result["cnn"]["class_index"] == result["resnet18"]["class_index"]
    result["confidence_gap"] = abs(result["cnn"]["confidence"] - result["resnet18"]["confidence"])
    result["inference_time_ms"] = {
        "cnn": result["cnn"]["inference_time_ms"],
        "resnet18": result["resnet18"]["inference_time_ms"],
    }
    return ok(result)


@router.post("/predict/batch")
async def predict_batch(files: list[UploadFile] = File(...), model_name: str = Form(...)) -> dict:
    if len(files) > MAX_BATCH_FILES:
        raise HTTPException(status_code=400, detail="批量预测最多支持 20 张图片")
    if model_name not in {"cnn", "resnet18", "both"}:
        raise HTTPException(status_code=400, detail="model_name 仅支持 cnn、resnet18 或 both")
    target_models = ["cnn", "resnet18"] if model_name == "both" else [model_name]
    for name in target_models:
        ensure_available(name)

    rows = []
    success_count = 0
    failed_count = 0
    for index, file in enumerate(files, start=1):
        row = {"index": index, "filename": file.filename, "results": {}, "error": None}
        try:
            image = await load_valid_image(file)
            for name in target_models:
                row["results"][name] = predict_image(image, name)
            if len(target_models) == 2:
                row["same_prediction"] = row["results"]["cnn"]["class_index"] == row["results"]["resnet18"]["class_index"]
            success_count += 1
        except HTTPException as exc:
            row["error"] = exc.detail
            failed_count += 1
        rows.append(row)
    return ok({"success_count": success_count, "failed_count": failed_count, "items": rows})

