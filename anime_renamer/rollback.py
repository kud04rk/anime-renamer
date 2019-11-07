from os.path import join
from os import getcwd,rename,walk

exts = ['.mkv', '.mp4', '.avi', '.flv', '.mpg', '.mpeg', '.wmv', '.webm', '.vob', '.mov', '.3gp', '.ogv']
invalidfiles=[]


def getfextensions(filename):
    """
    uses file name to get extension
    :param filename:
    :return:
    """
    a = filename.rfind('.')
    return filename[a:]

def get_episode_no(filename):
    try:
        temp = (filename.split('Ep-'))[1].split('-')[0]
        episode = temp[0:temp.find("S")].strip()
    except:
        print('error in episode')

    return int(episode)


def rollback():
    for root, dirs, files in walk(".", topdown=False):
        for name in files:
            filename = join(root, name)
            if getfextensions(filename) in exts:
                try:

                    src = getcwd() + filename.replace('./', '/')
                    dst = getcwd() + '/' + str(get_episode_no(str(name)))+getfextensions(filename)
                    rename(src, dst)

                except IOError:
                    print(IOError)
                    print(filename)

            else:
                invalidfiles.append(filename)
    return
rollback()