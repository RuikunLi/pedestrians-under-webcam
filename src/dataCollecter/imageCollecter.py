import os
from selenium import webdriver
import time
from abc import ABC, abstractmethod
import cv2
from streamlink import Streamlink

from ..utils import weather, times



# 先尝试streamlink， 不成就是用screenshot

class imageCollector(ABC):
    def __init__(self, webcam_url, city, image_prefix):
        self.webcam_url = webcam_url
        self.city = city
        self.image_prefix = image_prefix
        self.target_img_path = os.getcwd() + '/rawData'
        try:
            self.tz = times.tz_finder(city)
        except:
            print('### time zone is None, therefore use utc time###')
        try:
            self.init_streamlink(self.image_prefix)
        except:
            print('Streamlink not avaliable, now use screenshot method')
            self.init_webdriver(self.image_prefix)

    def init_streamlink(self, image_prefix='stream'):
        self.image_prefix = image_prefix
        self.session = Streamlink()
        self.session.set_option("http-headers", "User-Agent=Mozilla/5.0 (Windows NT 10.0 Win64 x64 rv:72.0) Gecko/20100101 Firefox/72.0")
        self.streams = self.session.streams(self.webcam_url)
        if self.streams is None:
            raise ValueError("cannot open the stream link %s" % self.webcam_url)

        q = list(self.streams.keys())[0]
        self.stream = self.streams['%s' % q]
        self.stream_url = self.stream.url
        

    def init_webdriver(self, image_prefix='screenshot'):
        """
       Initialize the webdriver of Chrome by using the python lib selenium.
        
        Args:
            Void
        
        Returns:
            Void
        """
		
        self.image_prefix = image_prefix
        self.driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        self.driver.get(self.webcam_url)
        time.sleep(15)  # Jump over the ads

    @abstractmethod
    def capture_frame_by_stream_wrapper(self, image_prefix,
                                        num_im,
                                        time_interval):
        print('abstract method')