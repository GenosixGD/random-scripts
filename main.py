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
notFoundAdressesLIST = []

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
    
adressesLIST = []
adressesCSV = join(path, 'workfiles/Сортированные адреса.csv')
with open (adressesCSV) as adressesFILE:
    for row in csv.reader(adressesFILE, delimiter = '|'):
        adressesLIST.append(row)

placesLIST = []
placesCSV = join(path, 'workfiles/Реестр площадок.csv')
with open (placesCSV) as placesFILE:
    for row in csv.reader(placesFILE, delimiter = '|'):
        placesLIST.append(row)


controllersCSV = join(path, 'Generated/УК Ульяновска.csv')
with open (controllersCSV) as controllersFILE:
    controllersLIST = []
    for row in csv.reader(controllersFILE, delimiter = '|', quotechar = '\''):
        controllersLIST.append(row)

content = None
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

#for item in adressFullLIST:
    #print(item)

# The actual list is being made now
for count, item in enumerate(retrievedAdressesLIST):
    cur = 0

    stop = False
    # get the adress entries from ГИС ЖКХ
    while stop == False:
        if item in ((adressesLIST[cur])[0]):
            curAdress = adressesLIST[cur]
            stop = True
            fullStop = False
        else:
            cur = cur + 1
            if cur == len(adressesLIST):
                stop = True
                notFoundAdressesLIST.append(item)
                fullStop = True

    # Получить всю информацию об УК дома, к которому привязана площадка, из списка УК
    cur2 = 0
    stop = False
    if fullStop != True:
        while stop == False:
            if not (curAdress in notFoundAdressesLIST):
                if curAdress[1] in (controllersLIST[cur2])[0]:
                    curController = []
                    curController = (controllersLIST[cur2])
                    stop = True
                else:
                    cur2 = cur2 + 1
                    if cur2 == len(controllersLIST):
                        stop = True
            else:
                stop = True

        curGarbageAreaList = {}
        curGarbageAreaList.update({curController[0]: [item.replace('Ульяновская обл, г. Ульяновск, ', '')]})

    # Разобрать список остальных домов площадки на читаемый список
    fullStop = False
    stop = False
    curAdresses = (adressFullLIST[count])[4]
    curAdressesStrip = [item.strip() for item in curAdresses.split(',')]
    curAdressesWithEmpties = []
    for item in curAdressesStrip:
        if 'дом' in item:
            item2 = (item.split(" "))[1]
            curAdressesWithEmpties.append(item2.strip())
        elif 'д. ' in item:
            item2 = (item.split(". "))[1]
            curAdressesWithEmpties.append(item2.strip())
        else:
            curAdressesWithEmpties.append(item.strip())
    for item in curAdressesWithEmpties:
        if item == '':
            curAdressesWithEmpties.remove(item)

    # Сделать машиночитаемый список из полученного выше списка
    curAdressesReady = []
    for item in curAdressesWithEmpties:
        curStreet = {}
        houses = []
        curGarbArea = []
        counter = 0
        rember = None
        for subitem in item:
            for supersubitem in list(subitem):
                if supersubitem.isdigit == False:
                    counter += 1
            if counter >= 3:
                curStreet.update({'street': subitem})
            elif counter < 3:
                if rember != curStreet:
                    curStreet.update({'houses': houses})
                    curGarbArea.append(curStreet)
                    houses = []
                houses.append(subitem)
                rember = curStreet
        curGarbAreaReady = []
        print (curGarbArea)