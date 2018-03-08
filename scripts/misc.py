# Colors
NOCOLOR = (0, 0, 0, 0)
BLACK = (0, 0, 0, 255)
TBLACK = (0, 0, 0, 200)
YELLOW = (225, 192, 1, 255)
GREY = (155, 150, 150, 255)
WHITE = (225, 225, 225, 255)
BLUE = (0, 101, 153, 255)

# Latin Font
from PIL import ImageFont
import os
import sys
md = os.path.dirname(os.path.realpath(__file__))
def lfont(size, type="r"):
    if type == "r":
        return ImageFont.truetype(md + "/fonts/Lato-Regular.ttf", size)
    elif type == "b":
        return ImageFont.truetype(md + "/fonts/Lato-Bold.ttf", size)
    elif type == "l":
        return ImageFont.truetype(md + "/fonts/Lato-Light.ttf", size)
    else:
        return "Font Type Error"

# Arabic Font
def afont(size, type="b"):
    if type == "r":
        return ImageFont.truetype(md + "/fonts/Aj-Regular.ttf", size)
    elif type == "b":
        return ImageFont.truetype(md + "/fonts/Aj-Bold.ttf", size)
    elif type == "l":
        return ImageFont.truetype(md + "/fonts/Aj-Light.ttf", size)
    else:
        return "Font Type Error"

# Age Caluclator
from dateutil.relativedelta import *
from datetime import datetime
def age_calculator(date):
    now = datetime.now()
    rdelta = relativedelta(now,date)
    years = rdelta.years
    months = rdelta.months
    days = rdelta.days
    return str(years) + " years " + str(months) + " months " + str(days) + " days"

# Wrap Text
def text_wrap(text, chunk_size):
    wrapped_text = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    for i in range(len(wrapped_text)-1):
        line = wrapped_text[i]
        if line[-1] != ' ':
            space = line.rfind(' ')
            wrapped_text[i+1] = (wrapped_text[i])[space:] + wrapped_text[i+1]
            wrapped_text[i] = (wrapped_text[i])[0:space]
    return wrapped_text
