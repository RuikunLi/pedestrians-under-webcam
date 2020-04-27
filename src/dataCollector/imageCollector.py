import os
import platform
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
import time
from abc import ABC, abstractmethod
import cv2
from streamlink import Streamlink
from pathlib import Path
from ..utils import weather, times, dataUtils




# 先尝试streamlink， 不成就是用screenshot

class imageCollector(ABC):
    def __init__(self, webcam_url, city):
        self.webcam_url = webcam_url
        self.city = city
        self.image_prefix = dataUtils.image_prefix_generator(city)
        self.path = Path(os.getcwd())
        self.target_img_path = str(self.path.parent) + '/rawData'
        # self.driver_path = str(self.path) + '/webdrivers'
        self.platform = platform.system()

        try:
            self.tz = times.tz_finder(city)
        except:
            print('### time zone is None, therefore use utc time###')
        # try:
        #     self.init_streamlink(self.image_prefix)
        # except:
        #     print('Streamlink not avaliable, now use screenshot method')
        #     # self.init_webdriver(self.image_prefix)
        # try:
        #     self.init_webdriver(self.image_prefix)
        # except:
        #     pass

    def init_streamlink(self):
        self.session = Streamlink()
        self.session.set_option("http-headers", "User-Agent=Mozilla/5.0 (Windows NT 10.0 Win64 x64 rv:72.0) Gecko/20100101 Firefox/72.0")
        self.streams = self.session.streams(self.webcam_url)
        if self.streams is None:
            raise ValueError("cannot open the stream link %s" % self.webcam_url)

        q = list(self.streams.keys())[0]
        self.stream = self.streams['%s' % q]
        self.stream_url = self.stream.url
        

    def init_webdriver(self):
        """
       Initialize the webdriver of Chrome by using the python lib selenium.
        
        Args:
            Void
        
        Returns:
            Void
        """
		
        self.image_prefix = self.image_prefix + '_' + image_prefix
        try:
            options = ChromeOptions()
            options.headless = True
            self.driver = webdriver.Chrome(options=options, executable_path='./webdrivers/{}/chromedriver'.format(self.platform))  # Optional argument, if not specified will search path.
            self.driver.maximize_window()
            size = self.driver.get_window_size()
            options.add_argument("window-size={}".format(size))
            self.driver = webdriver.Chrome(options=options, executable_path='./webdrivers/{}/chromedriver'.format(self.platform))
            print('web driver is initialized')

        except:
            print('no Chrome founded, will try another browser')
            try:
                options = FirefoxOptions()
                options.headless = True
                # options.add_argument("window-size=1920,1080")
                self.driver = webdriver.Firefox(options=options, executable_path='./webdrivers/{}/geckodriver'.format(self.platform))
                self.driver.Manage().Window.Maximize()
                print('web driver is initialized')
            except:
                pass

        self.driver.get(self.webcam_url)
        time.sleep(15)  # Jump over the ads

    # @abstractmethod
    # def capture_frame_by_stream_wrapper(self, image_prefix,
    #                                     num_im,
    #                                     time_interval):
    #     print('abstract method')

    # @abstractmethod
    # def capture_frame_by_screenshot_wrapper(self, image_prefix,
    #                                     num_im,
    #                                     time_interval):
    #     print('abstract method')