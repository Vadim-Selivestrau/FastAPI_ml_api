from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from model import response_from_model, ModelError, Model
from typing import List

from cache import get_from_cache, set_to_cache
from loger import logger

app = FastAPI()

class UserText(BaseModel):
    text: str = Field(..., description="User input text")

class Prediction(BaseModel):
    label: str = Field(..., description="Class label")
    probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Class probability",
    )

class ClassificationResponse(BaseModel):
    text: str
    predictions: List[Prediction]
    model: str
    cached: bool



@app.post("/process", response_model=ClassificationResponse)
async def process_prompt(payload: UserText):
    logger.info("⬇ Incoming request")

    text = payload.text

    try:
        cached_result = get_from_cache(text)

        if cached_result is None:
            logger.info("Cache miss")
            predictions = response_from_model(text)
            set_to_cache(text, predictions)
            cached = False
        else:
            logger.info("Cache hit")
            predictions = cached_result
            cached = True

        return ClassificationResponse(
            text=text,
            predictions=predictions,
            model=Model,
            cached=cached,
        )

    except ModelError as e:
        logger.error("Model error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Model service unavailable",
        )

    except Exception:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=501,
            detail="Internal server error",
        )
