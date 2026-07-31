"""Stage 3 - rename episodes using TheTVDB metadata.

Unlike the original version (which only understood files named as a bare
number, e.g. ``356.mp4``), this stage understands many real-world naming
conventions::

    356.mp4
    [Group] Title - 356 [720p].mkv
    Title S01E02.mkv / Title s1 e2.mkv
    Title 1x02.mkv
    Title EP12.mkv / Episode 12.mkv / E12.mkv
    Title - 12 END.mkv

Files are matched against TheTVDB either by season+episode (when the name
contains ``S01E02`` / ``1x02``) or by absolute number.  Output names follow a
clean, media-server friendly layout::

    Series - S01E02 - Episode Name.ext
"""

import os
import sys

import tvdbsimple as tvdb

try:
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    import utils

tvdb.KEYS.API_KEY = "UB0SOLRB8XH3I39L"

# Output name pattern.  Kept parseable so organiser/downloader/rollback can
# read the season back out of it.
NAME_TEMPLATE = "{series} - S{season:02d}E{episode:02d} - {title}"


class SourceFile(object):
    """A media file discovered locally together with its parsed episode info."""

    def __init__(self, filename, info, extension):
        self.filename = filename
        self.info = info
        self.extension = extension

    def __repr__(self):
        return "<SourceFile {} {}>".format(self.filename,
                                           utils.describe_episode_info(self.info))


# ---------------------------------------------------------------------------
# TheTVDB helpers
# ---------------------------------------------------------------------------
def get_series_details(seriesid):
    """Print a short summary of the selected series."""
    show = tvdb.Series(seriesid)
    info = show.info()
    utils.sep()
    print("Series name : ", info.get("seriesName", "?"))
    overview = info.get("overview") or "(no overview available)"
    print("Overview    : ", overview)
    utils.sep()
    return info


def _episode_maps(seriesid):
    """Return ``(absolute_map, season_map, episodes)`` for a series."""
    episodes = tvdb.Series_Episodes(seriesid).all() or []

    absolute_map = {}
    season_map = {}
    for ep in episodes:
        season = ep.get("airedSeason")
        number = ep.get("airedEpisodeNumber")
        if season is not None and number is not None:
            season_map[(int(season), int(number))] = ep
        absolute = ep.get("absoluteNumber")
        if absolute is not None:
            absolute_map[int(absolute)] = ep
    return absolute_map, season_map, episodes


# ---------------------------------------------------------------------------
# Scanning & matching
# ---------------------------------------------------------------------------
def scan_folder(path):
    """Collect media files in *path* together with parsed episode info."""
    sources = []
    skipped = []
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if not os.path.isfile(full) or not utils.is_media(name):
            continue
        info = utils.extract_episode_info(name)
        if info is None:
            skipped.append(name)
            continue
        sources.append(SourceFile(name, info, utils.get_extension(name)))
    if skipped:
        print("  No episode number found in:")
        for name in skipped:
            print("    - {}".format(name))
    return sources


def _lookup(source, absolute_map, season_map):
    """Find the matching TVDB episode record for *source*, or ``None``."""
    info = source.info
    if info["kind"] == "season":
        ep = season_map.get((info["season"], info["episode"]))
        if ep:
            return ep
    if info["kind"] in ("season", "absolute"):
        ep = absolute_map.get(info["number"])
        if ep:
            return ep
    return None


def make_filename(series, season, episode, title):
    """Build a clean, cross-platform safe output file name (no extension)."""
    safe_series = utils.sanitize_filename(str(series)) or "Unknown"
    safe_title = utils.sanitize_filename(str(title)) if title else ""
    if not safe_title:
        safe_title = "Episode {:02d}".format(episode)
    return NAME_TEMPLATE.format(series=safe_series, season=season,
                                episode=episode, title=safe_title)


def match_filenames(sources, seriesid):
    """Rename *sources* according to TheTVDB metadata."""
    absolute_map, season_map, episodes = _episode_maps(seriesid)

    renamed = 0
    unmatched = 0
    folder = os.getcwd()

    for source in sources:
        ep = _lookup(source, absolute_map, season_map)
        if ep is None:
            unmatched += 1
            print("  ! no TVDB match for {} ({}). Left unchanged."
                  .format(source.filename,
                          utils.describe_episode_info(source.info)))
            continue

        season = int(ep.get("airedSeason") or 1)
        episode = int(ep.get("airedEpisodeNumber") or 0)
        title = ep.get("episodeName") or ""

        new_stem = make_filename(get_series_name(seriesid), season, episode, title)
        new_name = new_stem + source.extension

        src = os.path.join(folder, source.filename)
        dst = utils.safe_rename(src, os.path.join(folder, new_name))
        if dst:
            renamed += 1
            print("  {}  ->  {}".format(source.filename, os.path.basename(dst)))

    print("Done. {} renamed, {} unmatched.".format(renamed, unmatched))
    return renamed, unmatched


# Tiny cached accessor so we don't re-fetch the series name per file.
_SERIES_NAME_CACHE = {}


def get_series_name(seriesid):
    if seriesid not in _SERIES_NAME_CACHE:
        try:
            _SERIES_NAME_CACHE[seriesid] = tvdb.Series(seriesid).info().get("seriesName", "Unknown")
        except Exception:
            _SERIES_NAME_CACHE[seriesid] = "Unknown"
    return _SERIES_NAME_CACHE[seriesid]


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------
def run(seriesid, path=None):
    """Full rename pass for *seriesid* inside *path* (default: cwd)."""
    path = path or os.getcwd()
    get_series_details(seriesid)
    sources = scan_folder(path)
    print("Found {} candidate file(s).".format(len(sources)))
    if not sources:
        print("Nothing to rename.")
        return 0, 0
    return match_filenames(sources, seriesid)


def main(seriesid):
    return run(seriesid)


def mainpackage(seriesid):
    return run(seriesid)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python renamer.py <seriesid>")
