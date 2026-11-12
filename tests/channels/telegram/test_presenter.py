"""TelegramPresenter tests: the reply text is sent to the right chat.
Later: long replies are split; pending actions get Send/Cancel buttons.
"""

import asyncio

from assistant.channels.telegram.presenter import TelegramPresenter
from assistant.domain.models import AgentReply


class TestTelegramPresenter:
    def test_send_reply_sends_text_to_chat(self, fake_bot):
        """The reply text goes to the given chat, once."""
        reply = AgentReply(run_id="run_1", text="Echo: hello", iteration_count=1)

        asyncio.run(TelegramPresenter().send_reply(fake_bot, chat_id=42, reply=reply))

        assert fake_bot.sent_messages == [{"chat_id": 42, "text": "Echo: hello"}]
