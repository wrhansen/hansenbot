from django.urls import path

from . import views

urlpatterns = [
    path(
        "bots/hansenbot/webhook/",
        views.HansenBotWebhook.as_view(),
        name="hansenbot-webhook",
    ),
]
