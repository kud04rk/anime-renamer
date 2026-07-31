"""Shared helpers for anime_renamer.

Everything in here is deliberately free of side effects so it can be imported
safely on any platform (Windows, Linux, macOS) without touching the file
system.  The pipeline stages build on top of these helpers.
"""

import json
import os
import re
from datetime import datetime

try:
    from pathlib import Path
except ImportError:  # pragma: no cover - py2 fallback, not officially supported
    Path = None  # type: ignore


# ---------------------------------------------------------------------------
# Extension lists
# ---------------------------------------------------------------------------
VIDEO_EXTENSIONS = (
    ".mkv", ".mp4", ".avi", ".flv", ".mpg", ".mpeg", ".m4v",
    ".wmv", ".webm", ".vob", ".mov", ".3gp", ".ogv", ".ts", ".m2ts",
)

SUBTITLE_EXTENSIONS = (
    ".srt", ".ass", ".ssa", ".sub", ".vtt", ".idx", ".smi",
)

MEDIA_EXTENSIONS = VIDEO_EXTENSIONS + SUBTITLE_EXTENSIONS

# Hidden transaction log used to make rollback reliable across every stage.
LOG_FILENAME = ".anime_renamer_log.json"


# ---------------------------------------------------------------------------
# Path / filename helpers
# ---------------------------------------------------------------------------
def get_extension(filename):
    """Return the extension (including the dot) of *filename*, lower-cased.

    Returns an empty string when there is no extension.
    """
    base = os.path.basename(filename)
    idx = base.rfind(".")
    if idx == -1:
        return ""
    return base[idx:].lower()


def has_extension(filename, extensions):
    return get_extension(filename) in extensions


def is_video(filename):
    return has_extension(filename, VIDEO_EXTENSIONS)


def is_subtitle(filename):
    return has_extension(filename, SUBTITLE_EXTENSIONS)


def is_media(filename):
    return has_extension(filename, MEDIA_EXTENSIONS)


# Characters that are illegal on Windows. We strip them on every platform so
# that produced names stay portable when media is copied between OSes.
_ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
# Repeating whitespace / dots that often remain after stripping tags.
_MULTI_SPACE = re.compile(r"[\s_]{2,}")


def sanitize_filename(name):
    """Make *name* safe to use on Windows, Linux and macOS.

    Keeps it readable: illegal characters are replaced with sensible
    stand-ins (``:`` -> ``-``) and the result is trimmed.
    """
    if not name:
        return name
    name = name.replace(":", "-")
    name = name.replace("/", "-")
    name = name.replace("\\", "-")
    name = _ILLEGAL_CHARS.sub("", name)
    name = _MULTI_SPACE.sub(" ", name)
    return name.strip(" ._-")


def unique_path(target_path):
    """Return a path that does not exist yet, near *target_path*.

    If ``target_path`` is free it is returned unchanged, otherwise a numeric
    suffix is inserted before the extension (``foo.mkv`` -> ``foo (1).mkv``).
    """
    if not os.path.exists(target_path):
        return target_path
    directory = os.path.dirname(target_path) or "."
    base = os.path.basename(target_path)
    stem, ext = os.path.splitext(base)
    index = 1
    while True:
        candidate = os.path.join(directory, "{} ({}){}".format(stem, index, ext))
        if not os.path.exists(candidate):
            return candidate
        index += 1


def safe_rename(src, dst, log=True):
    """Rename *src* -> *dst* without clobbering an existing *dst*.

    On a collision a unique suffix is added to *dst*.  Every successful move
    is recorded in the transaction log so rollback can reverse it.

    Returns the path that was actually written.
    """
    src = os.path.abspath(src)
    dst = unique_path(os.path.abspath(dst))
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    try:
        os.rename(src, dst)
    except OSError as exc:
        print("  ! could not rename {} ({}). Skipped.".format(src, exc))
        return None
    if log:
        log_rename(src, dst)
    return dst


def ensure_dir(path):
    """Create *path* (and parents) if it does not exist. Idempotent."""
    if path and not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# Transaction log (powers reliable rollback)
# ---------------------------------------------------------------------------
def _log_path(base=None):
    base = base or os.getcwd()
    return os.path.join(base, LOG_FILENAME)


def log_rename(src, dst):
    """Append a single rename record to the transaction log."""
    record = {"src": os.path.abspath(src), "dst": os.path.abspath(dst),
              "time": datetime.now().isoformat(timespec="seconds")}
    data = {"operations": []}
    try:
        with open(_log_path(), "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (IOError, OSError, ValueError):
        data = {"operations": []}
    data.setdefault("operations", []).append(record)
    try:
        with open(_log_path(), "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    except OSError as exc:
        print("  ! could not write rename log ({})".format(exc))


def load_log(base=None):
    """Return the list of recorded operations (oldest first)."""
    try:
        with open(_log_path(base), "r", encoding="utf-8") as handle:
            return json.load(handle).get("operations", [])
    except (IOError, OSError, ValueError):
        return []


def clear_log(base=None):
    """Remove the transaction log file."""
    try:
        os.remove(_log_path(base))
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Episode number extraction
# ---------------------------------------------------------------------------
# Ordered: the first pattern that matches wins. Season+episode forms first,
# then explicit "EP/Episode" markers, finally a bare-number fallback.
_SEASON_EPISODE_PATTERNS = [
    re.compile(r"[sS](\d{1,2})\s*[eE](\d{1,4})"),            # S01E02 / s1 e2
    re.compile(r"(?<![\d])(\d{1,2})[xX](\d{1,4})(?!\d)"),    # 1x02
    re.compile(r"season\s*(\d{1,2})\s*(?:episode|ep\.?|e)\s*(\d{1,4})", re.I),
]

_EPISODE_MARKER_PATTERNS = [
    re.compile(r"\bepisode\s*#?\s*(\d{1,4})\b", re.I),
    re.compile(r"\beps?\s*(\d{1,4})\b", re.I),               # EP12 / Ep. 12
    re.compile(r"\beps?\s*\.?\s*(\d{1,4})\b", re.I),
    re.compile(r"\b(\d{1,4})v\d\b", re.I),                   # 03v2 (versioned)
]

# Things to strip before falling back to bare-number detection.
_STRIP_TAGS = [
    re.compile(r"\[[^\]]*\]"),        # [Group] [720p]
    re.compile(r"\([^)]*\)"),         # (720p) (x264)
    re.compile(r"\{[^}]*\}"),         # {comment}
    re.compile(r"\b\d{3,4}p\b", re.I),    # 720p / 1080p
    re.compile(r"\b(?:x|h)\.?26[45]\b", re.I),
    re.compile(r"\b(?:19|20)\d{2}\b"),     # years
    re.compile(r"\b(?:bluray|bdrip|dvdrip|webrip|web-dl|webdl|hdtv|remux)\b", re.I),
    re.compile(r"\b(?:truehd|aac|ac3|dts|flac|mp3)\d?\b", re.I),
    re.compile(r"\b(10bit|8bit|hi10|hi10p)\b", re.I),
]


def _strip_tags(stem):
    cleaned = stem
    for pattern in _STRIP_TAGS:
        cleaned = pattern.sub(" ", cleaned)
    cleaned = cleaned.replace(".", " ").replace("_", " ")
    cleaned = _MULTI_SPACE.sub(" ", cleaned).strip()
    return cleaned


def extract_episode_info(filename):
    """Parse an episode number out of *filename*.

    Returns a dict describing what was found:

    * ``{"kind": "season", "season": int, "episode": int}``
    * ``{"kind": "absolute", "number": int}``
    * ``None`` when nothing usable was found.

    Handles, among others::

        356.mp4
        [Group] Title - 356 [720p].mkv
        Title S01E02.mkv
        Title s1 e2.mkv
        Title 1x02.mkv
        Title EP12.mkv / Episode 12.mkv / E12.mkv
        Title - 12 END.mkv
    """
    stem = os.path.basename(filename)
    # Strip a trailing extension only when it looks like one (short, no
    # spaces) so dotted names such as "Title.S01E02" survive intact.
    dot = stem.rfind(".")
    if dot != -1:
        suffix = stem[dot + 1:]
        if 0 < len(suffix) <= 4 and " " not in suffix and suffix.isalnum():
            stem = stem[:dot]
    # Treat dots / underscores as word separators (e.g. "Title.S01E02").
    stem = stem.replace(".", " ").replace("_", " ")

    # 1) season + episode forms
    for pattern in _SEASON_EPISODE_PATTERNS:
        match = pattern.search(stem)
        if match:
            season = int(match.group(1))
            episode = int(match.group(2))
            if season >= 0 and episode > 0:
                return {"kind": "season", "season": season, "episode": episode}

    # 2) explicit episode markers (EP / Episode / E)
    for pattern in _EPISODE_MARKER_PATTERNS:
        match = pattern.search(stem)
        if match:
            return {"kind": "absolute", "number": int(match.group(1))}

    # 3) bare-number fallback: strip noise tags, collect remaining integers.
    cleaned = _strip_tags(stem)
    candidates = [int(n) for n in re.findall(r"\b\d{1,4}\b", cleaned)]
    # filter out obvious non-episode noise that survived stripping
    candidates = [n for n in candidates if 0 < n < 10000 and n not in (480, 720, 1080)]
    if candidates:
        # The episode number is most often the last meaningful number left.
        return {"kind": "absolute", "number": candidates[-1]}

    return None


def describe_episode_info(info):
    """Human readable label for an extract_episode_info result."""
    if not info:
        return "unknown"
    if info["kind"] == "season":
        return "S{:02d}E{:02d}".format(info["season"], info["episode"])
    return "abs {}".format(info["number"])


def sep(char="-", width=80):
    print(char * width)
