import enum

import requests
from django.template.loader import render_to_string

# All available weather codes
# Source: https://openweathermap.org/weather-conditions
WEATHER_MAPPING = {
    "Thunderstorm": "⛈",
    "Drizzle": "🌧",
    "Rain": "💧",
    "Snow": "❄",
    "Mist": "🌧",
    "Haze": "🌧",
    "Fog": "🌁",
    "Ash": "🌋",
    "Tornado": "🌪",
    "Clear": "☀",
    "Clouds": "☁",
}


class Units(str, enum.Enum):
    IMPERIAL = "imperial"
    STANDARD = "standard"
    METRIC = "metric"


class OpenWeatherMapAPI:
    base_url = "https://api.openweathermap.org/data/2.5"

    def __init__(self, appid, units):
        self.appid = appid
        self.units = units

    def fetch(self, url, params):
        params["appid"] = self.appid
        params["units"] = self.units
        response = requests.get(url, params)
        response.raise_for_status()
        return response.json()

    def get_weather_by_zip(self, zip_code, country_code):
        url = f"{self.base_url}/weather"
        params = {"zip": f"{zip_code},{country_code.lower()}"}
        return self.fetch(url, params)

    def one_call(self, latitude: str, longitude: str):
        url = f"{self.base_url}/onecall"
        params = {"lon": longitude, "lat": latitude}
        return self.fetch(url, params)


class WeatherFormat:
    def __init__(self, data):
        self.data = data

    def weather_format(self, weather):
        return WEATHER_MAPPING.get(weather, weather)

    def format(self):

        context = {}
        # Current Weather
        current = self.data["current"]
        context["current_temp"] = current["temp"]
        context["current_weather"] = self.weather_format(current["weather"][0]["main"])

        # Forecast Today
        today = self.data["daily"][0]
        context["today_high"] = today["temp"]["max"]
        context["today_low"] = today["temp"]["min"]
        context["today_weather"] = self.weather_format(today["weather"][0]["main"])
        return render_to_string("weather.html", context)


class WeatherAPI:
    '''
    This is a class that encapsulates weatherapi.com data.
    Going to see if this data is better than openweathermap.org
    '''
    base_url = "https://api.weatherapi.com/v1"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch(self, url, params):
        params["key"] = self.api_key
        response = requests.get(url, params)
        response.raise_for_status()
        return response.json()

    def get_weather_by_zip(self, zipcode, days=3):
        url = f"{self.base_url}/forecast.json"
        params = {
            "days": days,
            "q": zipcode,
            "aqi": "no",
            "alerts": "no",
        }
        return self.fetch(url, params)


class WeatherAPIFormatter:
    def __init__(self, data):
        self.data = data

    def format(self):
        current = data["current"]
        forecast = data["forecast"]["forecastday"][0]["day"]
        context = {
            "current_temp": current["temp_f"],
            "current_weather": WEATHER_MAPPING.get(current["condition"]["text"], current["condition"]["text"]),
            "today_high": forecast["maxtemp_f"],
            "today_low": forecast["mintemp_f"],
            "today_weather": WEATHER_MAPPING.get(forecast["condition"]["text"], forecast["condition"]["text"]),
        }

        return render_to_string("weather.html", context)
