########################################
# RSS_AJ Parser and Drawer             #
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


def img_url(url):
    response = requests.get(url)
    content = str(response.content)
    tag_start = '<meta name="NewImage" content="'
    tag_end = '" />'
    x = content.find(tag_start)
    y = content[x:].find(tag_end)
    img_id = content[x+len(tag_start):x+y]
    img_url = "http://www.aljazeera.net/File/GetImageCustom/{}/747/441".format(img_id)
    if len(img_url) > 100:
        return None
    return img_url

def img_get(url):
    if url is None:
        return Image.open(cwd + "/no_img.jpeg")
    img_response = requests.get(url)
    return Image.open(BytesIO(img_response.content))

def parser():
    rss_aj = "http://www.aljazeera.net/aljazeerarss/be46a341-fe26-41f1-acab-b6ed9c198b19/e6aef64d-084c-42f0-8269-abe48e0cd154"
    feed = feedparser.parse(rss_aj)
    content = list()
    for item in feed["items"]:
        item_dict = dict()
        item_dict["title"] = item["title"]
        item_dict["description"] = item["description"]
        item_dict["link"] = item["link"]
        item_dict["image"] = img_url(item["link"])
        content.append(item_dict)
#    content = json.dumps(content, sort_keys=False, ensure_ascii=False, indent=4)
    return content

def drawer(img, title, description):
    img = img.convert("RGBA")
    rect = Image.new("RGBA", img.size, NOCOLOR)
    draw_rect = ImageDraw.Draw(rect)
    draw_rect.rectangle(((0, 250), img.size), fill=TBLACK)
    img = Image.alpha_composite(img, rect)
    draw = ImageDraw.Draw(img)
    title_font = afont(30, "b")
    w = title_font.getsize(title)[0]
    draw.text(((747-w)/2, 250), title, YELLOW, title_font)
    desc_font = afont(25, "b")
    desc_list = text_wrap(description, 57)
    for i in range(len(desc_list)):
        line = desc_list[i]
        w = desc_font.getsize(line)[0]
        draw.text(((747-w)/2, 300+i*28), line, WHITE, desc_font)
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
#        if i == 10:
#            break

if __name__ == "__main__":
    main()
