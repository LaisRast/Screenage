########################################
# Datetime Parser and Drawer           #
########################################

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


def parser():
    now = datetime.now()
    time = dict()
    time["time"] = now.strftime("%H:%M")
    time["date"] = now.strftime("%A, %d %b")
    time["day_name"] = now.strftime("%A")
    time["month_name"] = now.strftime("%B")
#    time = json.dumps(time, sort_keys=False, ensure_ascii=False, indent=4)
    return time

def drawer(content):
    img = Image.new('RGBA', (300, 120), BLACK)
    draw = ImageDraw.Draw(img)
    w1 = lfont(80, "l").getsize(content["time"])[0]
    draw.text(((300-w1)/2, 0), content["time"], WHITE, lfont(80, "l"))

    w2 = lfont(25, "b").getsize(content["date"])[0]
    draw.text(((300 - w2)/2, 85), content["date"], WHITE, lfont(25, "b"))

    return img

def main():
    content = parser()
    img = drawer(content)
    img.save(cwd + "/date_time.png")

if __name__ == "__main__":
    main()


