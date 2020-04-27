import streamlink
import cv2
import os
from ..webcamList import webcams
from .imageCollector import imageCollector
from ..utils import times, weather
import time


class frameCaptureWrapper(imageCollector):
    def __init__(self, webcam_url, city):
        super().__init__(webcam_url, city)
        self.init_streamlink()

    def capture_frame_by_stream(self,
                                image_index=0
                                ):
        """
        capture a frame from a online stream, namely webcam. And store it as an image.

        Args:
            image_prefix (str): Prefix of target images. The postfix is numerated by numbers.
            image_index (int): The postfix of target images. By default, numerated from 0.

        Returns:
            tuple: The name of target image, the number of persons in an image detected by the model and the current time.
        """
        # image_prefix = self.image_prefix + '_stream'
        self.init_streamlink()
        video_cap = cv2.VideoCapture(self.stream_url)
        dir_path = os.path.join(self.target_img_path, self.image_prefix)

        if video_cap is None:
            print("Open webcam [%s] failed." %self.webcam_url)
            return None
        else:
            ret, frame = video_cap.read()
            if not ret:
                video_cap.release()
                raise ValueError("Captured frame is broken.")
            else:
                print("-----------------------------------------------------")
                print("Capturing frame %d." % image_index)
                target_img_name = "{}_{}.png".format(self.image_prefix, image_index)
                cv2.imwrite(os.path.join(dir_path, target_img_name), frame)
                print(dir_path, target_img_name)

                video_cap.release()

                current_time = times.get_time(self.tz)
                current_weather = weather.get_weather(self.city)

                return target_img_name, current_time, current_weather

    def capture_frame_by_stream_wrapper(self,
                                        num_im=6,
                                        time_interval=10):
        """
        A wrapper of the function capture_frame_by_stream.
        
        Args:
            image_prefix (str): Prefix of target images. The postfix is numerated by numbers.
            mprob (int): Minimum probability to be a person.
            num_im (int): How many images will be taken.
            time_interval (int): Time interval of taking next image, the unit is second.        
        Returns:
            void
        
        """
        print("The current collecting function is based on capture frame by stream.")
        
        
        results = []
        dir_path = os.path.join(self.target_img_path, self.image_prefix)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        if num_im <= 0:
            try:
                i = 0
                while True:
                    i = i + 1
                    result = self.capture_frame_by_stream(i)
                    results.append(result)
                    time.sleep(time_interval)
                    
            except KeyboardInterrupt:
                print('Abort by key interrupt.')
                return results
        else:
            for i in range(num_im):
                result = self.capture_frame_by_stream(i)
                results.append(result)
                time.sleep(time_interval)
                
            return results

            