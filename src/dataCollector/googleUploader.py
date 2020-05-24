import gspread
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive

class Uploader():
    def __init__(self, credential):
        self.gauth = GoogleAuth()
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credential, self.scopes)
        self.gauth.credentials = self.credentials
        self.drive = GoogleDrive(self.gauth)
        self.gsheet = gspread.authorize(self.credentials)

    def init_google_sheet(self, sheet, worksheet, columns=['image_name', 'time', 'skyDescription', 'temperature', 'temperatureDesc', 'humidity', 'windSpeed', 'system']):
        sheet = sheet.lower()
        if worksheet != 'NYC':
            worksheet = worksheet.lower()
        try:
            try:
                self.sh = self.gsheet.open(sheet)
            except:
                self.sh = self.gsheet.create(sheet)
                print("Google sheet {} does not exist, now created".format(sheet))

                try:
                    self.sh.share('liruikunbruce@gmail.com', perm_type='user', role='reader', notify=False)
                    self.sh.share('pedestriansunderwebcam@gmail.com', perm_type='user', role='reader', notify=False)
                    self.sh.share('pedestrianwebcam@modular-rex-275114.iam.gserviceaccount.com', perm_type='user', role='writer', notify=False)
                except Exception as e:
                    print('---can not share sheet to the others---')
                    print(e)
            try:
                self.ws = self.sh.worksheet(worksheet)
            except:
                self.sh.add_worksheet(title=worksheet, rows=100, cols=20)
                self.ws = self.sh.worksheet(worksheet)
                print("Worksheet {} does not exist, now created".format(worksheet))
            if self.ws.frozen_row_count == 0:
                self.ws.insert_row(columns, index=1)
                self.ws.freeze(1)
            print('google sheet {}, worksheet {} initialized'.format(sheet, worksheet))
        except Exception as e:
            print('---init google sheet failed---')
            print(e)

    def insert_to_google_sheet(self, values, sheet, worksheet, index):
        sheet = sheet.lower()
        if worksheet != 'NYC':
            worksheet = worksheet.lower()
        try:
            self.sh = self.gsheet.open(sheet)
            # for i in sh.worksheets():
            #     print(i.title)
            self.ws = self.sh.worksheet(worksheet)
            #start at 1 and 1 is col name.
            self.ws.insert_row(values, index=index+2)
            print('index {} uploaded to google sheet'.format(index))
            # return sh.url
        except Exception as e:
            print('---upload to google sheet failed---')
            print(e)

    def init_google_drive(self, city):
        
        try:
            titleList = []
            folderList = self.drive.ListFile({'q': "mimeType = 'application/vnd.google-apps.folder'"}).GetList()
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
                rawData = self.drive.CreateFile(folder_metadata)
                rawData.Upload()
                rawData_id = rawData['id']

            # Create a sub-directory
            # Make sure to assign it the proper parent ID
            if city not in titleList:
                city_folder = self.drive.CreateFile({'title': '{}'.format(city), 'mimeType' : 'application/vnd.google-apps.folder', 'parents':[{'id':rawData_id}]})
                city_folder.Upload()
                city_id = city_folder['id']

            # try:
            #     file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            #     for f in file_list:
            #         permission_list = [email['emailAddress'] for email in f.GetPermissions()]
            #         if 'pedestriansunderwebcam@gmail.com' not in permission_list:
            #             f.InsertPermission({
            #                     'type': 'user',
            #                     'value': 'pedestriansunderwebcam@gmail.com',
            #                     'role': 'reader',
            #                     'sendNotificationEmails': 'false'
            #                     })
            # except Exception as e:
            #     print('---can not init file permission---')
            #     print(e)
            print('google dirve initialized')
            return city_id
        except Exception as e:
            print('---can not create folders---')
            print(e)
        

    def upload_img_to_google_drive(self, folder_id, img, name):
        try:
            file = self.drive.CreateFile({'title':'{}'.format(name), "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
            file.SetContentFile(img)
            file.Upload()
            print('image {} uploaded'.format(img))
        except Exception as e:
            print('---can not upload {}'.format(img))
            print(e)