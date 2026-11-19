"""Load config/ (settings.yaml, personas/*.yaml, prompts/*.md) and .env into typed settings.
Read-only at runtime.
"""

import os

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    """Values the app needs at start-up; secrets come from .env."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    telegram_token_secretary: str  # bot token from BotFather
    owner_telegram_id: int  # only this Telegram user may talk to the bot


def load_settings() -> Settings:
    """Read .env into Settings; raise if a required value is missing."""
    load_dotenv()  # copies .env into os.environ; real environment variables win
    missing_names = [
        name for name in ("TELEGRAM_TOKEN_SECRETARY", "OWNER_TELEGRAM_ID") if not os.getenv(name)
    ]
    if missing_names:
        raise RuntimeError(f"Missing in .env: {', '.join(missing_names)}")
    return Settings(
        telegram_token_secretary=os.environ["TELEGRAM_TOKEN_SECRETARY"],
        owner_telegram_id=int(os.environ["OWNER_TELEGRAM_ID"]),
    )
