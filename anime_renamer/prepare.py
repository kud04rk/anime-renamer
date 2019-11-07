from os import rename, getcwd, walk
from os.path import join

exts = ['.mkv', '.mp4', '.avi', '.flv', '.mpg', '.mpeg', '.wmv', '.webm', '.vob', '.mov', '.3gp', '.ogv']
invalidfiles=[]


def getfileextensions(filename):
    """
    uses file name to get extension
    :param filename:
    :return:
    """
    a = filename.rfind('.')
    return filename[a:]




def preparefiles():
    print('inside prepare files')
    for root, dirs, files in walk(".", topdown=False):
        for name in files:
            filename = join(root, name)
            if getfileextensions(filename) in exts:
                try:

                    src = getcwd() + filename.replace('./', '/')
                    dst = getcwd() + '/' + name
                    rename(src, dst)

                except IOError:
                    print(IOError)
                    print(filename)

            else:
                invalidfiles.append(filename)
    return
preparefiles()