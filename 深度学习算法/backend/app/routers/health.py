from __future__ import annotations

import platform

import torch
from fastapi import APIRouter

from app.model_manager import manager
from app.schemas import ok

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return ok({
        "status": "running",
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "device": str(manager.device),
        "cuda_available": torch.cuda.is_available(),
        "cnn_loaded": manager.get_status("cnn").available,
        "resnet18_loaded": manager.get_status("resnet18").available,
    })

