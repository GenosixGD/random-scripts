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

    doneList = []
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

def unpack():
    # Unpack the template to work with it's contents
    with zipfile.ZipFile(ZIPpath, 'r') as zip_ref:
        zip_ref.extractall(DIRpath)

# Compare and copy adresses with the ГИС ЖКХ registry
for item in placesLIST:
    print (item)
    spl = (item[1].split('. '))
    if (len(spl) != 2) or ('п.' in spl[0]) or ('(' in spl[1]) or (item[2] == ''):
        adressRejectLIST.append(item)
    elif (spl[0] == 'пер') or ('ул' in spl[0]):
        if item[0] == 'Ульяновск':
            retrievedAdressesLIST.append([item[1], item[2], item[3], item[4]])
        else:
            retrievedAdressesLIST.append([item[0], item[1], item[2], item[3], item[4]])
        adressFullLIST.append(item)
    else:
        adressRejectLIST.append(item)

# The actual list is being made now
notFoundAdressesLIST = []
corruptAdresses = []
curGarbageAreaList = {}
for count, item in enumerate(retrievedAdressesLIST):
    print (count, item)

    # get the adress entries from ГИС ЖКХ
    cur = 0
    stop = False
    fullStop = False
    if len(item) > 4:
        address = (item[0], + ', ' + item[1], + ', д. ' + item [2])
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

    # Получить УК дома, к которому привязана площадка
    cur2 = 0
    stop = False
    if fullStop != True:
        while stop == False:
            if not (curAdress in notFoundAdressesLIST):
                strip = curAdress[0][39:]
                split = strip.split(', д. ')
                curGarbageAreaList = {curAdress[1]: {split[0]: [split[1]]}}
                stop = True
            else:
                stop = True

    # Список домов по адресам в более удобном формате
    curStreet = {}
    houses = []
    curGarbArea = []
    curAdressesReady = []
    rember = None
    overstreet = None
    street = None
    prevstreet = None
    for item3 in curAdressesCleaned:
        counter = 0
        for subitem in item3:
            if subitem.isdigit() == False:
                counter += 1
        if counter <= 2:
            houses.append(item3)
        else:
            if ('п.' in item3) or ('д.' in item3) or ('пос.' in item3):
                overstreet = item3
                if street != None:
                    curGarbArea.append([street, houses])
            else:
                if overstreet == None:
                    if street != None:
                        prevstreet = street
                    street = item3
                else:
                    street = (overstreet + ', ' + item3)
                if prevstreet != None:
                    curGarbArea.append([prevstreet, houses])
                houses = []
                
    if (adressFullLIST[count][1] == '') and (curGarbArea == []):
        corruptAdresses.append(item)
    else:
        if adressFullLIST[count][0] == 'Ульяновск':
            garbAdressSearch = (adressFullLIST[count][1] + ', д. ' + adressFullLIST[count][2])
        else:
            garbAdressSearch = (adressFullLIST[count][0] + ', ' + adressFullLIST[count][1] + ', д. ' + adressFullLIST[count][2])
        garbAdress = (adressFullLIST[count][1] + ', ' + adressFullLIST[count][2])
        garbArea = []
        garbAreaSearch = []
        for item in curGarbArea:
            for subitem in item[1]:
                garbAreaSearch = (item[0] + ', д. ' + subitem)
                cur = 0
                stop = False
                fullStop = False
                while stop == False:
                    if garbAreaSearch in (adressesLIST[cur][0]):
                        controller = adressesLIST[cur][1]
                        if controller in curGarbageAreaList:
                            curDict = curGarbageAreaList[controller]
                        else:
                            curDict = {}
                        if item[0] in curDict:
                            curDictStreet = curDict[item[0]]
                        else:
                            curDictStreet = []
                        curDictStreet.append(subitem)
                        curDict.update({item[0]: curDictStreet})
                        curGarbageAreaList.update(curDict)
                        stop = True
                        fullStop = False
                    else:
                        cur = cur + 1
                        if cur == len(adressesLIST):
                            stop = True
                            notFoundAdressesLIST.append(item)
                            fullStop = True