"""Stage 5 - download metadata (artwork + NFO).

Downloads the series poster / banner / fanart and a thumbnail for every
episode that has a matching local file, and writes ``.nfo`` sidecar files
that media servers (Plex, Jellyfin, Kodi, Emby) understand.

Robust against missing artwork (some episodes have no thumbnail on TheTVDB)
and against network errors.  Cross-platform path handling throughout.
"""

import os
import re
import sys

import requests
import tvdbsimple as tvdb
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

try:
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    import utils

tvdb.KEYS.API_KEY = "UB0SOLRB8X3I39L"

IMAGE_BASE = "https://www.thetvdb.com/banners/"
_SEASON_EPISODE = re.compile(r"[sS](\d{1,2})\s*[eE](\d{1,4})")


# ---------------------------------------------------------------------------
# Low level helpers
# ---------------------------------------------------------------------------
def download_image(url_path, output_path):
    """Download *url_path* (relative to IMAGE_BASE) to *output_path*.

    Silently skips empty URLs and reports (but survives) network errors.
    """
    if not url_path:
        return False
    full_url = IMAGE_BASE + url_path.lstrip("/")
    try:
        response = requests.get(full_url, stream=True, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        print("  ! could not download {} ({})".format(full_url, exc))
        return False
    with open(output_path, "wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                handle.write(chunk)
    print("  downloaded: {}".format(os.path.basename(output_path)))
    return True


def _pretty_xml(root_element):
    rough = ET.tostring(root_element, encoding="unicode")
    return minidom.parseString(rough).toprettyxml(indent="  ")


def write_nfo(nfo_element, output_path):
    """Write *nfo_element* (an ``ElementTree.Element``) to *output_path*."""
    try:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(_pretty_xml(nfo_element))
        print("  wrote: {}".format(os.path.basename(output_path)))
    except OSError as exc:
        print("  ! could not write {} ({})".format(output_path, exc))


# ---------------------------------------------------------------------------
# Series level
# ---------------------------------------------------------------------------
def download_series_data(seriesid, folder=None):
    """Download series artwork + tvshow.nfo into *folder* (default cwd)."""
    folder = folder or os.getcwd()
    utils.ensure_dir(folder)

    show = tvdb.Series(seriesid)
    info = show.info()
    title = info.get("seriesName") or "Unknown"
    plot = info.get("overview") or ""

    # tvshow.nfo
    tvshow = ET.Element("tvshow")
    ET.SubElement(tvshow, "title").text = title
    ET.SubElement(tvshow, "plot").text = plot
    ET.SubElement(tvshow, "id").text = str(seriesid)
    write_nfo(tvshow, os.path.join(folder, "tvshow.nfo"))

    # Artwork - each is optional on TheTVDB.
    banner = info.get("banner")
    if banner:
        download_image(banner, os.path.join(folder, "banner.jpg"))

    try:
        posters = show.Images.poster() or []
        if posters:
            download_image(posters[0].get("fileName"), os.path.join(folder, "poster.jpg"))
    except Exception as exc:  # noqa - tvdbsimple raises a bare Exception
        print("  ! poster unavailable ({})".format(exc))

    try:
        fanarts = show.Images.fanart() or []
        if fanarts:
            download_image(fanarts[0].get("fileName"), os.path.join(folder, "fanart.jpg"))
    except Exception as exc:  # noqa - tvdbsimple raises a bare Exception
        print("  ! fanart unavailable ({})".format(exc))

    return title


# ---------------------------------------------------------------------------
# Episode level
# ---------------------------------------------------------------------------
def _build_episode_maps(seriesid):
    episodes = tvdb.Series_Episodes(seriesid).all() or []
    season_map = {}
    for ep in episodes:
        season = ep.get("airedSeason")
        number = ep.get("airedEpisodeNumber")
        if season is not None and number is not None:
            season_map[(int(season), int(number))] = ep
    return season_map


def download_episode_data(seriesid, root=None):
    """Download a thumbnail + .nfo next to every matched episode file."""
    root = root or os.getcwd()
    season_map = _build_episode_maps(seriesid)

    processed = 0
    missing = 0

    for current, _dirs, files in os.walk(root):
        for name in files:
            if not utils.is_video(name):
                continue
            match = _SEASON_EPISODE.search(name)
            if not match:
                continue
            season, episode = int(match.group(1)), int(match.group(2))
            ep = season_map.get((season, episode))
            if not ep:
                missing += 1
                continue

            base, _ext = os.path.splitext(os.path.join(current, name))

            thumb = ep.get("filename")
            if thumb:
                download_image(thumb, base + ".jpg")

            nfo = ET.Element("episodedetails")
            ET.SubElement(nfo, "title").text = ep.get("episodeName") or ""
            ET.SubElement(nfo, "season").text = str(season)
            ET.SubElement(nfo, "episode").text = str(episode)
            ET.SubElement(nfo, "plot").text = ep.get("overview") or ""
            ET.SubElement(nfo, "aired").text = ep.get("firstAired") or ""
            write_nfo(nfo, base + ".nfo")
            processed += 1

    print("Done. {} episode(s) processed, {} unmatched.".format(processed, missing))
    return processed, missing


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------
def run(seriesid, root=None):
    title = download_series_data(seriesid, root)
    print("Series: {}".format(title))
    download_episode_data(seriesid, root)


def main(seriesid):
    return run(seriesid)


def mainpackage(seriesid):
    return run(seriesid)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python downloader.py <seriesid>")
