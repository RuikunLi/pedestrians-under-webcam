from src.webcamList import webcams
from src.dataCollector.frameCaptureWrapper import frameCaptureWrapper
from src.dataCollector.screenshotCaptureWrapper import screenshotCaptureWrapper
from src.utils.times import tz_finder
from src.utils import dataUtils, emailNotification
from datetime import datetime 
import pytz

 
# img_prefix = dataUtils.image_prefix_generator('dublin')
print("List of city webcams:")
print(list(webcams.webcams.keys()))
city = input("Enter city name:")
if city not in list(webcams.webcams.keys()):
    raise ValueError("enterted city not in the list")
        
num_im = int(input("Enter the number of images:"))
time = float(input("Enter the time interval (in min):"))
time_interval = int(time * 60)

# num_im = 2
# time_interval = 5

webcam = webcams.webcams[city]
try:
    city_tz = city.split('_', 1)[0]
    tz = tz_finder(city_tz)
    start = datetime.now(pytz.timezone(tz))
    print('------------------Start---------------')
    print('The current is webcam is from {}, timezone is {}, required the number of images is {}, time interval is {} minutes'.format(city, tz, num_im, time_interval/60))
except Exception as e:
    print(e)

bystreamflag = True

if bystreamflag:
    try:
        collector = frameCaptureWrapper(webcam_url=webcam, city=city)
        res = collector.capture_frame_by_stream_wrapper(num_im=num_im, time_interval=time_interval)
        method = 'stream'

    except Exception as e:
        print("---frame capture failed---")
        print(e)
        collector = screenshotCaptureWrapper(webcam_url=webcam, city=city)
        res = collector.capture_frame_by_screenshot_wrapper(num_im=num_im, time_interval=time_interval)
        method = 'screenshot'
else:
    collector = screenshotCaptureWrapper(webcam_url=webcam, city=city)
    res = collector.capture_frame_by_screenshot_wrapper(num_im=num_im, time_interval=time_interval)
    method = 'screenshot'
end = datetime.now(pytz.timezone(tz))
dataUtils.init_permisson_google_drive(role='writer')
dataUtils.store_as_csv(data=res, dir_path=collector.dir_path, image_prefix=collector.image_prefix)
emailNotification.emailNotification(city=city, num=num_im, time_interval=time_interval, start=start, end=end, url=webcam, method=method, tz=tz, path=collector.dir_path)

print('------------------End---------------')
