from src.webcamList import webcams

from src.dataCollecter.frameCaptureWrapper import frameCaputureWrapper
from src.dataCollecter.screenshotCaptureWrapper import screenshotCaptureWrapper
from src.utils import dataUtils

img_prefix = dataUtils.image_prefix_generator('dublin')
# dublin = imageCollector(webcams.dublin)
dublin = screenshotCaptureWrapper(webcams.dublin, 'Dublin', img_prefix)
res = dublin.capture_frame_by_screenshot_wrapper(num_im=3, time_interval=3)
dataUtils.store_as_csv(res, dublin.target_img_path, dublin.image_prefix)


