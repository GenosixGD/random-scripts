import os
import shutil
import zipfile
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from os.path import join

path = os.path.dirname(__file__)

# Paths for working with unpacked .odt file
ZIPpath = join(path, 'Generated/.Шаблон.zip')
DIRpath = join (path, 'Generated/.extracted/')

# Predefining lists
retrievedAdressesLIST = []
adressFullLIST = []
adressRejectLIST = []
rejectedPlacesLIST = []
doneList = []

# Variables to work with Google Sheets API
## If modifying these scopes, delete the file token.json.
Scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SpreadSheetID = "17r_g5ROMUXcHUhdpB508hFZyXpOXV5UC8UYglVHeNsQ"
SheetsRange = "A2:G"
tokenf = os.path.join (path, "token.json")
credsf = os.path.join (path, "credentials.json")

# Variables to work with data searching
cur = 0
stop = False
fullStop = False
stop2 = False

# Open files and make lists from them
    
adressesCSV = join(path, 'workfiles/Сортированные адреса.csv')
with open (adressesCSV) as adressesFILE:
    adressesLIST = []
    for row in csv.reader(adressesFILE, delimiter = '|'):
        adressesLIST.append(row)

placesCSV = join(path, 'workfiles/Реестр площадок.csv')
with open (placesCSV) as placesFILE:
    placesLIST = []
    for row in csv.reader(placesFILE, delimiter = '|'):
        placesLIST.append(row)

controllersCSV = join(path, 'Generated/УК Ульяновска.csv')
with open (controllersCSV) as controllersFILE:
    controllersLIST = []
    for row in csv.reader(controllersFILE, delimiter = '|', quotechar = '\''):
        controllersLIST.append(row)

contentXML = join(path, 'Generated/.extracted/content.xml')
with open (contentXML) as contentFILE:
    content = (contentFILE.readlines())[1]
        
## Получить таблицу претензий
def googleSheetGet():

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(tokenf):
        creds = Credentials.from_authorized_user_file(tokenf, Scopes)

    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credsf, Scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run

        with open(tokenf, "w") as token:
            token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)
        except HttpError as err:
            exit(err)

        # Call the Sheets API

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SpreadSheetID, range=SheetsRange)
            .execute()
        )
        values = result.get("values", [])

        for row in values:
            if row[0] != "":
                doneList.append({"address": row[0], "controller": row[1], "houses": row[2], "ready": row[3], "printed": row[4], "fileName": row[5], "allHouses": row[6]})

# Unpack the template to work with it's contents
with zipfile.ZipFile(ZIPpath, 'r') as zip_ref:
    zip_ref.extractall(DIRpath)










# Compare and copy adresses with the ГИС ЖКХ registry
for item in placesLIST:
    spl = (item[1].split('. '))
    if (len(spl) != 2) or ('п.' in spl[0]) or ('(' in spl[1]) or (item[2] == ''):
        adressRejectLIST.append(item)
    elif (spl[0] == 'пер') or ('ул' in spl[0]):
        if item[0] == 'Ульяновск':
            adress = ('Ульяновская обл, г. Ульяновск, ' + item[1] + ', д. ' + item[2])
        else:
            adress = ('Ульяновская обл, г. Ульяновск, ' + item[0] + ', ' + item[1] + ', д. ' + item[2])
        retrievedAdressesLIST.append(adress)
        adressFullLIST.append(item)

# The actual list is being made now
for item in retrievedAdressesLIST:
    cur = 0

    while stop == False:
        if item in (adressesLIST[cur])[0]:
            curAdress = adressesLIST[cur]
            stop = True
            stop2 == True
        else:
            cur = cur + 1
            if cur == len(adressesLIST):
                stop = True
                stop2 = True
    cur2 = 0
    stop = False
    if stop2 == False:
        while stop == False:
            if curAdress[1] in (conrollersLIST[cur2])[0]:
                curController = []
                curController.append(controllersLIST[1], controllersLIST[2], controllersLIST[3], controllersLIST[4])
                stop = True
            else:
                cur2 = cur2 + 1
        stop = False

    