"""Pipeline step 1 — Telegram controller: raw update -> IncomingMessage (persona chosen by bot
token) -> pipeline. Button taps (Send/Cancel) come in here too.
No business logic and no formatting here.
"""

from telegram import Update

from assistant.domain.models import IncomingMessage


class TelegramController:
    """Turn Telegram updates into IncomingMessage."""

    def __init__(self, persona: str) -> None:
        self._persona = persona

    def parse_message(self, update: Update) -> IncomingMessage:
        """Turn a Telegram update into an IncomingMessage."""
        return IncomingMessage(
            persona=self._persona,
            sender_id=str(update.message.from_user.id),
            text=update.message.text,
            received_at=update.message.date,
        )
