import requests

def get_weather(city):
    weather = 'https://weather.ls.hereapi.com/weather/1.0/report.json?product=observation&name={}&apiKey=OD6LfhsDdjGDFwHGjk3igxNeo1venf9kvq-BzS3it10'.format(city)
    r_json = requests.get(weather).json()
    local_json = r_json['observations']['location'][0]['observation'][0]
    weather = dict(
    skyDescription = local_json['skyDescription'],
    temperature = local_json['temperature'],
    temperatureDesc = local_json['temperatureDesc'],
    humidity = local_json['humidity'],
    windSpeed = local_json['windSpeed'],
    )
    
    
    return weather