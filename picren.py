#!/usr/bin/env python3
import sys
import os
import subprocess
from traverse_dirs import traverse_dirs
from rename_pic import rename_pic

def main():
  cargs = sys.argv
  traverse_dirs(cargs)

  # make setup script

  # attach as a command line application
  
  # handle passed in files
  # connect to database while program is running
  photo_exts = ['.heic', '.heif', '.jpg', '.jpeg', '.png', '.tiff', '.raw', '.mov']
  video_exts = ['.mov', '.hevc', '.mp4', '.mpg', '.avi']

  # traverse dirs works now, saving this for testing
  #for arg in cargs:
  #  if not arg.lower().endswith(tuple(photo_exts)):
  #    continue
  #  rename_pic(arg)

    # handle video formats

    # handle duplicates 
      # keep track of the photos
      # test if file exists

    # ORM to database: what typescript is to javascript
    

  
  return 0

if __name__ == "__main__":
  main()