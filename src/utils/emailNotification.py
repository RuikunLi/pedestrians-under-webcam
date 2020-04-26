#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header

def emailNotification(prefix, num, time_interval):
    
    try:
        sender = 'pedestriansunderwebcam@gmail.com'
        receivers = ['ruikun.li@rwth-aachen.de']  
        
        message = MIMEText("{} task finished, there are {} samples, time interval is {} minutes".format(prefix, num, time_interval/60), 'plain', 'utf-8')
        
        subject = '{} task finished notification'.format(prefix)
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


