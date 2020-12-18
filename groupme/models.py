import datetime
from calendar import monthrange

from django.db import models


class Birthday(models.Model):
    name = models.CharField(max_length=64)
    birthdate = models.DateField(db_index=True)

    class Meta:
        ordering = ["birthdate"]

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
        milestone = "months old" if self.age < 2 else "years old"

        age = self.age
        if age < 2:
            age = self.monthdelta(self.birthdate, datetime.date.today())
        return f"{age} {milestone}"

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
