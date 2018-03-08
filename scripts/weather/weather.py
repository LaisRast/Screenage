########################################
# Weather Parser and Drawer            #
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

# Add Parent Directory to the Path
cwd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cwd)
sys.path.append(pd)
from misc import *


def icon(icon_code):
    return Image.open(cwd + "/icons/" + icon_code + ".png")

def parser():
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=Metric"
    response = requests.get(url.format(lat, lng, API_key))
    content = response.json()
    weather = dict()
    weather["time"] = str(datetime.now())
    weather["location"] = content["name"]
    weather["temp"] = str(round(content["main"]["temp"])) + "°"
    weather["pressure"] = str(content["main"]["pressure"])
    weather["humidity"] = str(content["main"]["humidity"])
    weather["wind_speed"] = str(content["wind"]["speed"])
    weather["short_desc"] = str(content["weather"][0]["main"])
    weather["description"] = content["weather"][0]['description']
    weather["icon"] = content["weather"][0]["icon"]
#    weather = json.dumps(weather, sort_keys=False, ensure_ascii=False, indent=4)
    return weather

def drawer(content):
    img = Image.new('RGBA', (300, 120), BLACK)
    draw = ImageDraw.Draw(img)
    icon_main = icon(content["icon"]).convert("RGBA").resize((125,125), Image.ANTIALIAS)
    img.paste(icon_main, (0, 0), icon_main)
    w1 = lfont(80, "l").getsize(content["temp"])[0]
    draw.text((100+(200-w1)/2, 0), content["temp"], WHITE, lfont(80, "l"))
    w2 = lfont(30, "b").getsize(content["short_desc"].title())[0]
    draw.text((100+(200-w2)/2, 85), content["short_desc"].title(), WHITE, lfont(30, "b"))
    return img

def main():
    content = parser()
    img = drawer(content)
    img.save(cwd + "/weather.png")

if __name__ == "__main__":
    config = ConfigParser()
    config.read(pd + '/config.ini')
    API_key = config['weather']['api_key']
    lat = config['location']['lat']
    lng = config['location']['lng']
    main()
