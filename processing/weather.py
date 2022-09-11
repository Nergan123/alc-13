import requests
from logger import LoggingHandler


class Weather_module(LoggingHandler):
    def __init__(self, city, lang, api_key):
        super().__init__()
        self.log.info(f'Setting up weather module')
        self.city = city
        self.lang = lang
        self.key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.log.info(f'Weather module setup complete')

    def get_weather(self):
        self.log.info(f'Getting weather')
        complete_url = self.base_url + "appid=" + self.key + "&q=" + self.city

        response = requests.get(complete_url)
        x = response.json()
        self.log.info(f'Got response: {x["cod"]}')
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

            self.log.info(f'Returning: Today is {weather_description}. \
                   The temperature is {current_temperature} degrees Celsius. \
                   Humidity is {current_humidity} percent')

            return f'Today is {weather_description}.' \
                   f'The temperature is {current_temperature} degrees Celsius.' \
                   f'Humidity is {current_humidity} percent.'

        else:
            self.log.warning(f'City not found')
            return "City Not Found"
