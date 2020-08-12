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
        image_prefix = dataUtils.image_prefix_generator(self.image_prefix)

        if self.driver is None:
            print("Web driver is none.")
            return None
        else:
            print("-----------------------------------------------------")


            target_img_name = "{}_screenshot_{}_{}.png".format(image_prefix, self.platform, image_index)
            print("Taking screenshot {}...".format(image_index))
            self.driver.save_screenshot(os.path.join(self.target_img_path, target_img_name))
            self.upload_img_to_google_drive(self.google_drive_folder_id, os.path.join(self.target_img_path, target_img_name), target_img_name)
            
            print(os.path.join(self.target_img_path, target_img_name))
            current_time = ''
            current_weather = ''
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

            try:
                result.append(target_img_name)
            except Exception as e:
                    print('---can append target img name--')
                    print(e)
            
            try:
                result.append(current_time)
            except Exception as e:
                    print('---can append current time--')
                    print(e)
            try:
                result.extend(current_weather)
            except Exception as e:
                    print('---can append current weather--')
                    print(e)
            try:
                result.append(self.platform)
            except Exception as e:
                    print('---can append platform--')
                    print(e)
            
            return result
    def capture_frame_by_screenshot_wrapper(self,
                                        num_im=6,
                                        time_interval=10,
                                        bsize=1):
        """
        A wrapper of the function capture_frame_by_stream.
        
        Args:
            num_im (int): How many images will be taken.
            time_interval (int): Time interval of taking next image, the unit is second.  
            bszie: batch size.      
        Returns:
            void
        
        """
        results = []
        # if not os.path.isdir(target_img_path):
        os.makedirs(self.target_img_path, exist_ok=True)
        print("The current collecting function is based on capture frame by screenshot.")
        if (num_im-1) * time_interval/60 >= 30 or num_im >= 100:
            print("time range is too long or num of images is too big, will take batch， batch size is {}".format(bsize))
            b = 0
            for batch in range(0, num_im, bsize):
                vars()['batch_'+str(b)] = [i for i in range(num_im)][batch:batch+bsize]
                indexes = eval('batch_'+str(b))
                print("The current batch is " + str(indexes))
                for i in indexes:
                    try:
                        result = self.capture_frame_by_screenshot(i)
                        self.insert_to_google_sheet(result, 'collector', self.image_prefix, index=i)
                        results.append(result)
                        time.sleep(time_interval)
                    except Exception as e:
                        print(e)
                    b = b + 1     
            if self.driver is not None:
                self.driver.quit()

            return results
        elif num_im <= 0:
            try:
                i = 0
                while True:
                    try:
                        i = i + 1
                        result = self.capture_frame_by_screenshot(i)
                        self.insert_to_google_sheet(result, 'collector', self.image_prefix, index=i)
                    
                        results.append(result)
                        time.sleep(time_interval)
                    except Exception as e:
                        print(e)
            except KeyboardInterrupt:
                print('Abort by key interrupt.')
                if self.driver is not None:
                    self.driver.quit()
                return results
        else:
            for i in range(num_im):
                try:
                    result = self.capture_frame_by_screenshot(i)
                    self.insert_to_google_sheet(result, 'collector', self.image_prefix, index=i)
                    results.append(result)
                    time.sleep(time_interval)
                except Exception as e:
                    print(e)
                
            if self.driver is not None:
                self.driver.quit()

            return results
