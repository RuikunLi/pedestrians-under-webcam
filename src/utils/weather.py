import requests

def get_weather(city):
    try:
        weather_url = 'https://weather.ls.hereapi.com/weather/1.0/report.json?product=observation&name={}&apiKey=OD6LfhsDdjGDFwHGjk3igxNeo1venf9kvq-BzS3it10'.format(city)
        status_code = requests.get(weather_url).status_code
        if status_code != 200:
            raise ValueError("Error {}".format(status_code))
        else:
            r_json = requests.get(weather_url).json()
            local_json = r_json['observations']['location'][0]['observation'][0]
            weather = dict(
            skyDescription = local_json['skyDescription'],
            temperature = local_json['temperature'],
            temperatureDesc = local_json['temperatureDesc'],
            humidity = local_json['humidity'],
            windSpeed = local_json['windSpeed'],
            )
            return weather
    except Exception as e:
        print('---can not get the weather---')
        print(e)
    
    