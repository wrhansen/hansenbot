from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .models import Birthday, Pet, Weather


class BirthdayAdmin(admin.ModelAdmin):
    list_display = ("name", "birthdate", "age", "next_bday", "str_age")


class WeatherAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "zipcode", "country_code")


class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "birthdate", "age", "next_bday", "str_age")


class GroupMeBotAdminSite(admin.AdminSite):
    site_header = "HansenBot Admin"
    site_title = "HansenBot"
    index_title = "HansenBot"


admin_site = GroupMeBotAdminSite(name="myadmin")
admin_site.register(Birthday, BirthdayAdmin)
admin_site.register(Weather, WeatherAdmin)
admin_site.register(Pet, PetAdmin)

# Standard User/Group admin stuff
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
