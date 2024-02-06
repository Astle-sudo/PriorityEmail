import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class Email :
  
  def __init__(self, snippet=None, From=None, Subject=None) :
    self.summary = snippet
    self.sender = From
    self.subject = Subject
    self.rank = 0

def extractEmails(N=3):

  def getInfo (mes) :
    e = Email()
    e.summary = mes.execute()['snippet']
    for i in mes.execute()["payload"]["headers"]:
      if i['name'] == 'From' :
        e.sender = i["value"]
      if i['name'] == 'Subject' :
        e.subject = i["value"]
    return e

  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=N).execute()
    labels = results.get("messages", [])

    emails = list()
    for info in labels :
      mes = service.users().messages().get(userId="me", id=str(info['id']))
      emails.append(getInfo(mes))
    
    return emails

  except HttpError as error:
    print(f"An error occurred: {error}")



