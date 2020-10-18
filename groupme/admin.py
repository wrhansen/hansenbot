from django.contrib import admin

from .models import Birthday, Weather


class BirthdayAdmin(admin.ModelAdmin):
    list_display = ("name", "birthdate", "age", "next_bday")


admin.site.register(Birthday, BirthdayAdmin)


class WeatherAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "zipcode", "country_code")


admin.site.register(Weather, WeatherAdmin)
