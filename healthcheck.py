#!/usr/bin/python3
import subprocess
import httplib2
import os
import sys
import time
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

now = datetime.utcnow()
start_time = now + timedelta(minutes=2)
start_time_iso = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
command_stop = "sudo systemctl stop surfcam.service"
command_start = "sudo systemctl start surfcam.service"
CLIENT_SECRETS_FILE = "/surf/client_secrets.json"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the Developers Console
https://console.developers.google.com/
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_SCOPE)

storage = Storage("/surf/main.py-oauth2.json")
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

request = youtube.liveBroadcasts().list(
        part="status",
        broadcastStatus="active",
        broadcastType="all"
    )
response = request.execute()
print(response)
if response['items']:
    if response['items'][0]['status']['lifeCycleStatus'] == "live":
        print("running")
        pass
else:
    print("dead")
    stop = subprocess.run(command_stop, shell=True, text=True, capture_output=True)
    print(stop.stdout)
    time.sleep(15)
    print("starting stream")

    stream = youtube.liveStreams().insert(
        part="snippet,cdn",
        body={
            "snippet": {
                "title": "Campus Point Surf Cam",
                "description": "Campus Point Surf Cam"
            },
            "cdn": {
                "resolution": "1440p",
                "frameRate": "30fps",
                "ingestionType": "rtmp"
            }
        }
    ).execute()

    time.sleep(30)
    start = subprocess.run(command_start, shell=True, text=True, capture_output=True)
    print(start.stdout)
    
    # Check if the stream is active
    stream_status = youtube.liveStreams().list(
        part="status",
        id=stream["id"]
    ).execute()['items'][0]['status']['streamStatus']

    if stream_status == "active":
        # Bind the broadcast to the stream
        bind_broadcast = youtube.liveBroadcasts().bind(
            part="id,contentDetails",
            id=broadcast["id"],
            streamId=stream["id"]
        ).execute()

        # Transition the broadcast to live
        transition_broadcast = youtube.liveBroadcasts().transition(
            broadcastStatus="live",
            id=broadcast["id"],
            part="id,contentDetails"
        ).execute()

print("done")
