"""Access tests: strangers (outside the allowlist) are blocked; each persona gets only its tools."""

from datetime import UTC, datetime

from assistant.application.policy.access import AccessPolicy
from assistant.domain.models import IncomingMessage


class TestAccessPolicy:
    def test_can_access_allows_owner(self):
        """A message from the owner is allowed."""
        # Arrange: a policy for owner "42" and a message from "42"
        policy = AccessPolicy(owner_id="42")
        message = IncomingMessage(
            persona="secretary",
            sender_id="42",
            text="hello",
            received_at=datetime.now(UTC),
        )

        # Act: ask the policy
        is_allowed = policy.can_access(message)

        # Assert: the owner gets in
        assert is_allowed is True

    def test_can_access_blocks_stranger(self):
        """A message from a stranger should be rejected."""
        # Arrange: a policy for owner "1" but the message from "2"
        policy = AccessPolicy("1")
        message = IncomingMessage(
            persona="secretary", sender_id="2", text="hello2", received_at=datetime.now(UTC)
        )

        # Act: ask the policy
        is_allowed = policy.can_access(message)

        # Assert: be Rejected
        assert is_allowed is False
