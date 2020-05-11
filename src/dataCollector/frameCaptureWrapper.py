import streamlink
import cv2
import os
from ..webcamList import webcams
from .imageCollector import imageCollector
from ..utils import times, weather, dataUtils
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
        result = []
        # image_prefix = self.image_prefix + '_stream'
        # self.init_streamlink()
        self.image_prefix = dataUtils.image_prefix_generator(self.city)
        # video_cap = cv2.VideoCapture(self.stream_url)
        if self.video_cap is None:
            print("Open webcam [%s] failed." %self.webcam_url)
            return None
        else:
            ret, frame = self.video_cap.read()
            if not ret:
                self.video_cap.release()
                try:
                    self.init_streamlink()
                except Exception as e:
                    print(e)
                    raise ValueError("Captured frame is broken.")
            else:
                print("-----------------------------------------------------")
                print("Capturing frame %d." % image_index)
                target_img_name = "{}_stream_{}.png".format(self.image_prefix, image_index)
                cv2.imwrite(os.path.join(self.target_img_path, target_img_name), frame)
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

    def capture_frame_by_stream_wrapper(self,
                                        num_im,
                                        time_interval):
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
        # if not os.path.isdir(target_img_path):
        os.makedirs(self.target_img_path, exist_ok=True)
        # print(self.target_img_path)
        if num_im <= 0:
            try:
                i = 0
                while True:
                    i = i + 1
                    result = self.capture_frame_by_stream(i)
                    dataUtils.insert_to_google_sheet(result, 'collector', self.city, index=i)
                    results.append(result)
                    time.sleep(time_interval)
                    
                    
            except KeyboardInterrupt:
                print('Abort by key interrupt.')
                self.video_cap.release()
                return results
        else:
            for i in range(num_im):
                result = self.capture_frame_by_stream(i)
                dataUtils.insert_to_google_sheet(result, 'collector', self.city, index=i)
                results.append(result)
                time.sleep(time_interval)
            
            self.video_cap.release()
            return results

            