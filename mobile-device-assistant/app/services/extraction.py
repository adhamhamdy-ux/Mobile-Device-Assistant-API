import json 
import os 
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import ValidationError
from app.schema.device import Device
from app.prompts.templates import SYSTEM_PROMPT, USER_MESSAGE, RETRY_MESSAGE

load_dotenv()
client = OpenAI(api_key=os.getenv("api_key"))
MODEL_NAME = os.getenv("model_name", "gpt-4o-mini")
MAX_RETRIES = 2

class ExtractionError(Exception):
    """Raised when the LLM output can't be validated after all retries."""

def extract_device(text:str)->Device:
    message = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_MESSAGE.format(input_text=text)}
    ]    
    for attempt in range(MAX_RETRIES +1):
        response = client.chat.completions.create(model=MODEL_NAME,messages=message,response_format={"type": "json_object"},temperature=0)

        raw = response.choices[0].message.content

        try:
            data = json.loads(raw)
            return Device.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = str(e)
            message.append({"role": "assistant", "content": raw})
            message.append({"role": "user", "content": RETRY_MESSAGE.format(error=last_error)})

    raise ExtractionError(f"Validation failed after {MAX_RETRIES} retries: {last_error}")
