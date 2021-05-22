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


@click.command()
# @click.argument('source', type=click.Path(exists=True, file_okay=True, dir_okay=True))
def picren():
    args = sys.argv
    print(args)
    source_path = clean_source()
    print(source_path)

    # dest_dir = click.prompt(
    #    'Please enter a valid destination path', default='/Picren')
    # print(dest_path)

    # handle passed in files
    # source_path = args
    dest_path = '/Picren'
    traverse_dirs(source_path, dest_path)
    # handle video formats

    # handle duplicates
    # keep track of the photos
    # test if file exists
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
