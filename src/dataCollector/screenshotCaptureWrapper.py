import cv2
import os
from ..webcamList import webcams
from .imageCollector import imageCollector
from ..utils import times, weather, dataUtils
import time


class screenshotCaptureWrapper(imageCollector):
    def __init__(self, webcam_url, city):
        super().__init__(webcam_url, city)
        self.init_webdriver()
        

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

        result = []
        self.image_prefix = dataUtils.image_prefix_generator(self.city)

        if self.driver is None:
            print("Web driver is none.")
            return None
        else:
            print("-----------------------------------------------------")


            target_img_name = "{}_screenshot_{}.png".format(self.image_prefix, image_index)
            print("Taking screenshot {}...".format(image_index))
            self.driver.save_screenshot(os.path.join(self.target_img_path, target_img_name))
            dataUtils.upload_img_to_google_drive(self.google_drive_folder_id, os.path.join(self.target_img_path, target_img_name), target_img_name)
            print(os.path.join(self.target_img_path, target_img_name))
            current_time = None
            current_weather = None
            try:
                current_time = times.get_time(self.tz)
                print(current_time)
            except Exception as e:
                print('--- can not get the current time---')
                print(e)
            try:
                current_weather = weather.get_weather(self.city)
            except Exception as e:
                print('---can not get the current weather---')
                print(e)

            result.append(target_img_name)
            result.append(current_time)
            result.extend(current_weather)

            return result
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
        print("The current collecting function is based on capture frame by screenshot.")
        
        results = []
        # if not os.path.isdir(target_img_path):
        os.makedirs(self.target_img_path, exist_ok=True)
        if num_im <= 0:
            try:
                i = 0
                while True:
                    i = i + 1
                    result = self.capture_frame_by_screenshot(i)
                    dataUtils.insert_to_google_sheet(result, 'collector', self.city, index=i)
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
                dataUtils.insert_to_google_sheet(result, 'collector', self.city, index=i)
                results.append(result)
                time.sleep(time_interval)
                
            if self.driver is not None:
                self.driver.quit()

            return results
