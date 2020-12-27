import logging

from celery.schedules import crontab
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


daily_morning = crontab(minute=0, hour=8)


@app.task
def morning_digest():
    """
    Daily morning routine that checks for upcoming birthdays and countdowns and
    updates the family on what to expect for the day.
    """
    logger.info("morning_digest() run!")


app.conf.beat_schedule = {
    "morning_digest": {
        "task": "groupme.tasks.morning_digest",
        "schedule": daily_morning,
    },
}
app.conf.timezone = "America/Detroit"
