from fastapi.testclient import TestClient
from PIL import Image

from app.preprocessing import image_to_tensor
from main import app


def test_invalid_model_name_rejected():
    response = TestClient(app).post(
        "/api/predict",
        data={"model_name": "bad"},
        files={"file": ("x.txt", b"abc", "text/plain")},
    )
    assert response.status_code == 400


def test_non_image_rejected_for_existing_model_name():
    response = TestClient(app).post(
        "/api/predict",
        data={"model_name": "cnn"},
        files={"file": ("x.txt", b"abc", "text/plain")},
    )
    assert response.status_code in {400, 503}


def test_uploaded_image_preprocessing_matches_model_input_sizes():
    image = Image.new("RGB", (640, 360), color="white")

    cnn_tensor = image_to_tensor(image, "cnn")
    resnet_tensor = image_to_tensor(image, "resnet18")

    assert tuple(cnn_tensor.shape) == (1, 3, 32, 32)
    assert tuple(resnet_tensor.shape) == (1, 3, 224, 224)
