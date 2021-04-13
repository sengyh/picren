#!/usr/bin/env python3
import sys
import os
import subprocess

from traverse_dirs import traverse_dirs
from rename_pic import rename_pic

  # make setup script
  # attach as a command line application
  # connect to database while program is running

def main():
  args = sys.argv
  # handle passed in files
  traverse_dirs(args)
  # handle video formats

  # handle duplicates 
    # keep track of the photos
    # test if file exists
    

  
  return 0

if __name__ == "__main__":
  main()