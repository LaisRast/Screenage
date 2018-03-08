########################################
# VBB Parser and Drawer                #
########################################

import os
import sys
import json
import requests

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from datetime import datetime
from configparser import ConfigParser
from math import ceil

# Add Parent Directory to the Path
cwd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cwd)
sys.path.append(pd)
from misc import *


def icon(icon_code):
    return Image.open(cwd + "/icons/" + icon_code + ".png")

def remain(time):
    now = datetime.now().replace(second=0)
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000+01:00")
    if time <= now:
        remain_minuts = 0
    else:
        remain = time - now
        remain_minuts = ceil(remain.seconds/60)
    return str(remain_minuts) + " min(s)"
    
def get_stations(lat, lng, station_num=2):
    url = "https://2.vbb.transport.rest/stations/nearby?latitude={}&longitude={}"
    response = requests.get(url.format(lat, lng))
    content = response.json()
    stations = dict()
    if station_num > len(content):
        station_num = len(content)
    for i in range(station_num):
        stations[content[i]['name']] = content[i]['id']
    return stations

def station_departures(station_id, station_name, depatures_num=6):
    url = "https://2.vbb.transport.rest/stations/%s/departures?duration=30"
    response = requests.get(url % (station_id))
    content = response.json()
    station_departures = {'station': station_name, "depatures": list()}
    if depatures_num > len(content):
        depatures_num = len(content)
    for i in range(depatures_num):
#        if content[i]['station']['name'] == station_name:
            depature = dict()
            depature["product"] = content[i]['line']['product']
            if depature["product"] == "bus":
                depature["name"] = content[i]['line']['name'][4:]
            elif depature["product"] == "tram":
                depature["name"] = content[i]['line']['name'][5:]
            else:
                depature["name"] = content[i]['line']['name']
            depature["direction"] = content[i]['direction']
            depature["time"] = str(datetime.strptime(content[i]['when'], "%Y-%m-%dT%H:%M:%S.000+01:00"))
            depature["remain"] = remain(content[i]['when'])
            station_departures["depatures"].append(depature)
#        else:
#            pass
    return station_departures

def drawer(content):
    img = Image.new('RGBA', (500, 770), BLACK)
    draw = ImageDraw.Draw(img)
    title = "Traffic Information"
    w = lfont(50, "b").getsize(title)[0]
    draw.text(((500-w)/2, 22), title, YELLOW, lfont(50, "b"))
    header = "Type           Direction                                    Remain"
    draw.text((15, 110), header, WHITE, lfont(20, "b"))
    max_rows = 15
    row = 0
    for i in range(len(content)):
        draw.rectangle(((10, 145+row*40), (490, 185+row*40)), fill=BLUE)
        w1 = lfont(23, "b").getsize(content[i]["station"])[0]
        draw.text(((500-w1)/2, 150+row*40), content[i]["station"], WHITE, lfont(23, "b"))
        row = row + 1.1
        if row > max_rows:
            break
        deps = content[i]["depatures"]
        for j in range(len(deps)):
            draw.rectangle(((10, 145+row*40), (490, 185+row*40)), fill=YELLOW)
            draw.text((50, 150+row*40), deps[j]["name"], BLACK, lfont(20, "b"))
            if len(deps[j]["direction"]) > 27:
                deps[j]["direction"] = deps[j]["direction"][:24] + '..'
            draw.text((115, 150+row*40), deps[j]["direction"], BLACK, lfont(20, "b"))
            draw.text((400, 150+row*40), deps[j]["remain"], BLACK, lfont(20, "b"))
            icon_small = icon(deps[j]["product"]).resize((30, 30), Image.ANTIALIAS)
            img.paste(icon_small, (17, 150+int(row*40)), icon_small)
            row = row + 1.1
            if row > max_rows:
                break
    return img

def main():
    depatures = list()
    stations = get_stations(lat, lng)
    for key in stations:
        depatures.append(station_departures(stations[key], key))
#    depatures = json.dumps(depatures, sort_keys=False, ensure_ascii=False, indent=4)
    img = drawer(depatures)
    img.save(cwd + "/vbb.png")

if __name__ == "__main__":
    config = ConfigParser()
    config.read(pd + '/config.ini')
    lat = config['location']['lat']
    lng = config['location']['lng']
    main()
