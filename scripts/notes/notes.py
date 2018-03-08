########################################
# Notes Parser                         #
########################################

import os
import sys
import json

from datetime import datetime
from configparser import ConfigParser

# Add Parent Directory to the Path
cwd = os.path.dirname(os.path.realpath(__file__))
pd = os.path.dirname(cwd)
sys.path.append(pd)
from misc import *


def parser():
    notes = list()
#    Person = datetime(1990, 1, 1)
#    notes.append("[Age] Person's age is " + age_calculator(Person) + ".")
    with open(notes_file) as f:
        lines = f.read().splitlines()
        for line in lines:
            notes.append(line)
    notes = json.dumps(notes, sort_keys=False, ensure_ascii=False, indent=4)
    return notes

def main():
    content = parser()
    with open(cwd + '/notes.json', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    config = ConfigParser()
    config.read(pd + '/config.ini')
    notes_file = config['notes']['file']
    main()

