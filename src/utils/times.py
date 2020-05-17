import time
from datetime import datetime
from pytz import timezone
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_time(tz=None):
    '''
    tz (str): Time zone from package pytz. Default is None, then apply utc time. 
    '''
    if tz is None:
        current_time = datetime.utcnow().strftime(
            "%a %Y-%m-%d %H:%M:%S")
        
    else:
        current_time = datetime.now(
            timezone(tz)).strftime("%a %Y-%m-%d %H:%M:%S")

    return current_time

def tz_finder(city):
    
    geolocator = Nominatim(user_agent="tz_finder")
    location = geolocator.geocode(city)

    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=location.longitude, lat=location.latitude)

    return tz

# if __name__ == "__main__":
#     print(tz_finder('Elburg'))
