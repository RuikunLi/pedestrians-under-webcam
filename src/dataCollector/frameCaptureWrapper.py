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
        # self.init_streamlink()

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
        self.init_streamlink()
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
                except:
                    try:
                        self.video_cap.release()
                        self.init_streamlink()
                    except Exception as e:
                        print(e)
                        raise ValueError("Captured frame is broken.")
            else:
                print("-----------------------------------------------------")
                print("Capturing frame %d." % image_index)
                target_img_name = "{}_stream_{}_{}.png".format(self.image_prefix, self.platform, image_index)
                cv2.imwrite(os.path.join(self.target_img_path, target_img_name), frame)
                self.upload_img_to_google_drive(self.google_drive_folder_id, os.path.join(self.target_img_path, target_img_name), target_img_name)
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
                for func in [result.append(target_img_name),
                        result.append(current_time),
                        result.extend(current_weather),
                        result.append(self.platform)  ]

                try:
                    func()
                except Exception as e:
                    print('---can not get result---')
                    print(e)

                self.video_cap.release()


                return result

    def capture_frame_by_stream_wrapper(self,
                                        num_im,
                                        time_interval,
                                        bsize=10):
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
        # if total time in min bigger than 100 mins 
        if (num_im-1) * time_interval/60 >=  100 or num_im >= 100:
            print("time range is too long or the num of images is too big , will take batch， batch size is {}".format(bsize))
            b = 0
            for batch in range(0, num_im, bsize):
                vars()['batch_'+str(b)] = [i for i in range(num_im)][batch:batch+bsize]
                indexes = eval('batch_'+str(b))
                print("The current batch is " + str(indexes))
                for i in indexes:
                    result = self.capture_frame_by_stream(i) 
                    self.insert_to_google_sheet(result, 'collector', self.city, index=i)
                    results.append(result)
                    time.sleep(time_interval)
                b = b + 1     

            return results
        elif num_im <= 0:
            try:
                i = 0
                while True:
                    i = i + 1
                    result = self.capture_frame_by_stream(i)
                    self.insert_to_google_sheet(result, 'collector', self.city, index=i)

                    results.append(result)
                    time.sleep(time_interval)
                    
            except KeyboardInterrupt:
                print('Abort by key interrupt.')
                self.video_cap.release()
                return results
        else:
            for i in range(num_im):
                    result = self.capture_frame_by_stream(i)
                    self.insert_to_google_sheet(result, 'collector', self.city, index=i)

                    results.append(result)
                    time.sleep(time_interval)
            # self.video_cap.release()
            return results

            