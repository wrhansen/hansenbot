import datetime
import typing
from calendar import monthrange

from django.db import models


class BirthdayMixin:
    birthdate: datetime.date

    @property
    def age(self):
        today = datetime.date.today()
        return (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

    @property
    def str_age(self) -> str:
        milestone = "year"

        age = self.age
        if age < 2:
            today = datetime.date.today()
            age = self.monthdelta(self.birthdate, today)
            if age == 0:  # New born age milestones
                days = (today - self.birthdate).days
                if today.day == self.birthdate.day:  # Months milestone
                    if (
                        today.month == self.birthdate.month
                        and today.year != self.birthdate.year
                    ):  # let's say 1 year instead of 12 months
                        age = 1
                        milestone = "year"
                    else:
                        age = days // 30
                        milestone = "month"
                elif days < 30:  # Do days for any child under
                    age = days
                    milestone = "day"
                else:  # Weeks milestone
                    age = days // 7
                    milestone = "week"
        s = "s" if age > 1 else ""
        return f"{age} {milestone}{s} old"

    def monthdelta(self, d1, d2):
        delta = 0
        while True:
            mdays = monthrange(d1.year, d1.month)[1]
            d1 += datetime.timedelta(days=mdays)
            if d1 <= d2:
                delta += 1
            else:
                break
        return delta

    @property
    def next_bday(self):
        today = datetime.date.today()

        this_year_bday = datetime.date(
            year=today.year, month=self.birthdate.month, day=self.birthdate.day
        )

        if this_year_bday >= today:
            next_birthday = this_year_bday
        else:
            next_birthday = datetime.date(
                year=today.year + 1, month=self.birthdate.month, day=self.birthdate.day
            )

        timedelta = next_birthday - today
        return timedelta.days


class Birthday(models.Model, BirthdayMixin):
    name = models.CharField(max_length=64)
    birthdate = models.DateField(db_index=True)

    class Meta:
        ordering = ["birthdate"]

    def __str__(self):
        return f"{self.name} : {self.birthdate} : {self.age} : {self.next_bday}"


class Weather(models.Model):
    city = models.CharField(
        max_length=64, blank=True, help_text="City is displayed in the bot message"
    )
    state = models.CharField(
        max_length=64, blank=True, help_text="State is displayed in the bot message"
    )
    zipcode = models.CharField(
        max_length=64,
        help_text="Required to lookup the weather data on openweathermap.org API.",
    )
    country_code = models.CharField(
        max_length=32,
        help_text="2-digit country code. Required to lookup the weather data on openweathermap.org API.",
    )

    class Meta:
        verbose_name_plural = "Weather"

    def __str__(self):
        return f"{self.id} : {self.city}, {self.state}, {self.country_code}  {self.zipcode}"


class Countdown(models.Model):
    event = models.CharField(max_length=255)
    deadline = models.DateTimeField()


class Pet(models.Model, BirthdayMixin):
    PET_DOG = "dog"
    PET_CAT = "cat"
    PET_TYPES = [
        (PET_DOG, "Dog"),
        (PET_CAT, "Cat"),
    ]

    name = models.CharField(max_length=64)
    birthdate = models.DateField(db_index=True)
    type = models.CharField(max_length=64, choices=PET_TYPES)

    def __str__(self):
        return f"{self.name} : {self.type} : {self.birthdate} : {self.age} : {self.next_bday}"
