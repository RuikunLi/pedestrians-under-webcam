import os
import platform
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
# from abc import ABC, abstractmethod
import cv2
from streamlink import Streamlink
from pathlib import Path
from ..utils import weather, times, dataUtils
from .googleUploader import Uploader




# 先尝试streamlink， 不成就是用screenshot

class imageCollector(Uploader):
    def __init__(self, webcam, city):
        super().__init__('client_secrets.json')
        self.webcam = webcam #dict 
        self.city = city.split('_', 1)[0]
        self.image_prefix = city
        self.path = Path(os.getcwd())
        self.dir_path = str(self.path.parent) + '/rawData'
        self.target_img_path = os.path.join(self.dir_path, self.image_prefix)
        # self.driver_path = str(self.path) + '/webdrivers'
        self.platform = platform.system()

        self.google_drive_folder_id = self.init_google_drive(self.image_prefix)
        self.init_google_sheet('collector', self.image_prefix)

        
        try:
            city_tz = city.split('_', 1)[0]
            self.tz = times.tz_finder(city_tz)
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
        self.streams = self.session.streams(self.webcam[0])
        if self.streams is None:
            raise ValueError("cannot open the stream link %s" % self.webcam[0])
        try:
            qlist = list(self.streams.keys())
            print(qlist)
            quality = max([q for q in qlist if q[-1].lower() == 'p'])
            print('The stream quality is {}'.format(quality))
            self.stream = self.streams['%s' % quality]
            self.stream_url = self.stream.url
            self.video_cap = cv2.VideoCapture(self.stream_url)
        except Exception as e:
            print(e)
            # raise ValueError("cannot open the stream link %s" % self.webcam[0])
            try:
                quality = 'best'
                print('The stream quality is {}'.format(quality))
                self.stream = self.streams['%s' % quality]
                self.stream_url = self.stream.url
                self.video_cap = cv2.VideoCapture(self.stream_url)
            except:
                try:
                    quality = list(self.streams.keys())[0]
                    print('---can not find the best stream quality, use the first one---')
                    print('The stream quality is {}'.format(quality))
                    self.stream = self.streams['%s' % quality]
                    self.stream_url = self.stream.url
                    self.video_cap = cv2.VideoCapture(self.stream_url)
                except Exception as e:
                    print(e)
                finally:
                    raise ValueError("cannot open the stream link %s" % self.webcam[0])
        

    def init_webdriver(self):
        """
       Initialize the webdriver of Chrome by using the python lib selenium.
        
        Args:
            Void
        
        Returns:
            Void
        """
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('media.autoplay.default', 0)
        # firefox_profile.set_preference('media.autoplay.allow-muted', True)

        
        try:
            exec_path = str(self.path) + '/webdrivers/{}/geckodriver'.format(self.platform)
            print(exec_path)

            if self.platform != 'Windows':
                os.system("chmod +x {}".format(exec_path))
            
            options = FirefoxOptions()
            options.headless = True
            # options.add_argument("window-size=1920,1080")
            
            self.driver = webdriver.Firefox(firefox_profile=firefox_profile, options=options, executable_path=exec_path)
            self.driver.get(self.webcam[0])
            print(self.webcam[0])
            time.sleep(35)  # Jump over the ads
            # self.driver.maximize_window()
            try:
                fullScreenButton = self.driver.find_element_by_xpath("//*[@id='live']/div/div[2]/div[2]/div[3]/button[1]")
                fullScreenButton.click()
            except Exception as e:
                try:
                    fullScreenButton = self.driver.find_element_by_xpath("//*[@id='ecnPlayer']/div/div[1]/div[2]/div[2]/button[13]")
                    fullScreenButton.click()
                except Exception as e:
                    try:
                        fullScreenButton = self.driver.find_element_by_xpath(" //*[@id='slp-player']/div[2]/div[1]/div[3]/a[3]")
                        fullScreenButton.click()
                    except Exception as e:
                        print('--- Can not full screen---')
                        print(e)
            print('web driver is initialized')
            

        except Exception as e:
            print(e)
            print('no Firefox founded, will try Chrome')
            try:
                exec_path = str(self.path) + '/webdrivers/{}/chromedriver'.format(self.platform)
                print(exec_path)
                options = ChromeOptions()
                options.headless = True
                self.driver = webdriver.Chrome(options=options, executable_path=exec_path)  # Optional argument, if not specified will search path.
                self.driver.maximize_window()
                size = self.driver.get_window_size()
                options.add_argument("window-size={}".format(size))
                self.driver = webdriver.Chrome(options=options, executable_path=exec_path)
                print('web driver is initialized')
            except:
                raise EnvironmentError("---No webdriver founded---")

       

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