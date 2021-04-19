import datetime
import logging
from typing import Dict, Optional

import requests
from django.conf import settings

from .models import Birthday, Pet, Weather

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

    def get_weather_by_zip(self, zip_code, country_code):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "zip": f"{zip_code},{country_code.lower()}",
                "appid": settings.GROUPME["OPEN_WEATHER_API_KEY"],
                "units": "imperial",
            },
        )
        response.raise_for_status()
        return response.json()

    def get_weather_data_string(self):
        weather_data = []
        for weather in Weather.objects.all():
            try:
                api_data = self.get_weather_by_zip(
                    weather.zipcode, weather.country_code
                )
            except requests.exceptions.HTTPError:
                logger.warning(f"Couldn't lookup weather for: {weather}")

            weather_data.append(
                {
                    "location": f"{weather.city}, {weather.state}",
                    "description": api_data["weather"][0]["main"],
                    "temp": api_data["main"]["temp"],
                }
            )

        weather_string = "\n".join(
            [
                f"* {datum['location']} : {datum['temp']}°F -- {datum['description']}"
                for datum in weather_data
            ]
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
