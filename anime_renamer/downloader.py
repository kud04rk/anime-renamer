import sys

import tvdbsimple as tvdb
import requests
from os import walk, getcwd
from os.path import join
import xml.etree.ElementTree as ET
import xml.dom.minidom as xmlpretty

tvdb.KEYS.API_KEY = 'UB0SOLRB8XH3I39L'

image_basepath = 'https://www.thetvdb.com/banners/'


def downloadseriesdata(seriesid):
    """this downlaods series data
    banner
    poster
    fanart
    """
    show = tvdb.Series(seriesid)
    info = show.info()
    title = info['seriesName']
    plot = info['overview']
    banner = info['banner']
    print(title, plot, banner)
    poster = show.Images.poster()[0]['fileName']
    fanart = show.Images.fanart()[0]['fileName']
    make_nfo_file_series(title, plot)
    downlaod_file_images(banner, 'Banner')
    downlaod_file_images(poster, 'Poster')
    downlaod_file_images(fanart, 'Fanart')
    return


def getnameextensions(name):
    """get extensionof the name"""

    a = name.rfind('.')
    return name[a:]
    return


def get_episodeno(filename):
    try:
        temp = (filename.split('Ep-'))[1].split('-')[0]
        episode = temp[0:temp.find("S")].strip()
    except:
        episode = 1

    return int(episode)


def download_episode_data(sereisid):
    """dwonlaod episode data"""
    episodes = tvdb.Series_Episodes(sereisid).all()
    exts = ['.mkv', '.mp4', '.avi', '.flv', '.mpg', '.mpeg', '.wmv', '.webm', '.vob', '.mov', '.3gp', '.ogv']
    for root, dirs, files in walk(getcwd(), topdown=False):
        for name in files:
            filename = join(root, name)
            if getnameextensions(filename) in exts:
                for s in episodes:
                    try:
                        if s['absoluteNumber'] == get_episodeno(filename):
                            downlaod_file_images(s['filename'], filename.replace('./', getcwd()).replace(
                                getnameextensions(filename), ''))
                    except IOError as e:
                        print(e.errno)
                        print(e)
                    continue
    return


def make_nfo_file_series(title_text, plot_text):
    """
    this function will create nfo file for the series
    :param title:
    :param plot:
    :return:
    """
    tvshow = ET.Element('tvshow')
    title = ET.SubElement(tvshow, 'title')
    plot = ET.SubElement(tvshow, 'plot')
    title.text = title_text
    plot.text = plot_text

    # create a new XML file with the results
    mydata = ET.tostring(tvshow)
    xml = xmlpretty.parseString(mydata)
    xml_pretty_str = xml.toprettyxml()
    xmlfinal = xml_pretty_str.replace('<?xml version="1.0" ?>', '')
    print(xmlfinal)
    myfile = open(title_text + ".nfo", "w")
    myfile.write(xmlfinal)
    return


def downlaod_file_images(img_url, oufilename):
    """this function will downalod the image given url"""
    print(image_basepath + img_url)
    print(oufilename)
    r = requests.get(image_basepath + img_url, stream=True)
    with open(oufilename + ".jpg", 'wb') as f:
        f.write(r.content)
        return


def make_nfo_file_episode(title_text, plot_text):
    """
    this function will create nfo file for the series
    :param title:
    :param plot:
    :return:
    """
    tvshow = ET.Element('tvshow')
    title = ET.SubElement(tvshow, 'title')
    plot = ET.SubElement(tvshow, 'plot')
    title.text = title_text
    plot.text = plot_text

    # create a new XML file with the results
    mydata = ET.tostring(tvshow)
    myfile = open(title_text + ".nfo", "w")
    myfile.write(mydata)
    return


def main():
    """this function coordinates all other functions
    """
    downloadseriesdata(sys.argv[1])
    download_episode_data(sys.argv[1])

    return


def mainpackage(seriesid):
    """used for packaging"""
    downloadseriesdata(seriesid)
    download_episode_data(seriesid)

    return


if len(sys.argv) > 1:
    main()
else:
    blah = ''
