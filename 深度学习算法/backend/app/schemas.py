from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: T


def ok(data: Any, message: str = "success") -> dict[str, Any]:
    return {"code": 200, "message": message, "data": data}


class ModelStatus(BaseModel):
    id: str
    name: str
    description: str
    available: bool
    weights_exist: bool
    parameters: int | None = None
    input_size: str

