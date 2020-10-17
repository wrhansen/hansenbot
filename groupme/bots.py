import logging
from typing import Dict, Optional

import requests
from django.conf import settings

from .models import Birthday

BOT_INVOCATION = "!hb"

logger = logging.getLogger(__name__)

registry: Dict = {}


class ParseError(Exception):
    pass


class RegistryError(Exception):
    pass


def parse_command(message):
    try:
        invocation, command, *extra = message.strip().split(" ")
    except ValueError:
        raise ParseError("Unknown Format")

    if invocation != BOT_INVOCATION:
        raise ParseError("Invocation not used.")

    return command, extra


class GroupMeBotType(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if bases:
            if not cls.help_text:
                raise RegistryError(f"`help_text` missing for {cls.__name__}")
            registry[cls.command] = cls
        return cls


class GroupMeBot(metaclass=GroupMeBotType):
    command: Optional[str] = None
    help_text: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        raise NotImplementedError("Implement this!")

    def post_message(self, text):
        response = requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={"text": text, "bot_id": settings.GROUPME["BOT_ID"]},
        )
        logger.info(
            "Bot Message Posted",
            extra={
                "status": response.status_code,
                "text": text,
            },
        )


class HelpCommandBot(GroupMeBot):
    command = "help"
    help_text = "Shows this message, a list of available commands"

    def execute(self):
        help_texts = [
            f"* {BotClass.command} - {BotClass.help_text}"
            for BotClass in registry.values()
        ]

        help_text_list = "\n".join(help_texts)
        message = f"""Commands are invoked like: "{BOT_INVOCATION} <command>"

Available Commands:
{help_text_list}"""
        self.post_message(message)


class BirthdayCommandBot(GroupMeBot):
    command = "birthday"
    help_text = "Lists family birthdays"

    def execute(self):
        birthday_list = [
            (bday.name, bday.age, bday.next_bday, bday.birthdate)
            for bday in Birthday.objects.all()
        ]

        (name, age, next_bday, birthdate) = min(birthday_list, key=lambda x: x[2])
        age += 1

        birthday_list_str = "\n".join(
            f"    {b[0]} : {b[1]} years old ({b[3]})" for b in birthday_list
        )

        message = f"""I know the following birthdays:
{birthday_list_str}

Next upcoming birthday: {name} turns {age} in {next_bday} days!"""

        self.post_message(message)


class DadJokeCommandBot(GroupMeBot):
    command = "dadjoke"
    help_text = "Returns a random dad joke"

    def execute(self):
        response = requests.get(
            "https://icanhazdadjoke.com/", headers={"accept": "application/json"}
        )
        joke = response.json()["joke"]

        self.post_message(f"Dad Joke: {joke}")
