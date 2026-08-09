# Anime Renamer

A **FREE**, simple command-line renamer for anime files (a free alternative to
FileBot). It fetches metadata from [TheTVDB](https://thetvdb.com) and renames,
organises and tags your episodes automatically.

Tested anime: Naruto, One Piece, Gintama, The Promised Neverland, Angel Beats!,
Demon Slayer, and many more.

---

## Features

- Works on **Windows, Linux and macOS** (Python 3.6+).
- Understands many real-world file naming conventions (`S01E02`, `1x02`,
  `EP12`, bare numbers, fansub tags, ...).
- Renames to a clean, media-server friendly layout (`Series - S01E02 - Name`).
- Sorts episodes into `Season N` folders (specials go to `Specials`).
- Downloads poster/banner/fanart + per-episode thumbnails and `.nfo` sidecars
  (Plex, Jellyfin, Kodi, Emby).
- Reliable **rollback** that restores your original layout exactly.
- Handles subtitles, nested folders and name collisions.

Found a bug or have an idea? Please open an issue or pull request.

---

## Prerequisites

You need **Python 3.6 or newer** and an internet connection (to reach
TheTVDB).

### Install Python

| OS       | How to get Python 3                                                                 |
| -------- | ---------------------------------------------------------------------------------- |
| Windows  | Download from <https://www.python.org/downloads/> and tick **"Add Python to PATH"**. The `python` command is then available. |
| Linux    | Use your package manager, e.g. `sudo apt install python3 python3-pip` (Debian/Ubuntu) or `sudo dnf install python3` (Fedora). The command is usually **`python3`**. |
| macOS    | Install from <https://www.python.org/downloads/> or with Homebrew: `brew install python`. The command is usually **`python3`**. |

> **`python` vs `python3`:** On Windows the command is `python`. On most Linux
> and macOS setups it is `python3`. In the commands below, use whichever your
> system provides. (Likewise use `pip` on Windows and `pip3` on Linux/macOS,
> or always prefer `python -m pip ...` / `python3 -m pip ...`.)

---

## How to use

Pick **one** of the methods below. Then `cd` into the **base folder** of the
series (the folder that contains your episodes / season sub-folders) and run
the tool from there.

### Method 1 — Install from PyPI (recommended)

**Windows (Command Prompt / PowerShell):**
```powershell
pip install anime-renamer
cd "C:\Anime\Naruto"
anime_renamer
```

**Linux / macOS (Terminal):**
```bash
pip3 install anime-renamer
cd ~/Anime/Naruto
anime_renamer
```

### Method 2 — Install from source (clone this repo)

```bash
git clone https://github.com/kud04rk/anime-renamer.git
cd anime-renamer

# Windows
pip install .

# Linux / macOS
pip3 install .
```

Then run, from inside your series folder:

```bash
anime_renamer                 # any OS, after install
# or, without the console command:
python -m anime_renamer       # Windows
python3 -m anime_renamer      # Linux / macOS
```

### Method 3 — Copy & run (no installation)

If you do not want to install anything:

1. Install the two dependencies:

   ```powershell
   pip install tvdbsimple requests        # Windows
   ```
   ```bash
   pip3 install tvdbsimple requests       # Linux / macOS
   ```

2. Copy **every `.py` file** from the `anime_renamer/` folder into the base
   folder of your series.
3. From that folder run:

   ```powershell
   python main.py        # Windows
   ```
   ```bash
   python3 main.py       # Linux / macOS
   ```

---

## Supported file name formats

The only hard requirement is that each file name contains a recognisable
episode number. The tool understands, among others:

| Example input                              | Recognised as |
| ------------------------------------------ | ------------- |
| `356.mp4`                                   | absolute 356  |
| `[Group] Title - 356 [720p].mkv`           | absolute 356  |
| `Title S01E02.mkv` / `Title s1 e2.mkv`     | S01E02        |
| `Title 1x02.mkv`                           | S01E02        |
| `Title EP12.mkv` / `Title Episode 12.mkv`  | absolute 12   |
| `Title - 12 END.mkv`                       | absolute 12   |
| `Title.S01E02.1080p.mkv`                   | S01E02        |
| `One Piece - 1014 [1080p].mkv`             | absolute 1014 |

> Tip: if a name is messy, use the **Remove text** stage (type `tags`) to strip
> `[Group]`, `(720p)`, codec and resolution tags first.

---

## The interactive workflow

When you launch the tool it first asks:

```
Roll back a previous run instead? (y/N):
```

Answer `n` for a normal run. You'll then type the anime name, pick the correct
series from the search results by number, and step through each stage. You can
skip any stage with `n`.

1. **Prepare folder** — flattens the directory tree. Every video **and its
   subtitle** found anywhere below the current folder is moved into the base
   folder. Empty sub-folders are removed; same-name files from different
   sub-folders get an automatic `(1)`, `(2)`... suffix.
2. **Remove text** — strips unwanted text. Remove several strings at once
   (separate with `|`), use a regular expression, or type `tags` to remove
   common release-group noise in one pass. Runs in a loop so you can clean
   names step by step.
3. **Rename episodes** — matches each file against TheTVDB (by season+episode
   **or** by absolute number) and renames it to:
   ```
   Series - S01E02 - Episode Name.ext
   ```
4. **Organise into season folders** — moves renamed files into `Season 1`,
   `Season 2`, ... (specials → `Specials`).
5. **Download metadata** — downloads series poster/banner/fanart, a thumbnail
   for each episode, and writes `.nfo` sidecar files.

If a network/API error occurs during the online stages (rename / metadata),
the tool reports it cleanly instead of crashing — just retry that stage.

---

## Rollback

Every move and rename performed by **any** stage is recorded in a hidden
`.anime_renamer_log.json` file next to your media. If you do not like the
result, re-run the tool and answer `y` to the first **Roll back** prompt — it
reverses every operation in the correct order and restores your original
layout exactly (including nested folders).

You can also roll back directly:

```powershell
python -m anime_renamer.rollback     # Windows (installed)
python rollback.py                   # Windows (copy & run)
```
```bash
python3 -m anime_renamer.rollback    # Linux / macOS (installed)
python3 rollback.py                  # Linux / macOS (copy & run)
```

---

## Tips

- **Always test on one episode first.** Copy a single file to a separate
  folder and run the tool there before processing a whole series.
- TheTVDB API key is bundled, so no configuration is needed. It is a shared
  public key; if you hit rate limits, wait a little and retry.
- Network-dependent stages (rename, metadata) need an internet connection.
- File names are sanitised for the strictest OS (Windows) so your library
  stays portable when copied between Windows, Linux and macOS.

---

## Contributing

Contributions are welcome.

```
fork -> clone -> branch -> commit (with clear messages) -> pull request
```

---

## To-DO

1. GUI / Electron app for ease of use.
2. Support even more exotic naming conventions.

---

## Thanks

- [TVDBsimple](https://github.com/sheffieldjack/tvdbsimple)
- [TheTVDB](https://thetvdb.com)
