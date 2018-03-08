########################################
# Forecast Parser and Drawer           #
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

def wallpaper(wallpaper_code):
    return Image.open(cwd + "/wallpapers/" + wallpaper_code + ".jpg")

def parser_weather():
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
    weather["city"] = content["name"]
#    weather = json.dumps(weather, sort_keys=False, ensure_ascii=False, indent=4)
    return weather

def parser_forecast():
    url = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=Metric'
    response = requests.get(url.format(lat, lng, API_key))
    content = response.json()
    forecast = list()
    lists = content["list"]
    for i in range(len(lists)):
        weather = dict()
        time = datetime.strptime(lists[i]["dt_txt"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        if time.day != now.day and time.hour == 12:
            weather["datetime"] = str(time)
            weather["day_name"] = str(time.strftime("%A"))
            weather["temp"] = str(round(lists[i]["main"]["temp"])) + "°"
            weather["pressure"] = str(lists[i]["main"]["pressure"])
            weather["humidity"] = str(lists[i]["main"]["humidity"])
            weather["wind_speed"] = str(lists[i]["wind"]["speed"])    
            weather["short_desc"] = str(lists[i]["weather"][0]["main"])
            weather["description"] = lists[i]["weather"][0]['description']
            weather["icon"] = lists[i]["weather"][0]["icon"]
            forecast.append(weather)
        else:
            pass
#    forecast = json.dumps(forecast, sort_keys=False, ensure_ascii=False, indent=4)
    return forecast

def drawer(weather, forecast):
    img = Image.new('RGBA', (650, 370), BLACK)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 125), (650, 130)), fill=YELLOW)
    draw.text((15, 20), "Current", GREY, lfont(16, "b"))
    draw.text((15, 50), weather["temp"], WHITE, lfont(50, "l"))
    w = lfont(16, "b").getsize(weather["short_desc"])[0]
    draw.text(((120-w)/2+120, 20), weather["short_desc"].title(), WHITE, lfont(16, "b"))
    icon_main = icon(weather["icon"]).convert("RGBA").resize((75, 75), Image.ANTIALIAS)
    img.paste(icon_main, (138, 40), icon_main)
    for i in range(4):
        draw.rectangle(((230+i*100, 15), (231+i*100, 115)), fill=GREY)
        w1 = lfont(16, "b").getsize(forecast[i]["day_name"])[0]
        draw.text((230+i*100+(100-w1)/2, 20), forecast[i]["day_name"], GREY, lfont(16, "b"))
        w2 = lfont(20, "b").getsize(forecast[i]["temp"])[0]
        draw.text((230+i*100+(100-w2)/2, 95), forecast[i]["temp"], WHITE, lfont(20, "b"))
        icon_small = icon(forecast[i]["icon"]).convert("RGBA").resize((50, 50), Image.ANTIALIAS)
        img.paste(icon_small, (255+i*100, 40), icon_small)
    wall = wallpaper(weather["icon"]).resize((650, 366))
    img.paste(wall, (0, 130))
    draw.text((10, 340), weather["city"], WHITE, lfont(20, "l"))
    return img

def main():
    content_weather = parser_weather()
    content_forecast = parser_forecast()
    img = drawer(content_weather, content_forecast)
    img.save(cwd + "/forecast.png")
    
if __name__ == "__main__":
    config = ConfigParser()
    config.read(pd + '/config.ini')
    API_key = config['weather']['api_key']
    lat = config['location']['lat']
    lng = config['location']['lng']
    main()
