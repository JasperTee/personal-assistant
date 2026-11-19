"""TelegramController tests: sample Telegram JSON -> IncomingMessage with the right persona
and time; a text message from the owner is echoed back to the same chat;
a message from a stranger gets no reply.
"""

import asyncio
from datetime import UTC, datetime
from types import SimpleNamespace

from telegram import Update

from assistant.application.pipeline import Pipeline
from assistant.application.policy.access import AccessPolicy
from assistant.entrypoints.telegram.controller import TelegramController
from assistant.entrypoints.telegram.presenter import TelegramPresenter
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


def build_controller(owner_id: str = "42") -> TelegramController:
    """A controller wired with the fake LLM, like main.py does with the real one.
    The owner is the sender of SAMPLE_UPDATE unless another owner_id is given.
    """
    return TelegramController(
        persona="secretary",
        pipeline=Pipeline(FakeLLMProvider(), AccessPolicy(owner_id=owner_id)),
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

    def test_handle_message_ignores_stranger(self, fake_bot):
        """A message from someone who is not the owner gets no reply."""
        update = Update.de_json(SAMPLE_UPDATE, None)  # sent by 42
        context = SimpleNamespace(bot=fake_bot)

        asyncio.run(build_controller(owner_id="99").handle_message(update, context))

        assert fake_bot.sent_messages == []
