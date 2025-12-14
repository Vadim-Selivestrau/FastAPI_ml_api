import os
from huggingface_hub import InferenceClient
from loger import logger


class ModelError(Exception):
    """Ошибка при обращении к модели"""
    pass


Model = "tabularisai/multilingual-sentiment-analysis"

client = InferenceClient(
    provider="hf-inference",
    api_key=API_TOKEN,
)


def response_from_model(request: str) -> list[dict]:
    try:
        logger.info("🤓Sending request to model (prompt_hash=%s)", request)
        
        result = client.text_classification(
            request,
            model=Model,
        )

        if not result:
            raise ModelError("empty result from Model")

        normalized = []
        for item in result:
            normalized.append(
                {
                    "label": item.label,
                    "probability": float(item.score),
                }
            )
        return normalized

    except ModelError:
        raise

    except Exception:

        logger.exception("Model Error")
        raise ModelError("request error")



