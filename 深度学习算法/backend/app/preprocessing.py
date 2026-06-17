from __future__ import annotations

from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_IMAGE_BYTES
from training.dataset import get_eval_transform


async def load_valid_image(file: UploadFile) -> Image.Image:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="仅支持 jpg、jpeg、png 图片")
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="图片 MIME 类型不合法")
    content = await file.read()
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=400, detail="单张图片不能超过 5MB")
    try:
        with Image.open(BytesIO(content)) as image:
            return image.convert("RGB").copy()
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="图片无法被正常读取，请上传有效图片") from exc


def image_to_tensor(image: Image.Image, model_name: str):
    return get_eval_transform(model_name)(image).unsqueeze(0)

