import os
import shutil


def get_files(dirpath: str) -> list:
    files = []
    for f in os.listdir(dirpath):
        if os.path.isfile(os.path.join(dirpath, f)):
            files.append(f)

    return files


def move_file(srcfilepath, dstdirpath):
    shutil.move(srcfilepath, dstdirpath)
