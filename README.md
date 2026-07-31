## Anime Renamer

---

Anime Renamer is a FREE, simple to use command line renamer for anime files
(similar to FileBot, which is now paid). It is powered by
[TheTVDB](https://thetvdb.com) metadata.

Any issues with the code please write in the issues section (comments,
feedback or enhancement are also welcome).

Personally used for many anime:

1. Naruto
2. One Piece
3. Gintama
4. Promised Neverland
5. Angel Beats
6. Demon Slayer
... and many more.

## Platform support

Anime Renamer now works on **Windows, Linux and macOS**. It only needs
Python 3.6+ and an internet connection (to reach TheTVDB).

## CONTRIBUTE

PLEASE TRY WITH ONE EPISODE BEFORE TRYING WITH COMPLETE SERIES.
(Copy the file to a different folder and try there first.)

## HOW TO USE

### Install method (recommended, all operating systems)

```bash
pip install anime-renamer        # or: pip install .
anime_renamer                    # run inside the base folder of the series
```

You can also run it without installing the console script:

```bash
python -m anime_renamer          # from the repo root, inside the series folder
```

### Copy & run method (no install)

1. Install the dependencies: `pip install tvdbsimple requests`
2. Copy every `.py` file from the `anime_renamer` folder into the base folder
   of the series.
3. Run `python main.py`

### Windows users

You can still download the `.exe` from releases and run it in the folder with
the series, or use any of the methods above.

## Prerequisites

The only hard requirement is that each file name must contain an episode
number that the tool can recognise. It now understands a wide variety of
real-world naming conventions, for example:

| Input file name                              | Recognised as |
| -------------------------------------------- | ------------- |
| `356.mp4`                                     | absolute 356  |
| `[Group] Title - 356 [720p].mkv`             | absolute 356  |
| `Title S01E02.mkv` / `Title s1 e2.mkv`       | S01E02        |
| `Title 1x02.mkv`                             | S01E02        |
| `Title EP12.mkv` / `Title Episode 12.mkv`    | absolute 12   |
| `Title - 12 END.mkv`                         | absolute 12   |

## Detailed explanation [MUST READ]

When you start the tool it will ask whether you want to **roll back** a
previous run first. Answer `n` to perform a normal run. You will then be
asked for the anime name, pick the correct series from the search results,
and then walk through each stage (you can skip any stage with `n`):

1. **Prepare folder** - flattens the directory tree. Every video **and its
   subtitle** file found anywhere below the current folder is moved into the
   base folder. Empty sub-folders are removed and name collisions between
   files coming from different sub-folders are resolved automatically.

2. **Remove text** - strips unwanted text from file names. You can remove
   several strings at once (separate them with `|`), use a regular
   expression, or type `tags` to remove common release-group noise
   (`[Group]`, `(720p)`, codec tags, etc.) in one pass. Runs in a loop so you
   can clean names incrementally.

3. **Rename episodes** - matches each file against TheTVDB (by season+episode
   **or** by absolute number) and renames it to a clean, media-server
   friendly layout:
   ```
   Series - S01E02 - Episode Name.ext
   ```

4. **Organise into season folders** - moves the renamed files into
   `Season 1`, `Season 2`, ... folders (specials go into `Specials`).

5. **Download metadata** - downloads the series poster/banner/fanart, a
   thumbnail for each episode, and writes `.nfo` sidecar files understood by
   Plex, Jellyfin, Kodi and Emby.

## Rollback

Every rename/move performed by any stage is recorded in a hidden
`.anime_renamer_log.json` file. If you do not like the result, just re-run
the tool and choose **Roll back** at the first prompt - it reverses every
operation in the correct order and restores your original layout exactly.
You can also run rollback directly:

```bash
python -m anime_renamer.rollback      # installed
python rollback.py                    # copy & run method
```

## Developer

Please contribute.

fork -> clone -> branch -> commit with proper comments.

## TO-DO

1. Electron / GUI app for ease of use.
2. Even more exotic naming conventions.

## Thanks

Thanks to TVDBsimple and TheTVDB.
