"""Data contracts (Pydantic, immutable):
IncomingMessage (with persona), AgentContext, ToolCall, ToolResult (with hint),
AgentReply, RunLog, RiskLevel.
Must not import any other folder of the project.
"""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class RiskLevel(StrEnum):
    """How dangerous an action the bot wants to take is."""

    READ = "READ"  # read only
    WRITE_SELF = "WRITE_SELF"  # write the owner's data
    EXTERNAL = "EXTERNAL"  # send something outside -> need approval
    FORBIDDEN = "FORBIDDEN"  # never allowed


class IncomingMessage(BaseModel):
    """A message that has just arrived from a channel."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    persona: str  # which bot received it
    sender_id: str  # who sent it
    text: str  # what they wrote
    received_at: datetime  # when it arrived


class ToolCall(BaseModel):
    """A request to call a tool."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    id: str  # given by the LLM; ToolResult.tool_call_id points back to it
    name: str  # tool name, e.g. "reminders.create"
    arguments: dict  # tool parameters, e.g. {"content": "gym", "remind_at": "..."}


class ToolResult(BaseModel):
    """The result of a tool call."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    tool_call_id: str  # which ToolCall this answers
    content: str  # the result or error message
    is_error: bool = False  # True if the tool call failed
    hint: str | None = None  # optional hint for the agent to understand next steps, results


class AgentReply(BaseModel):
    """A message that the agent wants to send back to the user."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    run_id: str  # which run this reply belongs to
    text: str  # what the agent wants to say
    tool_results: tuple[ToolResult, ...] = ()  # results of the tools the agent called
    iteration_count: int  # how many iterations of reasoning the agent did


class RunLog(BaseModel):
    """A log of a single run of the agent."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    run_id: str  # which run this log belongs to
    persona: str  # which bot this log belongs to
    route: str  # which route this log belongs to
    tool_names: tuple[str, ...] = ()  # which tools were called during this run
    input_tokens: int = 0  # how many tokens were used for the inputs
    output_tokens: int = 0  # how many tokens were used for the outputs
    cost_usd: Decimal = Decimal("0")  # how much this run cost in USD
    duration_ms: int  # how long this run took in milliseconds
    error: str | None = None  # optional error message if the run failed


class ChatRole(StrEnum):
    """Role of a message in a chat conversation."""

    USER = "user"  # the owner
    ASSISTANT = "assistant"  # the bot


class ChatMessage(BaseModel):
    """One message in the chat history"""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    role: ChatRole  # who sent the message
    content: str  # what they wrote


class AgentContext(BaseModel):
    """Everything the agent needs to know about the current conversation and its state."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    run_id: str  # which run this context belongs to
    message: IncomingMessage  # the incoming message that triggered this context
    system_prompt: str  # the system prompt that defines the agent's behavior
    history: tuple[ChatMessage, ...] = ()  # the chat history leading up to this message
    tool_names: tuple[str, ...] = ()  # which tools are available to the agent


class LLMResponse(BaseModel):
    """What the LLM returned for one call."""

    model_config = ConfigDict(frozen=True)  # cannot be changed after creation

    text: str = ""  # reply text; empty when the LLM only calls tools
    tool_calls: tuple[ToolCall, ...] = ()  # which tools the LLM wants to call
    input_tokens: int  # how many tokens were used for the inputs
    output_tokens: int  # how many tokens were used for the outputs
