"""Pipeline step 6 — Telegram presenter: AgentReply -> Telegram messages.
Formats text, splits long messages, adds Send/Cancel buttons for pending actions.
No business logic here.
"""

from telegram import Bot

from assistant.domain.models import AgentReply


class TelegramPresenter:
    """Send an AgentReply back to a Telegram chat."""

    async def send_reply(self, bot: Bot, chat_id: int, reply: AgentReply) -> None:
        """Send the reply text to the chat."""
        await bot.send_message(chat_id=chat_id, text=reply.text)
