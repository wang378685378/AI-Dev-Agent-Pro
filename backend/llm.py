import json
import time
from openai import OpenAI
from config import settings

client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url
)

def _call_with_retry(messages: list, **kwargs):
    last_error = None
    for attempt in range(settings.max_retries):
        try:
            response = client.chat.completions.create(
                model=settings.model,
                messages=messages,
                timeout=settings.timeout,
                **kwargs
            )
            return response
        except Exception as e:
            last_error = e
            if attempt < settings.max_retries - 1:
                time.sleep(2 ** attempt)
    raise last_error

def chat(prompt: str, system: str = "You are a helpful assistant") -> str:
    response = _call_with_retry(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=settings.temperature
    )
    return response.choices[0].message.content

def chat_json(prompt: str, system: str = "You are a helpful assistant") -> dict:
    response = _call_with_retry(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=settings.temperature
    )
    content = response.choices[0].message.content
    return json.loads(content)
