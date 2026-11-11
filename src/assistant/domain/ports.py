"""Interfaces (Protocol/ABC): LLMProvider, Channel, Tool, Repository.
Spec: see docs/tools.md and the Clean code section of the design document.
"""

from typing import Protocol

from assistant.domain.models import AgentContext, LLMResponse


class LLMProvider(Protocol):
    """Anything that can send a conversation to an LLM and return its answer."""

    async def generate_response(self, context: AgentContext) -> LLMResponse:
        """Send the context to the LLM and return its response."""
        ...
