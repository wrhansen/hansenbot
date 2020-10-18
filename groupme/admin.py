from django.contrib import admin

from .models import Birthday, Weather


class BirthdayAdmin(admin.ModelAdmin):
    list_display = ("name", "birthdate", "age", "next_bday")


class WeatherAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "zipcode", "country_code")


class GroupMeBotAdminSite(admin.AdminSite):
    site_header = "GroupMe Bot Admin"
    site_title = "HansenBot"


admin_site = GroupMeBotAdminSite(name="myadmin")
admin_site.register(Birthday, BirthdayAdmin)
admin_site.register(Weather, WeatherAdmin)
