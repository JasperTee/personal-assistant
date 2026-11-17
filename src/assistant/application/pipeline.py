"""Run the 7 steps in order for one IncomingMessage; generate a run_id that follows it all the way
through.
"""

from uuid import uuid4

from assistant.application.policy.access import AccessPolicy
from assistant.domain.models import AgentContext, AgentReply, IncomingMessage
from assistant.domain.ports import LLMProvider


class Pipeline:
    """Run one message through the steps and return the reply."""

    def __init__(self, llm_provider: LLMProvider, access_policy: AccessPolicy) -> None:
        self._llm_provider = llm_provider
        self._access_policy = access_policy

    async def run(self, message: IncomingMessage) -> AgentReply | None:
        """Send the message to the LLM and return the reply.
        Return None if the message is not from the owner.
        """
        if not self._access_policy.can_access(message):
            return None
        run_id = str(uuid4())
        context = AgentContext(run_id=run_id, message=message, system_prompt="")
        response = await self._llm_provider.generate_response(context)
        return AgentReply(
            run_id=run_id,
            text=response.text,
            iteration_count=1,  # no agent loop yet: one LLM call
        )
