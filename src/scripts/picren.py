#!/usr/bin/env python3
import subprocess
import sys
import glob
import os 
import click
import sqlalchemy
import geopy

from pathlib import Path, PosixPath
from src.traverse_dirs import traverse_dirs
from src.rename_pic import rename_pic
import src.create_db

# make setup script
# attach as a command line application
# connect to database while program is running

# handle video formats
# handle duplicates
# keep track of the photos
# test if file exists


@click.command()
@click.argument('source', nargs=1, type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.argument('dest', nargs=1, default=Path.home(), type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
def picren(source, dest):
    """
    Reorganises and renames your photos\n
    Folder Structure:\n
    Picren\n
    ⎿ __ Country\n
    \t ⎿ __ State\n
    \t      ⎿ __ Suburb\n
    \t\t   ⎿ __ date_time_village.JPG\n
    \t ⎿ __ City\n
    \t      ⎿ __ date_time_suburb.JPG\n
    ⎿ __ __No Location__\n
    \t   ⎿ __ Year\n
    \t        ⎿ __ date_time.JPG\n
    \t   ⎿ __ __No Date__\n
    \t\t  ⎿ __ original_name.JPG\n
    """
    # check for local file /.picren
    # error, doesnt work if files dont already exist
    # use a shell setup script instead
    app_data_path = Path.home() / '.picren'
    #print(app_data_path)
    if os.path.isdir(app_data_path) is False:
        #print('running script...')
        os.system("python3 src/create_db.py")

    dest_path = str(dest / 'Picren')
    source_path = str(source)
    num_pics = scanDir(source_path)

    click.confirm("Confirm migration to " +
                  click.style(dest_path, fg='green', underline=True) + "?", abort=True)
    #print('boop, magic wand tapped')

    # handle passed in folder
    traverse_dirs(source_path, dest_path, num_pics)
    return 0


def scanDir(source_path):
    photo_exts = ['.heic', '.heif', '.jpg', '.jpeg', '.png', '.tiff', '.raw']
    numPics = 0
    totalSize = 0
    for filepath in glob.iglob(source_path + '**/**', recursive=True):
        if Path(filepath).is_file and filepath.lower().endswith(tuple(photo_exts)):
            numPics += 1
            totalSize += Path(filepath).stat().st_size
            # print(filepath.split('/')[-1])
    totalReformatted = convert_bytes(totalSize)
    click.echo(click.style(str(numPics), fg='green') +
               " photos (" +
               click.style(str(totalReformatted), fg='cyan') +
               ") found in " + click.style
               (source_path, fg='yellow', underline=True) + " under all subfolders.")
    return numPics


def convert_bytes(num):
    step_unit = 1000.0  # 1024 if you're anal
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit

if __name__ == "__main__":
    picren()
