import requests


class Weather_module:
    def __init__(self, city, lang, api_key):
        self.city = city
        self.lang = lang
        self.key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def get_weather(self):
        complete_url = self.base_url + "appid=" + self.key + "&q=" + self.city

        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature = round(current_temperature - 273.0, 1)
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]

            weather_description = z[0]["description"]

            print(" Temperature (in kelvin unit) = " +
                  str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(current_pressure) +
                  "\n humidity (in percentage) = " +
                  str(current_humidity) +
                  "\n description = " +
                  str(weather_description))

            return f'Today is {weather_description}.' \
                   f'The temperature is {current_temperature} degrees Celsius.' \
                   f'Humidity is {current_humidity} percent.'

        else:
            return "City Not Found"
