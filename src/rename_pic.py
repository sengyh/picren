import sys
import os
import subprocess
import re
import time
import json

from src.search_location import get_address, reverse_geocode, process_address
from src.transplant_pic import transplant_pic


def rename_pic(pic, session, destination):
    # use subprocess or another way to parse exif data
    #forbidden_characters = '"*/:<>?\|'
    #unicode_characters = '”⁎∕꞉‹›︖＼⏐'
    # print(pic)
    date_time_str = get_date_time(pic, session)
    #print(date_time_str + '\n')

    geocode_on = True
    final_address_list = []
    if geocode_on:
        addr_str = get_address(pic, session)
        if addr_str != '':
            address = json.loads(addr_str)
            # hiearchy: [place, village, suburb, city, state, country]
            final_address_list = process_address(address)
            #print(final_address_list, '\n')
        # else:
            #print("sorry, you don't belong anywhere :(" + '\n')

    transplant_pic(pic, date_time_str, final_address_list, destination)
    return


def get_date_time(pic, session):
    new_pic_name = ''
    dtorg = subprocess.Popen(['exiftool', '-datetimeoriginal', '-n', pic],
                             stdout=subprocess.PIPE).communicate()[0].decode('ascii')
    if dtorg:
        date_time_arr = dtorg.rstrip("\n").split(': ')[1].split(' ')
        date = date_time_arr[0].replace(':', '-')
        time = date_time_arr[1].replace(':', '꞉')
        subsec_org = subprocess.Popen(['exiftool', '-subsectimeoriginal', '-n', pic],
                                      stdout=subprocess.PIPE).communicate()[0].decode('ascii')
        if subsec_org:
            subsec = subsec_org.rstrip("\n").split(': ')[1]
            time = time + '꞉' + subsec
        date_time_str = date + '_' + time
        new_pic_name = date_time_str
    else:
        # print('no create date found')
        # dtacc = subprocess.Popen(['exiftool', '-modifydate', '-n', pic],
        # stdout=subprocess.PIPE).communicate()[0].decode('ascii')
        only_pic_name = pic.split('/')[-1]
        new_pic_name = only_pic_name.split('.')[0]
    return new_pic_name
