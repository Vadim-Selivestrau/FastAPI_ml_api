from google import genai
import os
from loger import logger

client = genai.Client(api_key=TOKEN_KEY)
Model = "gemini-2.5-flash"

class LLMError(Exception):
    """Ошибка при обращении к LLM"""
    pass

def response_from_llm(request: str) -> str:
    try:    
        logger.info("🤓Sending request to LLM (prompt_hash=%s)", request)

        response = client.models.generate_content(
            model= Model,
            contents= request,
        )
        
        if not response.text:
            raise LLMError("Empty response from LLM")
        return response.text

    except Exception as e:
        logger.exception("LLM error")

        raise LLMError("LLM request error")
