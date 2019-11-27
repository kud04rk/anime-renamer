import sys
from os import listdir
from os.path import isfile, join
from os import rename
from os import getcwd
import tvdbsimple as tvdb
from pip._vendor.distlib.compat import raw_input

tvdb.KEYS.API_KEY = 'UB0SOLRB8XH3I39L'
validfiles = []
invalidfiles = []


class sfilenames:
    def __init__(self, episodenumber, filename, extension):
        self.extension = extension
        self.filename = filename
        self.episodenumber = episodenumber


def main(path=getcwd()):
    """
    does all the operations in steps
    :param path:
    :return:
    """
    get_series_deatils(sys.argv[1])
    scanfolder(path)
    match_filename(sys.argv[1])

    return


def mainpackage(seriesid):
    """
    does all the operations in steps
    :param path:
    :return:
    """
    path = getcwd()
    get_series_deatils(seriesid)
    scanfolder(path)
    match_filename(seriesid)

    return


def scanfolder(path):
    """
    scans the folder for files with extensions.mkv.mp4 etc and stores all the feasable cadidates.
    :param path:
    :return:
    """
    """need to go into config file supported extensions"""
    exts = ['.mkv', '.mp4', '.avi', '.flv', '.mpg', '.mpeg', '.wmv', '.webm', '.vob', '.mov', '.3gp', '.ogv']
    allfiles = [f for f in listdir(path) if isfile(join('.', f))]
    for file in allfiles:
        if getextension(file) in exts:
            try:
                validfiles.append(sfilenames(int(file.replace(getextension(file), '')), str(file), getextension(file)))
            except:
                continue


        else:
            invalidfiles.append(file)

    return


def getextension(filename):
    """
    uses file name to get extension
    :param filename:
    :return:
    """
    a = filename.rfind('.')
    return filename[a:]


def get_series_deatils(seriesid):
    """
    get series deatils sunch as poster info description no of seasons etc
    episodes = tvdb.Series_Episodes(series_id[0]['id']).all()
    print('Number of episodes: ', len(episodes))
    :param series_name:
    :return:
    """
    show = tvdb.Series(seriesid)
    info = show.info()
    linesep()
    print('Series name       : ', info['seriesName'])
    print('Overview          : ', info['overview'])
    linesep()

    return


def match_filename(seriesid):
    """
    get filenames from tv_db and match them with local filenames and save them for confirmation.
    :param filename:
    :return:
    """
    show = tvdb.Series(seriesid)
    info = show.info()
    title = info['seriesName']
    episodes = tvdb.Series_Episodes(seriesid).all()
    for s in episodes:
        for k in validfiles:
            try:
                if s['absoluteNumber'] == k.episodenumber:
                    outfilename = make_filename(title, s['airedSeason'], s['airedEpisodeNumber'],
                                                s['episodeName'],
                                                s['absoluteNumber'])
                    src = getcwd() + '/' + k.filename
                    dst = getcwd() + '/' + outfilename + k.extension
                    rename(src, dst)
            except IOError:
                print(IOError)
                continue

    return


def removeNonAscii(s): return "".join(i for i in s if ord(i) < 128)


def make_filename(seriesname, seasonnumber, seasonepisode, episodename, episodenumber):
    """
    this is used to make filename as per the format
    :return:
    """
    name = [str(removeNonAscii(seriesname)), ' Ep-', str(episodenumber), ' S', str(seasonnumber), 'E', str(seasonepisode), ' -',
            str(removeNonAscii(episodename))]

    finalname = ''.join(name)

    return finalname.replace(':', '!').replace('?', '')


def linesep():
    """
    this is used to drawline in the terminal window
    :return:
    """
    print("-" * 100)
    return


if len(sys.argv) > 1:
    main()
else:
    blah = ''
