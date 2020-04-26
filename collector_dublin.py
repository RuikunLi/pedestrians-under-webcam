from src.webcamList import webcams
from src.dataCollector.frameCaptureWrapper import frameCaptureWrapper
from src.dataCollector.screenshotCaptureWrapper import screenshotCaptureWrapper
from src.utils import dataUtils, emailNotification

img_prefix = dataUtils.image_prefix_generator('dublin')
num_im = 3
time_interval = 3
city = 'Dublin'


try:
    collector = frameCaptureWrapper(webcam_url=webcams.dublin, city=city, image_prefix=img_prefix)
    res = collector.capture_frame_by_stream_wrapper(num_im=num_im, time_interval=time_interval)

except:
    collector = screenshotCaptureWrapper(webcam_url=webcams.dublin, city=city, image_prefix=img_prefix)
    res = collector.capture_frame_by_screenshot_wrapper(num_im=num_im, time_interval=time_interval)

dataUtils.store_as_csv(res, collector.target_img_path, collector.image_prefix)
emailNotification.emailNotification(prefix=img_prefix, num=num_im, time_interval=time_interval)


