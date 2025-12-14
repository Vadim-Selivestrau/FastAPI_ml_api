import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_process_success(monkeypatch):
    """
    Успешный ответ от LLM 200
    """

    # fake LLM
    def fake_llm(prompt: str) -> str:
        return "mocked llm response"

    monkeypatch.setattr(
        "main.response_from_llm",
        fake_llm
    )

    response = client.post(
        "/process",
        json={"text": "hello"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)


def test_process_llm_error(monkeypatch):
    """
    Ошибка LLM 502
    """

    def fake_llm(prompt: str):
        raise Exception("LLM failed")

    monkeypatch.setattr(
        "main.response_from_llm",
        fake_llm
    )

    response = client.post(
        "/process",
        json={"text": "hello"}
    )

    assert response.status_code == 502

    data = response.json()
    assert "detail" in data
