########################################
# RSS_TS Parser and Drawer             #
########################################

import os
import sys
import json
import requests
import feedparser

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from io import BytesIO

# Add Parent Directory to the Path
cwd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cwd)
sys.path.append(pd)
from misc import *


def img_get(url):
    if url is None:
        return Image.open(cwd + "/no_img.jpeg")
    img_response = requests.get(url)
    return Image.open(BytesIO(img_response.content))

def parser():
    ts_rss = "http://www.tagesspiegel.de/contentexport/feed/berlin"
    feed = feedparser.parse(ts_rss)
    content = list()
    for item in feed.get("items"):
        item_dict = dict()
        item_dict["title"] = item["title"]
        item_dict["description"] = item["description"]
        item_dict["link"] = item["link"]
        item_dict["image"] = (item.enclosures[0].href)[:-5] + "15.jpg"
        content.append(item_dict)
#    content = json.dumps(content, sort_keys=False, ensure_ascii=False, indent=4)
    return content
    
def drawer(img, title, description):
    img = img.resize((747, 441)).convert("RGBA")
    rect = Image.new("RGBA", img.size, NOCOLOR)
    draw_rect = ImageDraw.Draw(rect)
    draw_rect.rectangle(((0, 250), img.size), fill=TBLACK)
    img = Image.alpha_composite(img, rect)
    draw = ImageDraw.Draw(img)
    title_font = lfont(30, "b")
    w = title_font.getsize(title)[0]
    if len(title) > 50:
        w1 = title_font.getsize(title[:40])[0]
        draw.text(((747-w1)/2, 250), title[:40], YELLOW, title_font)
        w2 = title_font.getsize(title[40:])[0]
        draw.text(((747-w2)/2, 280), title[40:], YELLOW, title_font)
    else:
        draw.text(((747-w)/2, 260), title, YELLOW, title_font)
    desc_font = lfont(25, "r")
    desc_list = text_wrap(description, 57)
    for i in range(len(desc_list)):
        line = desc_list[i]
        w = desc_font.getsize(line)[0]
        draw.text(((747 - w)/2, 320+i*28), line, WHITE, font=desc_font)
    return img

def main():
    os.makedirs(cwd + "/imgs", exist_ok=True)
    content = parser()
    i = 0
    for item in content:
        title = item["title"]
        description = item["description"]
        img = drawer(img_get(item["image"]), title, description).resize((650, 370), Image.ANTIALIAS)
        img.save(cwd + "/imgs/img_" + str(i)+".png")
        i = i + 1
        if i == 10:
            break

if __name__ == "__main__":
    main()
