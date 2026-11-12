"""Tests for load_settings: values come from the environment; missing ones fail clearly."""

import pytest

from assistant.infrastructure.config import load_settings


class TestLoadSettings:
    def test_reads_values_from_environment(self, monkeypatch):
        """Environment variables become typed settings."""
        monkeypatch.setenv("TELEGRAM_TOKEN_SECRETARY", "test-token")
        monkeypatch.setenv("OWNER_TELEGRAM_ID", "42")

        settings = load_settings()

        assert settings.telegram_token_secretary == "test-token"
        assert settings.owner_telegram_id == 42  # an int, not "42"

    def test_missing_value_raises(self, monkeypatch):
        """A missing token stops start-up with a clear message."""
        monkeypatch.setattr("assistant.infrastructure.config.load_dotenv", lambda: None)
        monkeypatch.delenv("TELEGRAM_TOKEN_SECRETARY", raising=False)
        monkeypatch.setenv("OWNER_TELEGRAM_ID", "42")

        with pytest.raises(RuntimeError, match="TELEGRAM_TOKEN_SECRETARY"):
            load_settings()
