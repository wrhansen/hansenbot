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
def countdown_check():
    logger.info("Countdown Check Run!")


@app.task
def birthday_check():
    pass


app.conf.beat_schedule = {
    "countdown": {"task": "groupme.tasks.countdown_check", "schedule": 10.0},
    "birthdays": {
        "task": "groupme.tasks.birthdays",
        "schedule": daily_morning,
    },
}
