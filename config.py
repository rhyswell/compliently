import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env if present
load_dotenv()


class Config:
    """
    Central configuration for Compliantly.
    Uses GPT-5.2 with message-based API.
    No temperature parameter.
    """

    # OpenAI
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = "gpt-5.2"

    # Completion control
    MAX_COMPLETION_TOKENS_GUIDELINES: int = 800
    MAX_COMPLETION_TOKENS_SEMANTIC: int = 1000

    # Scoring weights
    DETERMINISTIC_WEIGHT: float = 0.4
    SEMANTIC_WEIGHT: float = 0.6

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found. Set it as an environment variable."
            )

    @staticmethod
    def get_client() -> OpenAI:
        Config.validate()
        return OpenAI(api_key=Config.OPENAI_API_KEY)
