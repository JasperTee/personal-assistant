"""Tests for the data contracts in domain/models.py."""

import pytest
from pydantic import ValidationError

from assistant.domain.models import ChatMessage, ToolCall, ToolResult


class TestToolCall:
    def test_rejects_wrong_types(self):
        # arguments must be a dict; a string must be rejected
        with pytest.raises(ValidationError):
            ToolCall(id="call_1", name="reminders.create", arguments="not a dict")

    def test_is_frozen(self):
        call = ToolCall(id="call_1", name="reminders.create", arguments={})
        with pytest.raises(ValidationError):
            call.name = "expenses.add"


class TestToolResult:
    def test_defaults_to_success_without_hint(self):
        result = ToolResult(tool_call_id="call_1", content="done")
        assert result.is_error is False
        assert result.hint is None


class TestChatMessage:
    def test_rejects_unknown_role(self):
        # only "user" and "assistant" are valid roles
        with pytest.raises(ValidationError):
            ChatMessage(role="system", content="hi")
