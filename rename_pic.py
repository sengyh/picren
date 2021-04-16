import sys
import os
import subprocess
import re
import time
import json

from search_location import get_address, reverse_geocode, process_address


def rename_pic(pic, session):
    # use subprocess or another way to parse exif data
    #forbidden_characters = '"*/:<>?\|'
    #unicode_characters = '”⁎∕꞉‹›︖＼⏐'
    print(pic)
    date_time_str = get_time(pic, session)

    geocode_on = True
    address = {}
    if geocode_on:
        addr_str = get_address(pic, session)
        if addr_str != '':
            address = json.loads(addr_str)
            # hiearchy: [place, village, suburb, city, state, country]
            final_addr_list = process_address(address)
            print(final_addr_list, '\n')
        else:
            print("sorry, you don't belong anywhere :(" + '\n')
    return


def get_time(pic, session):
    dtorg = subprocess.Popen(['exiftool', '-datetimeoriginal', '-n', pic],
                             stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    # print(dtorg)
    if dtorg:
        print(dtorg.rstrip("\n"))
        date_time_arr = dtorg.rstrip("\n").split(': ')[1].split(' ')
        date = date_time_arr[0].replace(':', '-')
        time = date_time_arr[1].replace(':', '꞉')
        subsec_org = subprocess.Popen(['exiftool', '-subsectimeoriginal', '-n', pic],
                                      stdout=subprocess.PIPE).communicate()[0].decode('ascii')
        if subsec_org:
            subsec = subsec_org.rstrip("\n").split(': ')[1]
            time = time + '꞉' + subsec
        date_time_str = date + '_' + time
        print(date_time_str)
    else:
        print('no create date found')
    # if no subsec just do
    return ''


def process_date_time():
    return
