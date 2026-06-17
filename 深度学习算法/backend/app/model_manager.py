from __future__ import annotations

import time
from dataclasses import dataclass

import torch
from torch import nn

from app.config import MODEL_FILES
from training.models import build_model, count_parameters
from training.utils import safe_torch_load, select_device


@dataclass
class LoadedModel:
    model: nn.Module | None
    weights_exist: bool
    available: bool
    parameters: int
    error: str | None = None


class ModelManager:
    _instance: "ModelManager | None" = None

    def __new__(cls) -> "ModelManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.device = select_device("auto")
            cls._instance.models = {}
            cls._instance.load_all()
        return cls._instance

    def load_all(self) -> None:
        for name in ("cnn", "resnet18"):
            self.models[name] = self._load_model(name)

    def _load_model(self, model_name: str) -> LoadedModel:
        base_model = build_model(model_name, pretrained=False)
        parameters = count_parameters(base_model)
        weights_path = MODEL_FILES[model_name]
        if not weights_path.exists():
            return LoadedModel(None, False, False, parameters, "模型权重不存在，请先训练模型")
        try:
            state = safe_torch_load(weights_path, self.device)
            state_dict = state.get("model_state_dict", state) if isinstance(state, dict) else state
            base_model.load_state_dict(state_dict)
            base_model.to(self.device)
            base_model.eval()
            return LoadedModel(base_model, True, True, parameters)
        except Exception as exc:
            return LoadedModel(None, True, False, parameters, f"模型加载失败: {exc}")

    def get_status(self, model_name: str) -> LoadedModel:
        return self.models[model_name]

    def predict_logits(self, model_name: str, tensor: torch.Tensor) -> tuple[torch.Tensor, float]:
        loaded = self.models[model_name]
        if loaded.model is None:
            raise RuntimeError(loaded.error or "模型不可用")
        tensor = tensor.to(self.device)
        if self.device.type == "cuda":
            torch.cuda.synchronize()
        start = time.perf_counter()
        with torch.inference_mode():
            logits = loaded.model(tensor)
        if self.device.type == "cuda":
            torch.cuda.synchronize()
        elapsed_ms = (time.perf_counter() - start) * 1000
        return logits.cpu(), elapsed_ms


manager = ModelManager()

