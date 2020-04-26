#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header

def emailNotification(prefix, num, time_interval, start, end, url, method):
    
    try:
        sender = 'pedestriansunderwebcam@gmail.com'
        receivers = ['ruikun.li@rwth-aachen.de']  
        
        message = MIMEText(
            """
            <p> {} task finished, there are {} samples, time interval is {} minutes  </p>
            <p>start time at webcam timezone: {} </p>
            <p>end time at webcam timezone:{} </p>
            <p>webcam url : {} </p>
            <p>method: {}</p>
                            """.format(prefix, num, time_interval/60, start, end, url, method), 'html', 'utf-8')
        
        subject = '{} task notification'.format(prefix)
        message['Subject'] = Header(subject, 'utf-8')

        mail = smtplib.SMTP('smtp.gmail.com',587)

        mail.ehlo()

        mail.starttls()

        mail.login('pedestriansunderwebcam@gmail.com','bruce5271527vae')

        mail.sendmail(sender, receivers, message.as_string())
    except Exception as e:
        print(e)
    finally:
        mail.close()
        print("Email Notification Sent")


