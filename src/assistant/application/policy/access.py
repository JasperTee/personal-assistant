"""Pipeline step 2 — allowlist, roles, persona -> list of allowed tools; rate limiting.
The monthly budget check lives in budget.py.
"""

from assistant.domain.models import IncomingMessage


class AccessPolicy:
    """Decide who may use the bots."""

    def __init__(self, owner_id: str) -> None:
        self._owner_id = owner_id

    def can_access(self, message: IncomingMessage) -> bool:
        """Return True if the message is from the owner."""
        return self._owner_id == message.sender_id
