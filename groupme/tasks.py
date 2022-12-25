import logging

from celery.schedules import crontab

from website import celery_app as app

from .bots import GroupMeBot, ParseError, parse_command, registry

logger = logging.getLogger(__name__)
app.conf.update(timezone="America/Detroit")


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
every_minute = crontab()
every_30_minutes = crontab(minute="*/30")
afternoon = crontab(minute=0, hour=13)


@app.task
def morning_digest():
    """
    Daily morning routine that checks for upcoming birthdays and countdowns and
    updates the family on what to expect for the day.
    """
    logger.info("morning_digest() run!")
    messages = []
    for Bot in registry.values():
        bot = Bot()
        if hasattr(bot, "digest"):
            try:
                message = bot.digest()
                if message:
                    messages.append(bot.digest())
            except Exception:
                logger.exception(
                    "Error with bot digest", exc_info=True, extra={"bot_class": Bot}
                )

    if messages:
        bot = GroupMeBot()
        messages_str = "\n\n".join(messages)
        bot_message = f"Good Morning Hansen Family!\nHere is what you need to know today:\n\n{messages_str}"
        bot.post_message(bot_message)


# Celery Beat schedule for the groupme app.
app.conf.beat_schedule = {
    "morning_digest": {
        "task": "groupme.tasks.morning_digest",
        "schedule": every_minute,
    },
}
