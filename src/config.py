import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    SYNO_URL: str = os.getenv("SYNO_URL", "")
    SYNO_USER: str = os.getenv("SYNO_USER", "")
    SYNO_PASSWORD: str = os.getenv("SYNO_PASSWORD", "")
    DOWNLOAD_PATH: str = os.getenv("DOWNLOAD_PATH", "Downloads")

    @classmethod
    def validate(cls) -> Optional[str]:
        """Validates that all required configuration variables are set."""
        if not cls.SYNO_URL:
            return "SYNO_URL is not set in environment or .env file."
        if not cls.SYNO_USER:
            return "SYNO_USER is not set in environment or .env file."
        if not cls.SYNO_PASSWORD:
            return "SYNO_PASSWORD is not set in environment or .env file."
        return None
