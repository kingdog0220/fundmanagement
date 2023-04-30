import os
import shutil


def get_files(dirpath: str) -> list:
    """ファイルの一覧を取得する

    Args:
        dirpath (str): ファイルの一覧を取得するディレクトリのパス

    Returns:
        list: ファイルの一覧
    """
    files = []
    for f in os.listdir(dirpath):
        if os.path.isfile(os.path.join(dirpath, f)):
            files.append(f)

    return files


def move_file(srcfilepath, dstdirpath):
    """ファイルを移動する

    Args:
        srcfilepath (_type_): 移動するファイルのパス
        dstdirpath (_type_): 移動先のパス
    """
    shutil.move(srcfilepath, dstdirpath)
