import cv2
import os
from ..webcamList import webcams
from .imageCollector import imageCollector
from ..utils import times, weather
import time


class screenshotCaptureWrapper(imageCollector):
    def __init__(self, webcam_url, city, image_prefix):
        super().__init__(webcam_url, city, image_prefix)


    def capture_frame_by_screenshot(self,
                                    image_index=0):
        """
       capture an image by taking a screenshot on an opened website via browser.
        
        Args:
            image_prefix (str): Prefix of target images. The postfix is numerated by numbers.
            image_index (int): The postfix of target images. By default, numerated from 0.
            mprob (int): Minimum probability to be a person.
			tz (str): Time zone from package pytz. Default is None, then apply utc time. Use function pytz.all_timezones to get the list of timezones.

        
        Returns:
            tuple: The name of target image, the number of persons in an image detected by the model and the current time.
        
        """
		
        dir_path = os.path.join(self.target_img_path, self.image_prefix)

        if self.driver is None:
            print("Web driver is none.")
            return None
        else:
            print("-----------------------------------------------------")


            target_img_name = "{}_{}.png".format(self.image_prefix, image_index)
            print("Taking screenshot {}...".format(image_index))
            self.driver.save_screenshot(
                os.path.join(dir_path, target_img_name))
            
            current_time = times.get_time(self.tz)
            current_weather = weather.get_weather(self.city)

            return target_img_name, current_time, current_weather

    def capture_frame_by_screenshot_wrapper(self,
                                        num_im=6,
                                        time_interval=10):
        """
        A wrapper of the function capture_frame_by_stream.
        
        Args:
            num_im (int): How many images will be taken.
            time_interval (int): Time interval of taking next image, the unit is second.        
        Returns:
            void
        
        """
        print("The current conuting function is based on capture frame by screenshot.")
        
        results = []
        dir_path = os.path.join(self.target_img_path, self.image_prefix)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if num_im <= 0:
            try:
                i = 0
                while True:
                    i = i + 1
                    result = self.capture_frame_by_screenshot(i)
                    results.append(result)
                    time.sleep(time_interval)
                    
            except KeyboardInterrupt:
                print('Abort by key interrupt.')
                if self.driver is not None:
                    self.driver.quit()
                return results
        else:
            for i in range(num_im):
                result = self.capture_frame_by_screenshot(i)
                results.append(result)
                time.sleep(time_interval)
                
            if self.driver is not None:
                self.driver.quit()

            return results
