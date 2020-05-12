import pandas as pd
import numpy as np
import os
import datetime
import gspread
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

def init_google_drive(city):
    try:
        gauth = GoogleAuth()
        scope = ['https://www.googleapis.com/auth/drive']
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        drive = GoogleDrive(gauth)
    except Exception as e:
        print('---can not connect to google drive---')
        print(e)
    
    try:
        titleList = []
        folderList = drive.ListFile({'q': "mimeType = 'application/vnd.google-apps.folder'"}).GetList()
        for folder in folderList:
            # print('Title: %s, ID: %s' % (file['title'], file['id']))
            # Get the folder ID that you want
            if(folder['title'] == "rawData"):
                rawData_id = folder['id']
            if(folder['title'] == city):
                city_id = folder['id']
            titleList.append(folder['title'])
        if 'rawData' not in titleList:
            folder_metadata = {'title' : 'rawData', 'mimeType' : 'application/vnd.google-apps.folder'}
            rawData = drive.CreateFile(folder_metadata)
            rawData.Upload()
            rawData_id = rawData['id']

        # Create a sub-directory
        # Make sure to assign it the proper parent ID
        if city not in titleList:
            city_folder = drive.CreateFile({'title': '{}'.format(city), 'mimeType' : 'application/vnd.google-apps.folder', 'parents':[{'id':rawData_id}]})
            city_folder.Upload()
            city_id = city_folder['id']
        return city_id
    except Exception as e:
        print('---can not create folders---')
        print(e)
    try:
        
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for f in file_list:
            permission_list = [email['emailAddress'] for email in f.GetPermissions()]
            if 'pedestriansunderwebcam@gmail.com' not in permission_list:
                f.InsertPermission({
                        'type': 'user',
                        'value': 'pedestriansunderwebcam@gmail.com',
                        'role': 'reader',
                        'sendNotificationEmails': 'false'
                        })
    except Exception as e:
        print('---can not init file permission---')
        print(e)
    
        
            

def upload_img_to_google_drive(folder_id, img, name):
    try:
        gauth = GoogleAuth()
        scope = ['https://www.googleapis.com/auth/drive']
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        drive = GoogleDrive(gauth)
    except Exception as e:
        print('---can not connect to google drive---')
        print(e)
    try:
        file = drive.CreateFile({'title':'{}'.format(name), "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        file.SetContentFile(img)
        file.Upload()
        # file.InsertPermission({
        #                     'type': 'user',
        #                     'value': 'pedestriansunderwebcam@gmail.com',
        #                     'role': 'reader',
        #                     'sendNotificationEmails': 'false'
        #                     })
        # file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        # for f in file_list:
        #      f.InsertPermission({
        #                     'type': 'user',
        #                     'value': 'pedestriansunderwebcam@gmail.com',
        #                     'role': 'reader'})
    except Exception as e:
        print('---can not upload {}'.format(img))
        print(e)



def init_google_sheet(sheet, worksheet, columns=['image_name', 'time', 'skyDescription', 'temperature', 'temperatureDesc', 'humidity', 'windSpeed']):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file('client_secret.json',scopes=scopes)
        google_client = gspread.authorize(credentials)
    except Exception as e:
        print("---can not connect to google sheet---")
        print(e)
    try:
        sh = google_client.open(sheet)
    except:
        sh = google_client.create(sheet)
        print("Google sheet {} does not exist, now created".format(sheet))

        try:
            sh.share('liruikunbruce@gmail.com', perm_type='user', role='reader', notify=False)
            sh.share('pedestriansunderwebcam@gmail.com', perm_type='user', role='reader', notify=False)
            sh.share('pedestrianwebcam@modular-rex-275114.iam.gserviceaccount.com', perm_type='user', role='writer', notify=False)
        except Exception as e:
            print('---can not share sheet to the others---')
            print(e)
    try:
        ws = sh.worksheet(worksheet)
    except:
        sh.add_worksheet(title=worksheet, rows=100, cols=20)
        ws = sh.worksheet(worksheet)
        print("Worksheet {} does not exist, now created".format(worksheet))
    if ws.frozen_row_count == 0:
        ws.insert_row(columns, index=1)
        ws.freeze(1)
    
    

 
def insert_to_google_sheet(values, sheet, worksheet, index):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file('client_secret.json',scopes=scopes)
        google_client = gspread.authorize(credentials)
        sh = google_client.open(sheet)
        # for i in sh.worksheets():
        #     print(i.title)
        ws = sh.worksheet(worksheet)
        #start at 1 and 1 is col name.
        ws.insert_row(values, index=index+2)

        # return sh.url
    except Exception as e:
        print('---upload to google drive failed---')
        print(e)

    



def store_as_csv(data, dir_path, image_prefix, columns=['image_name', 'time', 'skyDescription', 'temperature', 'temperatureDesc', 'humidity', 'windSpeed']):
    try:
        df = pd.DataFrame(np.array(data), columns=columns)
        os.makedirs(dir_path + '/csvs', exist_ok=True)
        df.to_csv(path_or_buf=dir_path + "/csvs/{}.csv" .format(image_prefix))
        print('###csv stored###')
    except Exception as e:
        print('---store as csv failed---')
        print(e)

def image_prefix_generator(city):
    try:
        d = datetime.datetime.today()
        date = d.strftime('%Y-%m-%d')
        return '{}_{}'.format(city, date)
    except Exception as e:
        print('---image prefix generate failed---')
        print(e)