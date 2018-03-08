#!/usr/bin/python

import requests
import sys

from configparser import ConfigParser

def get_location(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address="{}"'
    response = requests.get(url.format(address))
    content = response.json()
    status = content['status']
    if status == 'OK':
        lat = content['results'][0]['geometry']['location']['lat']
        lng = content['results'][0]['geometry']['location']['lng']
        formatted_address = content['results'][0]['formatted_address']
        return lat, lng, formatted_address
    else:
        sys.exit(status)

def main():
    if len(sys.argv) >= 2:
        address = ' '.join(sys.argv[1:])
        lat, lng, formatted_address = get_location(address)
        config = ConfigParser()
        config.read('config.ini')
        config['location'] = {'address': formatted_address, 'lat': lat, 'lng': lng}
        print("Your address is " + formatted_address)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        print("Please give an address")

if __name__ == "__main__":
    main()