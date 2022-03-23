"""
A script that send to a specific or multiple persons whatsApp message with the weather of today.
"""

import requests  # a module that allows us to send a request to API
import os
import pywhatkit

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')


def kelvin_to_celsius(kelv: float) -> float:
    return round(kelv - 273.15, 1)


def build_message(city_, temp_now_, temp_feel_, temp_max_, temp_min_, rain_chance_, clouds_):
    message = f"Here is the weather for {city_} today.\nThe temp right now is {temp_now_}C\nBut feels like {temp_feel_}C\n" \
              f"The max temp is {temp_max_}C and the min {temp_min_}C\nchance for rain is {int(rain_chance_)}%\n" \
              f"Clouds in the sky: {clouds_}%"

    return message


def send_whatsapp(message: str) -> None:
    #                     Phone number   message   hour  min
    pywhatkit.sendwhatmsg("+972524350004", message, 20, 31)


def handle():
    # Api key from the website https://openweathermap.org/current
    API_KEY = "1a0fcb238d897b78bb6929f050d4bb21"
    BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

    # Now we will ask for the city that I want the weather of it
    cities = ["Tel Aviv", "Rosh-HaAyin", "Herzliya"]
    lang = "he"

    # here I need to build a url with my city
    request_url = f"{BASE_URL}?appid={API_KEY}&q={cities[0]}&lang={lang}"

    # Now I need to send a request to this URL
    response = requests.get(request_url)
    # Check if the response is OK and don't has any issue a long the way
    if response.status_code == 200:
        data = response.json()

        city = cities[1]
        temp_now = kelvin_to_celsius(data["list"][0]["main"]["temp"])
        temp_feel = kelvin_to_celsius(data["list"][0]["main"]["feels_like"])
        temp_max = kelvin_to_celsius(data["list"][0]["main"]["temp_max"])
        temp_min = kelvin_to_celsius(data["list"][0]["main"]["temp_min"])
        rain_chance = data["list"][0]["pop"] * 100
        clouds = data["list"][0]["clouds"]["all"]
        description = data["list"][0]["weather"][0]["description"]

        message = build_message(city, temp_now, temp_feel, temp_max, temp_min, rain_chance, clouds)
        send_whatsapp(message)

    else:
        print("An error occurred.")


if __name__ == '__main__':
    handle()
