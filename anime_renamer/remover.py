from os import listdir
from os.path import isfile, join
from os import getcwd, rename

from pip._vendor.distlib.compat import raw_input

validfiles=[]
invalidfiles=[]


def scancurrentfolder():
    """
    scans the folder for files with extensions.mkv.mp4 etc and stores all the feasable cadidates.
    :param path:
    :return:
    """
    """need to go into config file supported extensions"""
    exts = ['.mkv', '.mp4', '.avi', '.flv', '.mpg', '.mpeg', '.wmv', '.webm', '.vob', '.mov', '.3gp', '.ogv']
    str_to_replace = raw_input("string to be removed from filename: ")
    allfiles = [f for f in listdir('.') if isfile(join('.', f))]
    for file in allfiles:
        if getfileextension(file) in exts:
            src = getcwd() + '/' + str(file)
            outfilename=(str(file).replace(str(str_to_replace), '')).strip()
            dst = getcwd() + '/' + outfilename
            rename(src, dst)

        else:
            invalidfiles.append(file)


    return


def getfileextension(filename):
    """
    uses file name to get extension
    :param filename:
    :return:
    """
    a = filename.rfind('.')
    return filename[a:]

scancurrentfolder()