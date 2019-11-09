Anime Renamer
-------------------
------------------- 

Anime Renamer is a FREE,simple to use comand line renamer for all the anime files similar to filebot(which is now paid).
Any issues with the code please write in issues section (comments feedback or enchnacement are also welcome).

Personnaly used for many anime.

CONTRIBUTE:
---------------------------

PLEASE TRY WITH ONE EPISODE BEFORE TRYING WITH COMPLETE SEREIS.(COPY FILE TO A DIFFERENT FOLDER AND TRY)

HOW TO USE
----------------

Prerequisites:
----------------------

This script will ONLY work if you have episode number in your episode name.

you have to manually convert the episode name into 1.mp4 2.mp4 etc for this script to work

example:[ANIMEKG] Title episode 356 [720p].mp4

you have to make it 356.mp4 while running main.py

Two ways to USE:
----------------------

Meathod 1

1)install anime-renamer (pip install anime-renamer)

2)run anime_renamer in the base folder of the anime.


Meathod 2(dont want to install)

Steps:
------------------

1)run pip install tvdbsimple(need python for pip to work)

2)Copy all .py files from anime_reanmer folder into the base folder of the series and run python main.py


Detailed explanation[MUST READ]
------------------------------

This script works bsed on absolute numbering (i mean episode numbers like episode 2.mp4)

1)main.py:Do you want to prepare folder(y/n)

if yes this will move all files from the sub folders to mail folders this is necessary

2)Remove text to only leave episode number(y/n)

if yes this will help in converting the file name to required format.

3)Rename episodes(y/n)

if yes this will rename the files into the following format Naruto Ep:1 S1E1 -Enter: Naruto Uzumaki!(title Ep:episode number S season number Episodenumber - episode name) (only one format can be used)

4)Do you want to oraganize result back into season folders(y/n)

if yes this will oraanized the reanamed episodes into respective season folders

5)Do you want to download metadata for everything(y/n)

if yes this will download meta data for all episodes.
 

ROLLBACK
-------------------------------------
IF u didnt like the output or want to change it fpr any other reason
copy rollback.py from anime_renamer folder and run it.(python rollack.py)

DEVELOPER
----------------------------

Please contribute.

fork -> clone-> branch-> commit with proper comments.

Thanks
---------------------------
Thanks to TVDBsimple.


