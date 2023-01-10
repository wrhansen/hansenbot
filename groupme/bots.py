import datetime
import logging
from typing import Dict, Optional

import requests
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Birthday, Pet, Reminder, Weather
from .weather import WeatherAPI, WeatherAPIFormatter

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

        if len(self.args):
            self.prompt = " ".join(self.args[0])
        else:
            self.prompt = ""

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

    def _get_birthday_list(self):
        return [
            (
                bday.name,
                bday.age,
                bday.next_bday,
                bday.birthdate,
                bday.str_age,
            )
            for bday in Birthday.objects.all()
        ]

    def next_birthday(self, birthday_list):
        return min(birthday_list, key=lambda x: x[2])

    def digest(self):
        birthday_list = self._get_birthday_list()

        (name, age, next_bday, birthdate, birthdate_str) = self.next_birthday(
            birthday_list
        )
        if next_bday == 0:
            if birthdate.year == datetime.datetime.now().year:  # Born today
                return f"{name} is born today! Welcome to the family!"
            else:
                return f"Happy Birthday! {name} turns {age} today!"
        elif next_bday < 15:
            return f"Birthdays: \nNext upcoming birthday: {name} turns {age+1} in {next_bday} days!"
        else:
            return ""

    def execute(self):
        birthday_list = self._get_birthday_list()

        (name, age, next_bday, birthdate, birthdate_str) = self.next_birthday(
            birthday_list
        )

        birthday_list_str = "\n".join(
            f"    {b[0]} : {b[4]} ({b[3]})" for b in birthday_list
        )

        if next_bday == 0:
            if birthdate.year == datetime.datetime.now().year:  # Born today
                return f"{name} is born today! Welcome to the family!"
            else:
                next_bday_message = f"Happy Birthday! {name} turns {age} today!"
        else:
            next_bday_message = (
                f"Next upcoming birthday: {name} turns {age+1} in {next_bday} days!"
            )

        message = f"""I know the following birthdays:
{birthday_list_str}

{next_bday_message}"""

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


class WeatherCommandBot(GroupMeBot):
    command = "weather"
    help_text = "Returns current weather information"

    def get_weather_data_string(self):
        weather_data = []
        api = WeatherAPI(settings.GROUPME["WEATHER_API_COM_KEY"])

        for weather in Weather.objects.all():
            try:
                api_data = api.get_weather_by_zip(weather.zipcode)
            except requests.exceptions.HTTPError:
                logger.exception(f"Couldn't lookup weather for: {weather}")
            else:
                formatter = WeatherAPIFormatter(api_data)
                weather_format = formatter.format()

                weather_data.append(
                    {
                        "location": f"{weather.city}, {weather.state}",
                        "description": weather_format,
                    }
                )

        weather_string = "\n".join(
            [f"* {datum['location']}: {datum['description']}" for datum in weather_data]
        )
        return weather_string

    def digest(self):
        return f"Weather:\n{self.get_weather_data_string()}"

    def execute(self):
        weather_string = self.get_weather_data_string()
        self.post_message(f"Weather:\n{weather_string}")


class PetCommandBot(GroupMeBot):
    command = "pets"
    help_text = "List information about the family's pets"

    def execute(self):
        pet_list = [
            (
                bday.name,
                bday.age,
                bday.next_bday,
                bday.birthdate,
                bday.str_age,
            )
            for bday in Pet.objects.all()
        ]

        (name, age, next_bday, birthdate, birthdate_str) = min(
            pet_list, key=lambda x: x[2]
        )
        if next_bday == 0:
            next_bday_message = f"Happy Birthday! {name} turns {age} today!"
        else:
            next_bday_message = (
                f"Next upcoming birthday: {name} turns {age+1} in {next_bday} days!"
            )

        pet_list_str = "\n".join(f"    {b[0]} : {b[4]} ({b[3]})" for b in pet_list)

        message = f"""I know the following pets:
{pet_list_str}

{next_bday_message}!"""

        self.post_message(message)


class ReminderCommandBot(GroupMeBot):
    command = "reminder"
    help_text = "List reminders to the group"

    def execute(self):
        reminder_string = self.render_reminder_string()
        self.post_message(
            f"""Reminders:
{reminder_string}"""
        )

    def digest(self):
        reminder_string = self.render_reminder_string()
        if reminder_string:
            reminder_string = f"Reminders:\n{reminder_string}"
        return reminder_string

    def render_reminder_string(self):

        reminders = Reminder.objects.filter(
            Q(expires__gt=timezone.now().date()) | Q(expires__isnull=True)
        )
        return render_to_string("reminder.txt", {"reminders": reminders})


class OpenAICommandBot(GroupMeBot):
    command = "ai"
    help_text = "Talk to me, I am here to assist you with whatever you need."

    def execute(self):
        import openai

        openai.api_key = settings.OPENAI_KEY

        completion = openai.Completion.create(
            prompt=self.prompt, **settings.OPENAI_SETTINGS
        )
        answer = completion["choices"][0]["text"]
        self.post_message(answer.strip())
