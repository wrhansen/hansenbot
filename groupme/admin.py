from django.contrib import admin

from .models import Birthday


class BirthdayAdmin(admin.ModelAdmin):
    list_display = ("name", "birthdate", "age", "next_bday")


admin.site.register(Birthday, BirthdayAdmin)
