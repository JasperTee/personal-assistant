"""Composition root: read config, create the concrete classes (Telegram, Claude, SQLite...), wire
them together and start the bot.
Only this file knows the concrete classes; everything else uses the interfaces in
domain/ports.py.
"""

from telegram.ext import Application, MessageHandler, filters

from assistant.channels.telegram.controller import TelegramController
from assistant.channels.telegram.presenter import TelegramPresenter
from assistant.infrastructure.config import load_settings
from assistant.infrastructure.llm.fake import FakeLLMProvider
from assistant.orchestration.pipeline import Pipeline


def main() -> None:
    """Wire the Secretary bot with the fake LLM and start polling Telegram."""
    settings = load_settings()

    pipeline = Pipeline(FakeLLMProvider())  # phase 2: ClaudeLLMProvider
    controller = TelegramController(
        persona="secretary",
        pipeline=pipeline,
        presenter=TelegramPresenter(),
    )

    application = Application.builder().token(settings.telegram_token_secretary).build()
    only_owner_text = (
        filters.TEXT & ~filters.COMMAND & filters.User(user_id=settings.owner_telegram_id)
    )
    application.add_handler(MessageHandler(only_owner_text, controller.handle_message))
    application.run_polling()  # asks Telegram for new messages until Ctrl+C


if __name__ == "__main__":
    main()
