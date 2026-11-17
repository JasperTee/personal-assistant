"""Shared pytest fixtures for every test folder (e.g. a FakeLLMProvider, sample messages).
pytest loads this file automatically; fixtures here need no import.
"""

import pytest


class FakeBot:
    """Stands in for telegram.Bot: records messages instead of calling Telegram."""

    def __init__(self) -> None:
        self.sent_messages: list[dict] = []

    async def send_message(self, chat_id: int, text: str) -> None:
        """Remember what would have been sent."""
        self.sent_messages.append({"chat_id": chat_id, "text": text})


@pytest.fixture
def fake_bot() -> FakeBot:
    """A new FakeBot for each test."""
    return FakeBot()
