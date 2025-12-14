import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app
from model import ModelError

client = TestClient(app)

def test_process_prompt_success():
    test_text = "test text"
    fake_predictions = [
        {"label": "positive", "probability": 0.95},
        {"label": "negative", "probability": 0.05},
    ]

    with patch("main.get_from_cache", return_value=None), \
         patch("main.response_from_model", return_value=fake_predictions), \
         patch("main.set_to_cache"):

        response = client.post("/process", json={"text": test_text})
        assert response.status_code == 200

        data = response.json()
        assert data["text"] == test_text
        assert data["predictions"] == fake_predictions
        assert data["model"] == "tabularisai/multilingual-sentiment-analysis"
        assert data["cached"] is False


def test_process_prompt_model_error():
    test_text = "error text"

    with patch("main.get_from_cache", return_value=None), \
         patch("main.response_from_model", side_effect=ModelError("Model failed")):

        response = client.post("/process", json={"text": test_text})
        assert response.status_code == 502
        assert response.json()["detail"] == "Model service unavailable"
