import os
from typing import Optional

class Settings:
    def __init__(self):
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.openai_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL", None)
        self.model: str = os.getenv("MODEL_NAME", "gpt-4")
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
        self.timeout: int = int(os.getenv("TIMEOUT", "60"))
        self.max_fix_attempts: int = int(os.getenv("MAX_FIX_ATTEMPTS", "3"))
        
    def validate(self) -> bool:
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        return True

settings = Settings()
