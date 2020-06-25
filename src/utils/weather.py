import requests

def get_weather(city):
    print('getting weather of {}...'.format(city))
    try:
        weather_url = 'https://weather.ls.hereapi.com/weather/1.0/report.json?apiKey=RJZ0LgP7DcxKohEaMSCeMkPUBWev7ddOijgIVQQjmtg&product=observation&name={}'.format(city)
        status_code = requests.get(weather_url).status_code
        if status_code != 200:
            raise ValueError("Error {}".format(status_code))
        else:
            r_json = requests.get(weather_url).json()
            local_json = r_json['observations']['location'][0]['observation'][0]
            # weather = dict(
            # skyDescription = local_json['skyDescription'],
            # temperature = local_json['temperature'],
            # temperatureDesc = local_json['temperatureDesc'],
            # humidity = local_json['humidity'],
            # windSpeed = local_json['windSpeed'],
            # )
            weather = [
            local_json['skyDescription'],
            local_json['temperature'],
            local_json['temperatureDesc'],
            local_json['humidity'],
            local_json['windSpeed'],
            ]
            return weather
    except Exception as e:
        print('---can not get the weather---')
        print(e)

# if __name__ == "__main__":
#     print(get_weather('LA'))

    
    