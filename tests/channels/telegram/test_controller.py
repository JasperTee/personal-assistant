"""TelegramController tests: sample Telegram JSON -> IncomingMessage with the right persona
and time.
"""

from datetime import UTC, datetime

from telegram import Update

from assistant.channels.telegram.controller import TelegramController

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


class TestTelegramController:
    def test_parse_message_builds_incoming_message(self):
        """Persona comes from the controller; sender, text and time from the update."""
        update = Update.de_json(SAMPLE_UPDATE, None)
        controller = TelegramController(persona="secretary")

        message = controller.parse_message(update)

        assert message.persona == "secretary"
        assert message.sender_id == "42"  # a string, not the number 42
        assert message.text == "hello"
        assert message.received_at == datetime.fromtimestamp(1762900000, UTC)
