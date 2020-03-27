
from os import rename,mkdir,getcwd,listdir
from os.path import isfile, join, isdir


invalidfiles=[]

def getseason(filename):
    """this will return the season number given the file name and create folde if dowesnt exist"""
    try:
        temp = (filename.split('Ep-'))[1].split('-')[0]
        season = temp.split('S')[1].split('E')[0].strip()
        print('directory exists') if (isdir(getcwd() + '/Season ' + str(season))) else mkdir(
            getcwd() + '/Season ' + str(season))
    except:
        season = 0
        print('directory exists') if (isdir(getcwd() + '/Season 0')) else mkdir(
            getcwd() + '/Season 0')



    return str(season)


def move_files():
    """this is move files to respective folders"""
    exts = ['.mkv', '.mp4', '.avi', '.flv', '.mpg', '.mpeg', '.wmv', '.webm', '.vob', '.mov', '.3gp', '.ogv']
    allfiles = [f for f in listdir(getcwd()) if isfile(join('.', f))]
    for file in allfiles:
        if getextensions(file) in exts:
            try:

                src=getcwd()+'/'+str(file)
                dst=getcwd()+'/Season '+getseason(str(file))+'/'+str(file)
                print(src)
                print(dst)
                rename(src, dst)

            except IOError:
                print(IOError)
                print(file)
                continue

        else:
            invalidfiles.append(file)
    return

def getextensions(filename):
    """
    uses file name to get extension
    :param filename:
    :return:
    """
    a = filename.rfind('.')
    return filename[a:]

move_files()