from django.db import models

from .mixins import BirthdayMixin


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
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

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


class Reminder(models.Model):
    message = models.TextField()
    expires = models.DateField(default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Reminders"
