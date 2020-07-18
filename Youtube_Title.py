import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
#id de la video ici
video_id = "XXXXXXXXXX"

#Identification auprès de Youtube avec votre fichier client_id.json situé dans le même dossier que le script
creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_id.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=creds)

#boucle principale (ouais c'est dégueu mais flemme de faire une interface propre)
while True :
    #récupération des infos
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    try:
        response = request.execute()
    except:
        print("FAIL READ")
        time.sleep(480)
        continue
    viewcount=response["items"][0]["statistics"]["viewCount"]
    likecount=response["items"][0]["statistics"]["likeCount"]


    #mise à jour du titre
    request = youtube.videos().update(
        part="snippet",
        body={
          "id": video_id,
          "snippet": {
            "categoryId": "28",
            "defaultLanguage": "fr",
            "description": "Description",
            "tags": [
              "Sblerky"
            ],
            "title": "La vidéo a fait "+viewcount+" vues et "+likecount+" likes."
          },
        }
    )
    try :
        response = request.execute()
        print("Ok")
    except :
        print("FAIL UPDATE")

    time.sleep(480)
