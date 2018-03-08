########################################
# gCalendar Parser and Drawer          #
# Parser code is taken from Google     #
########################################

from __future__ import print_function
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python'

import os
import sys
import json

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from datetime import datetime

# Add Parent Directory to the Path
cwd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cwd)
sys.path.append(pd)
from misc import *


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def parser():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.utcnow().isoformat() + 'Z'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    events_list = list()
    for event in events:
        event_dict = dict()
        event_dict["summary"] = event["summary"]
        try:
            start = datetime.strptime(event["start"]["date"], "%Y-%m-%d")
            end = datetime.strptime(event["end"]["date"], "%Y-%m-%d")
            event_dict["start"] = str(start.strftime("%A, %d %B"))
            event_dict["end"] = str(end.strftime("%A, %d %B"))
        except:
            try:
                start = datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S+01:00")
                end = datetime.strptime(event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S+01:00")
            except:
                start = datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S+02:00")
                end = datetime.strptime(event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S+02:00")
            event_dict["start"] = str(start.strftime("%A, %d %B %H:%M"))
            event_dict["end"] = str(end.strftime("%A, %d %B %H:%M"))
        events_list.append(event_dict)
#    events_list = json.dumps(events_list, sort_keys=False, ensure_ascii=False, indent=4)
    return events_list
    
def drawer(content):
    img = Image.new('RGBA', (650, 770), BLACK)
    draw = ImageDraw.Draw(img)
    title = "Upcoming Events"
    w = lfont(50, "b").getsize(title)[0]
    draw.text(((650-w)/2, 22), title, YELLOW, lfont(50, "b"))
    max_rows = 15
    row = 0
    for i in range(len(content)):
        draw.rectangle(((10, 100+row*40), (640, 140+row*40)), fill=YELLOW)
        draw.text((20, 5+100+row*40), content[i]["start"], BLACK, lfont(20, "b"))
        draw.text((20+300, 5+100+row*40), "-", BLACK, lfont(20, "b"))
        draw.text((20+350, 5+100+row*40), content[i]["end"], BLACK, lfont(20, "b"))
        draw.rectangle(((10, 100+(row+1.1)*40), (640, 140+(row+1.1)*40)), fill=WHITE)
        draw.text((40,5+100+(row+1.1)*40), content[i]["summary"], BLACK, lfont(20,"b"))
        row = row + 2.2
        if row > max_rows:
            break
    return img

def main():
    content = parser()
    img = drawer(content)
    img.save(cwd + "/gcalendar.png")

if __name__ == "__main__":
    main()
