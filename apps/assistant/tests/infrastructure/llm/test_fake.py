"""Tests for FakeLLMProvider."""

import asyncio
from datetime import UTC, datetime

from assistant.domain.models import AgentContext, IncomingMessage
from assistant.infrastructure.llm.fake import FakeLLMProvider


class TestFakeLLMProvider:
    def test_echoes_message(self):
        """The fake LLM should echo the message text back."""
        message = IncomingMessage(
            persona="secretary",
            sender_id="1",
            text="Hello, world!",
            received_at=datetime.now(UTC),
        )
        context = AgentContext(run_id="run_1", message=message, system_prompt="")
        response = asyncio.run(FakeLLMProvider().generate_response(context))

        assert response.text == "Echo: Hello, world!"
        assert response.tool_calls == ()
