"""Stage 4 - sort renamed files into per-season folders.

Reads the ``S01E02`` token that the renamer writes into every file name and
moves the file into a ``Season 1`` folder (created on demand).  Falls back to
parsing the legacy ``Ep-N S-E`` layout for files produced by older runs.

Cross-platform path handling and automatic collision resolution are used
throughout, and every move is logged for rollback.
"""

import os
import re

try:
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    import utils

# Primary layout produced by renamer.py: "Series - S01E02 - Name.ext"
_SEASON_EPISODE = re.compile(r"[sS](\d{1,2})\s*[eE](\d{1,3})")
# Legacy layout: "Series Ep-5 S1E5 - Name.ext"
_LEGACY_SEASON = re.compile(r"S\s*(\d{1,2})\s*E", re.I)


def get_season(filename):
    """Return the season number found in *filename*, or ``None``."""
    match = _SEASON_EPISODE.search(filename) or _LEGACY_SEASON.search(filename)
    if match:
        return int(match.group(1))
    return None


def season_folder(base, season):
    """Return (and create) the folder path for *season* under *base*.

    Season 0 (specials) maps to a ``Specials`` folder.
    """
    name = "Specials" if season == 0 else "Season {}".format(season)
    path = os.path.join(base, name)
    utils.ensure_dir(path)
    return path


def move_files(root=None):
    """Move every media file in *root* into its season folder."""
    root = os.path.abspath(root or os.getcwd())
    print("Organising files in: {}".format(root))

    moved = 0
    skipped = 0

    for name in sorted(os.listdir(root)):
        src = os.path.join(root, name)
        if not os.path.isfile(src) or not utils.is_media(name):
            continue

        season = get_season(name)
        if season is None:
            print("  ! could not determine season for {}, left in place.".format(name))
            skipped += 1
            continue

        target_dir = season_folder(root, season)
        dst = utils.safe_rename(src, os.path.join(target_dir, name))
        if dst:
            moved += 1
            print("  {}  ->  {}/".format(name, os.path.basename(target_dir)))

    print("Done. {} file(s) organised, {} skipped.".format(moved, skipped))
    return moved, skipped


if __name__ == "__main__":
    move_files()
