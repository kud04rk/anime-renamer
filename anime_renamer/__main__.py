import tvdbsimple as tvdb
from pip._vendor.distlib.compat import raw_input

tvdb.KEYS.API_KEY = 'UB0SOLRB8XH3I39L'


def main():
    series_name = raw_input("What's the name of anime? eg naruto One Piece . Be precise line caps etc: ")
    search = tvdb.Search()
    matched_names = search.series(series_name)
    i = 1
    for series in matched_names:
        sep()
        if 'overview' not in series:
            print('No   :', i)
            print('Series name       : ', series['seriesName'])
        else:
            print('No   :', i)
            print('Series name       : ', series['seriesName'])
            print('Overview          : ', series['overview'])

        sep()
        i = i + 1
    id = raw_input("Please enter the Series NUMBER from the above list ")
    seriesid = matched_names[int(id) - 1]['id']
    print('seriesid:' + str(seriesid))
    print('Series name       : ', matched_names[int(id) - 1]['seriesName'], 'SELECTED')
    prepareressult = raw_input("Do you want to prepare folder(y/n)(read docs!) ")
    if prepareressult == 'y':
        from anime_renamer.prepare import preparefiles
        print("all required files are in folder and continuing")
        sep()
    else:
        print("assuming all required files are in folder and continuing")
        sep()
    removeresult = raw_input("Remove text to only leave episode number(y/n)(read docs!) ")
    if removeresult == 'y':
        remove()
        print("all required files are in correct format and continuing")
        sep()
    else:
        print("assuming all required files are in correct format and continuing")
        sep()
    renameresult = raw_input("Rename episodes(y/n)(read docs!) ")
    if renameresult == 'y':
        from anime_renamer.renamer import mainpackage as renamer
        renamer(str(seriesid))
        print('If any files remaining copy them toa different folder and do the rename')
        sep()
    else:
        print('If any files remaining copy them toa different folder and do the rename')
        sep()
    oraganizeresult = raw_input("Do you want to oraganize result back into season folders(y/n)(read docs!) ")
    if oraganizeresult == 'y':
        from anime_renamer.organiser import move_files
        print("continuing after organization complete")
        sep()
    else:
        print("continuing after organization complete")
        sep()
    downloadresult = raw_input("Do you want to download metadata for everything(y/n)(read docs!) ")
    if downloadresult == 'y':
        from anime_renamer.downloader import mainpackage as donwloader
        donwloader(seriesid)
        print("hope everything went smoothly for you **BUY ME coffee if you are happy** ")
        sep()
    else:
        print("hope everything went smoothly for you **BUY ME coffee if you are happy** ")
        sep()

    return


def sep():
    """
    this is used to drawline in the terminal window
    :return:
    """
    print("-" * 100)
    return


def remove():
    from anime_renamer.remover import scancurrentfolder
    removeresult = raw_input("Remove text to only leave episode number(y/n)(read docs!) ")
    if removeresult == 'y':
        remove()

    return


if __name__ == '__main__':
    main()
