#!/usr/bin/env python3
import sys
import os
import subprocess
import click
from pathlib import Path, PosixPath

from traverse_dirs import traverse_dirs
from rename_pic import rename_pic

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
    Picren helps you rename and reorganise your photos by date and location.
    Simply provide a valid folder or photo and a valid folder to create your picren library.

    The current (and default) method of organisation is to move photos to the destination folder and placed in a hierarchical order based on the address from the top down. 

    The default photos will be renamed to the date, time and location (if present) when and where it was taken.
    """
    args = sys.argv
    print(args)
    dest_path = str(dest / 'Picren')
    print(dest_path)

    #source_path = clean_source()
    source_path = source

    # dest_dir = click.prompt(
    #    'Please enter a valid destination path', default='/Picren')
    # print(dest_path)

    # handle passed in folder
    traverse_dirs(source_path, dest_path)

    return 0


def clean_source():
    cleaned_source = None
    while cleaned_source is None:
        source = click.prompt(
            "Please enter the folder or photo that you'd like to convert", type=str
        )
        p = Path(source)
        path_list = source.split('/')
        if (path_list[0] == '~'):
            p = Path.home()
            path_list.pop(0)
            for pfr in path_list:
                p = p / pfr
        else:
            p = Path.cwd() / source
        try:
            p = p.resolve(strict=True)
            cleaned_source = p
        except FileNotFoundError:
            click.echo("File/Folder does not exist. Please try again.")
            pass
    return cleaned_source

# if __name__ == "__main__":
#   picren()
