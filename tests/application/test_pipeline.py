"""Tests for Pipeline: one message in, one reply out."""

import asyncio
from datetime import UTC, datetime

from assistant.application.pipeline import Pipeline
from assistant.application.policy.access import AccessPolicy
from assistant.domain.models import IncomingMessage
from assistant.infrastructure.llm.fake import FakeLLMProvider


class TestPipeline:
    def test_run_returns_llm_text_as_reply(self):
        """The reply carries the LLM's text and a run_id."""
        message = IncomingMessage(
            persona="secretary",
            sender_id="1",
            text="hello",
            received_at=datetime.now(UTC),
        )
        pipeline = Pipeline(FakeLLMProvider(), AccessPolicy("1"))

        reply = asyncio.run(pipeline.run(message))

        assert reply.text == "Echo: hello"
        assert reply.run_id != ""  # a run_id was generated
        assert reply.iteration_count == 1

    def test_run_returns_none_for_stranger(self):
        """Return None when the message is not from the owner."""
        message = IncomingMessage(
            persona="secretary",
            sender_id="2",  # owner id is 1
            text="hello",
            received_at=datetime.now(UTC),
        )
        pipeline = Pipeline(FakeLLMProvider(), AccessPolicy("1"))

        reply = asyncio.run(pipeline.run(message))

        assert reply is None
