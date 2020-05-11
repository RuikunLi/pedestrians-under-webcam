#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header
import platform

def emailNotification(city, num, time_interval, start, end, url, method, tz, path, googlesheet=None):
    sys = platform.system()
    
    try:
        sender = 'pedestriansunderwebcam@gmail.com'
        receivers = ['ruikun.li@rwth-aachen.de']  
        
        message = MIMEText(
            """
            <p> {} task finished, there are {} samples, time interval is {} minutes  </p>
            <p>Start time at webcam timezone: {} </p>
            <p>End time at webcam timezone:{} </p>
            <p> Timezone: {} </p>
            <p>Webcam url : {} </p>
            <p>Method: {}</p>
            <p>Platform: {}</p>
            <p>Stored Path: {}</p>
            <p>Google Sheet: {}</p>
                            """.format(city, num, time_interval/60, start, end, tz, url, method, sys, path, googlesheet), 'html', 'utf-8')
        
        subject = '{} task notification'.format(city)
        message['Subject'] = Header(subject, 'utf-8')

        mail = smtplib.SMTP('smtp.gmail.com',587)

        mail.ehlo()

        mail.starttls()

        mail.login('pedestriansunderwebcam@gmail.com','bruce5271527vae')

        mail.sendmail(sender, receivers, message.as_string())
    except Exception as e:
        print('---email notification sent failed---')
        print(e)
    finally:
        mail.close()
        print("Email Notification Sent")


