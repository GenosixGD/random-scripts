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
adressRejectLIST = []
adressRejectLIST2 = []
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
    spl = (item[1].split('. '))
    if (spl[0] == 'пер') or ('ул' in spl[0]) or ('пр-кт' in spl[0]):
        retrievedAdressesLIST.append(item)
    elif (len(spl) != 2) or ('п.' in spl[0]) or ('(' in spl[1]) or (item[2] == ''):
        adressRejectLIST.append(item)
    else:
        adressRejectLIST.append(item)

# The actual list is being made now
notFoundAdressesLIST = []
corruptAdresses = []
curGarbageAreaList = {}
for count, item in enumerate(retrievedAdressesLIST):
    REJECT = False
    
    # Список домов по адресам в более удобном формате
    curStreet = {}
    houses = []
    curGarbArea = []
    curAdressesReady = []
    split = []
    strip = []
    anotherList = []
    curList = []
    prev = None
    overstreet = None
    street = None
    prevstreet = None
    for subitem in item[4].split(', '):
        split.append(subitem)
    for subitem in split:
        strip.append(subitem.strip())
    for subitem in strip:
        itemSplit = subitem.split(' ')
        digit = False
        for ssubitem in itemSplit:
            if  (('ул.' in ssubitem) or ('пер.'  in ssubitem) or ('б-р'  in ssubitem) or ('п.'  in ssubitem) or ('д.'  in ssubitem) or ('пос.'  in ssubitem) or ('с.'  in ssubitem)):
                prev = ssubitem
            if subitem.isdigit:
                digit = True
                curList.append(ssubitem)
            if (ssubitem == 'дома') or (ssubitem == 'дом'):
                pass
            else:
                print (prev)
                if prev != None:
                    curList.append((prev + ' ' + ssubitem))
                    prev = None
                    print (curList)
                else:
                    curList = (curList + ssubitem)
        if REJECT == True:
            break
        anotherList.append(curList)
    if REJECT == True:
        continue
    #print (anotherList)



    for subitem in split:
        counter = 0
        for symbol in subitem:
            if symbol.isdigit() == False:
                counter += 1
        if counter <= 2:
            houses.append(subitem)
        else:
            if ('п.' in subitem) or ('д.' in subitem) or ('пос.' in subitem) or ('с.' in subitem):
                overstreet = subitem.strip()
                if street != None:
                    curGarbArea.append([street, houses])
            elif ('дома' in subitem) or ('дом' in subitem):
                houses.append(subitem)
            else:
                if overstreet == None:
                    if street != None:
                        prevstreet = street
                    street = subitem
                else:
                    street = (overstreet + ', ' + subitem)
                if prevstreet != None:
                    curGarbArea.append([prevstreet, houses])
                houses = []
    if (item[1] == '') and (curGarbArea == []):
        corruptAdresses.append(item)
    else:
        if item[0] == 'Ульяновск':
            garbAdressSearch = (item[1] + ', д. ' + item[2])
        else:
            garbAdressSearch = (item[0] + ', ' + item[1] + ', д. ' + item[2])
        garbAdress = (item[1] + ', ' + item[2])
        garbArea = []
        garbAreaSearch = []
        for item4 in curGarbArea:
            for subitem4 in item4[1]:
                garbAreaSearch = (item4[0] + ', д. ' + subitem4)
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
                        if item4[0] in curDict:
                            curDictStreet = curDict[item4[0]]
                        else:
                            curDictStreet = []
                        curDictStreet.append(subitem4)
                        curDict.update({item4[0]: curDictStreet})
                        curGarbageAreaList.update(curDict)
                        stop = True
                        fullStop = False
                    else:
                        cur = cur + 1
                        if cur == len(adressesLIST):
                            stop = True
                            notFoundAdressesLIST.append(item4)
                            fullStop = True