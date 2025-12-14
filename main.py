from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm import response_from_llm, LLMError
from cache import get_from_cache, set_to_cache
from loger import logger

app = FastAPI()


class PromptIn(BaseModel):
    text: str


class PromptOut(BaseModel):
    result: str


@app.post("/process", response_model=PromptOut)
async def process_prompt(payload: PromptIn):
    try:
        user_request = payload.text
        logger.info("⬇Incoming request")

        user_result = get_from_cache(user_request)
        if user_result is None:
            llm_result = response_from_llm(user_request)
            set_to_cache(user_request, llm_result)
            return PromptOut(result=llm_result)
        else:
            return PromptOut(result = user_result)

    except LLMError:
        raise HTTPException(
            status_code=502,
            detail=HTTPException
        )
