import os
import sys
from rename_pic import rename_pic
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker


def traverse_dirs(args):
    engine = create_engine('sqlite:///location_cache.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    photo_exts = ['.heic', '.heif', '.jpg', '.jpeg', '.png', '.tiff', '.raw']
    video_exts = ['.mov', '.hevc', '.mp4', '.mpg', '.avi']
    for arg in args:
        if (os.path.isdir(arg)):
            for root, subdirs, files in os.walk(arg):
                # for subdir in subdirs:
                #print(os.path.join(root, subdir))
                for file in files:
                    #print(os.path.join(root, file))
                    if not file.lower().endswith(tuple(photo_exts)):
                        continue
                    rename_pic(os.path.join(root, file), session)
        if (os.path.isfile(arg)):
            # print(arg)
            if not arg.lower().endswith(tuple(photo_exts)):
                continue
            rename_pic(arg, session)
