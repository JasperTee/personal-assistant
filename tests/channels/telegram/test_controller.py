"""TelegramController tests: sample Telegram JSON -> IncomingMessage with the right persona
and time; a text message is echoed back to the same chat.
"""

import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace

from telegram import Update

from assistant.application.pipeline import Pipeline
from assistant.channels.telegram.controller import TelegramController
from assistant.channels.telegram.presenter import TelegramPresenter
from assistant.infrastructure.llm.fake import FakeLLMProvider

SAMPLE_UPDATE = {
    "update_id": 1,
    "message": {
        "message_id": 10,
        "date": 1762900000,  # Unix time, seconds since 1970 (UTC)
        "chat": {"id": 42, "type": "private"},
        "from": {"id": 42, "is_bot": False, "first_name": "Huy"},
        "text": "hello",
    },
}


def build_controller() -> TelegramController:
    """A controller wired with the fake LLM, like main.py does with the real one."""
    return TelegramController(
        persona="secretary",
        pipeline=Pipeline(FakeLLMProvider()),
        presenter=TelegramPresenter(),
    )


class TestTelegramController:
    def test_parse_message_builds_incoming_message(self):
        """Persona comes from the controller; sender, text and time from the update."""
        update = Update.de_json(SAMPLE_UPDATE, None)

        message = build_controller().parse_message(update)

        assert message.persona == "secretary"
        assert message.sender_id == "42"  # a string, not the number 42
        assert message.text == "hello"
        assert message.received_at == datetime.fromtimestamp(1762900000, UTC)

    def test_handle_message_echoes_to_same_chat(self, fake_bot):
        """A text message goes through the pipeline and the reply comes back to the chat."""
        update = Update.de_json(SAMPLE_UPDATE, None)
        context = SimpleNamespace(bot=fake_bot)  # only .bot is used

        asyncio.run(build_controller().handle_message(update, context))

        assert fake_bot.sent_messages == [{"chat_id": 42, "text": "Echo: hello"}]
