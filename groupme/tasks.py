import logging

from website import celery_app as app

from .bots import ParseError, parse_command, registry

logger = logging.getLogger(__name__)


@app.task
def handle_bot_message(**data):

    try:
        command, *args = parse_command(data["text"])
    except ParseError as e:
        logger.info(
            f"No command parsed from message. Data: {data} | ERROR: {e}",
            extra={"data": data, "error": e},
        )
        return

    try:
        Bot = registry[command]
    except KeyError:
        logger.info(
            f"Unknown command `{command}`",
            extra={
                "command": command,
                "args": args,
                "data": data,
            },
        )
        return

    bot = Bot(*args, **data)
    bot.execute()
