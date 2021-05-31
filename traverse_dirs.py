import os
import sys
import time
import click
from pathlib import Path
from rename_pic import rename_pic
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from alive_progress import alive_bar


def traverse_dirs(arg, dest_dir, num_pics):
    # change this when packaging shit is figured out
    p = Path.home() / 'projects' / 'picren' / 'location_cache.db'
    p_str = 'sqlite:///' + str(p)
    engine = create_engine(p_str)
    Session = sessionmaker(bind=engine)
    session = Session()

    photo_exts = ['.heic', '.heif', '.jpg', '.jpeg', '.png', '.tiff', '.raw']
    video_exts = ['.mov', '.hevc', '.mp4', '.mpg', '.avi']
    # for arg in args:
    pic_count = 0
    with alive_bar(num_pics, bar='smooth') as bar:
        if (os.path.isdir(arg)):
            for root, subdirs, files in os.walk(arg):
                # for subdir in subdirs:
                #print(os.path.join(root, subdir))
                for file in files:
                    #print(os.path.join(root, file))
                    if not file.lower().endswith(tuple(photo_exts)) or file.startswith("._"):
                        continue
                    else:
                        pic_count += 1
                        bar()
                        time.sleep(0.001)
                        rename_pic(os.path.join(root, file), session, dest_dir)
    print(pic_count)
    if (os.path.isfile(arg)):
        print(arg)
        file_path_str = str(arg)
        if not file_path_str.lower().endswith(tuple(photo_exts)):
            click.echo(
                "Conversion failed. Selected file is not a photo. Please select a valid photo")
        else:
            rename_pic(arg, session, dest_dir)
