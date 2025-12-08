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

# Paths of files with data to work with
adressesCSV = join(path, 'workfiles/Сортированные адреса.csv')
placesCSV = join(path, 'workfiles/Реестр площадок.csv')
controllersCSV = join(path, 'Generated/УК Ульяновска.csv')

# Paths for working with unpacked .odt file
TEMPLATEpath = join(path, 'workfiles/#Шаблон Претензия в УК по МНО.odt')
ZIPpath = join(path, 'Generated/.Шаблон.zip')
DIRpath = join (path, 'Generated/.extracted/')
CONTENTpath = join(path, 'Generated/.extracted/content.xml')

# Predefining lists
retrievedAdressesLIST = []
adressFullLIST = []
adressRejectLIST = []
adressesLIST = []
placesLIST = []
rejectedPlacesLIST = []
doneList = []
controllersLIST = []

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
curAdress = None

# Functions
## Open files and make lists from them
def openFiles():
    
    with open (adressesCSV) as adressesFILE:    
        for row in csv.reader(adressesFILE, delimiter = '|'):
            adressesLIST.append(row)

    with open (placesCSV) as placesFILE:
        for row in csv.reader(placesFILE, delimiter = '|'):
            placesLIST.append(row)

    with open (controllersCSV) as controllersFILE:
        for row in csv.reader(controllersFILE, delimiter = '|', quotechar = '\''):
            controllersLIST.append(row)
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
## Unpack the template to work with it's contents
def unpackZip():
    
    # shutil.copy2(TEMPLATEpath, ZIPpath)
    with zipfile.ZipFile(ZIPpath, 'r') as zip_ref:
        zip_ref.extractall(DIRpath)