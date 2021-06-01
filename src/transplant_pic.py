import shutil
import os
from pathlib import Path
import re


def transplant_pic(pic, new_name_str, address_list, destination):
    #Path(destination).mkdir(parents=True, exist_ok=True)
    pic_extension = str(pic).split('.')[-1]

    dt_list = []
    if re.match('^\d{4}-\d{2}-\d{2}_\d{2}꞉\d{2}꞉\d{2}', new_name_str):
        dt_list = get_date_time_list(new_name_str)

    dest_path = destination
    new_pic_name = new_name_str
    # no location, just put in folder and return
    if address_list == []:
        dest_path += '/_No Location_'
        if dt_list == []:
            dest_path += '/_No Date_'
        else:
            dest_path += '/' + dt_list[0]
    else:
        country = address_list[5]
        state = address_list[4]
        city = address_list[3]
        suburb = address_list[2]
        village = address_list[1]
        place = address_list[0]
        # set up directories
        if country == '':
            dest_path += '/_Mr Worldwide_'
        else:
            dest_path += '/' + country
            # city and states are in different folders
            if city == '':
                if state == '':
                    dest_path += '/_Stateless_'
                else:
                    dest_path += '/' + state
                    if suburb == '':
                        dest_path += "/_Still In State_"
                    else:
                        dest_path += '/' + suburb
            else:
                dest_path += '/' + city
        # setup new pic name
        if place != '':
            new_pic_name += '_' + place
        if city != '':
            if suburb != '':
                new_pic_name += '_' + suburb
        else:
            if village != '':
                new_pic_name += '_' + village

    # get home directory and combine with path
    #full_path = str(Path.home()) + dest_path
    full_path = dest_path
    Path(full_path).mkdir(parents=True, exist_ok=True)
    src = str(pic)
    dst = full_path + '/' + new_pic_name + '.' + pic_extension
    #shutil.move(src, dst)
    print("moved to " + dst)
    return


def get_date_time_list(first_name_str):
    date_time_separator = first_name_str.split('_')
    date = date_time_separator[0]
    time = date_time_separator[1]

    date_separator = date.split('-')
    year = date_separator[0]
    month = date_separator[1]
    day = date_separator[2]

    time_separator = time.split('꞉')
    hour = time_separator[0]
    minute = time_separator[1]
    second = time_separator[2]

    dt_list = [year, month, day, hour, minute, second]
    return dt_list
