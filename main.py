import os
import relatorio
import csv
import shutil
import zipfile

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from os.path import join

# If modifying these scopes, delete the file token.json.
Scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SpreadSheetID = "17r_g5ROMUXcHUhdpB508hFZyXpOXV5UC8UYglVHeNsQ"
Range = "A2:G"

path = os.path.dirname(__file__)
tokenf = os.path.join (path, "token.json")
credsf = os.path.join (path, "credentials.json")
doneList = []

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
      flow = InstalledAppFlow.from_client_secrets_file(
          credsf, Scopes
      )
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run

    with open(tokenf, "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
  except HttpError as err:
    print(err)
    exit(2)

  # Call the Sheets API

  sheet = service.spreadsheets()
  result = (
      sheet.values()
      .get(spreadsheetId=SpreadSheetID, range=Range)
      .execute()
  )
  values = result.get("values", [])

  for row in values:
    if not (row[0] == ""):
      doneList.append({"address": row[0], "controller": row[1], "houses": row[2], "ready": row[3], "printed": row[4], "fileName": row[5], "allHouses": row[6]})

### googleSheetGet()

TEMPLATEpath = join(path, 'workfiles/#Шаблон Претензия в УК по МНО.odt')
ZIPpath = join(path, 'Generated/.Шаблон.zip')
DIRpath = join (path, 'Generated/.extracted/')

def unpackZip():
  shutil.copy2(TEMPLATEpath, ZIPpath)
  with zipfile.ZipFile(ZIPpath, 'r') as zip_ref:
      zip_ref.extractall(DIRpath)

CONTENTpath = join(path, 'Generated/.extracted/content.xml')

# Read in the file
with open(CONTENTpath, 'r') as CONTENT:
  CONTENTdata = CONTENT.read()

# Replace the target string
CONTENTdata = CONTENTdata.replace('[#ИНН]', INN)

# Write the file out again
with open(CONTENTpath, 'w') as CONTENT:
  CONTENT.write(CONTENTdata)
