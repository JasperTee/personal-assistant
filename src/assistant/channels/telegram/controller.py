"""Pipeline step 1 — Telegram controller: raw update -> IncomingMessage (persona chosen by bot
token) -> pipeline. Button taps (Send/Cancel) come in here too.
No business logic and no formatting here.
"""

from telegram import Update
from telegram.ext import ContextTypes

from assistant.application.pipeline import Pipeline
from assistant.channels.telegram.presenter import TelegramPresenter
from assistant.domain.models import IncomingMessage


class TelegramController:
    """Turn Telegram updates into IncomingMessage, run the pipeline and send the reply."""

    def __init__(self, persona: str, pipeline: Pipeline, presenter: TelegramPresenter) -> None:
        self._persona = persona
        self._pipeline = pipeline
        self._presenter = presenter

    def parse_message(self, update: Update) -> IncomingMessage:
        """Turn a Telegram update into an IncomingMessage."""
        return IncomingMessage(
            persona=self._persona,
            sender_id=str(update.message.from_user.id),
            text=update.message.text,
            received_at=update.message.date,
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Called by python-telegram-bot for each text message: parse, run, reply."""
        message = self.parse_message(update)
        reply = await self._pipeline.run(message)
        await self._presenter.send_reply(context.bot, update.effective_chat.id, reply)
