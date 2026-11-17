"""Fake LLMProvider for tests: echoes the message back, costs no API money."""

from assistant.domain.models import AgentContext, LLMResponse


class FakeLLMProvider:
    """Echoes the user's message back."""

    async def generate_response(self, context: AgentContext) -> LLMResponse:
        """Return "Echo: <message text>" as the reply."""
        return LLMResponse(
            text=f"Echo: {context.message.text}",
            input_tokens=0,
            output_tokens=0,
        )
