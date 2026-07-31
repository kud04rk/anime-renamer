"""Stage 2 - strip unwanted text from file names.

Lets the user remove one or more substrings (or a regular expression) from
the names of every media file in the current folder.  Common release-group
noise (``[Group]``, ``(720p)``, resolution / codec tags) can be removed in a
single pass with the built-in ``--tags`` shorthand.

Cross-platform: paths are built with ``os.path`` and every rename is logged
so it can be undone by rollback.
"""

import os
import re

try:
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    import utils


# A ready-made pattern that strips the usual fansub/release-group noise.
TAG_PATTERN = re.compile(
    r"(\[[^\]]*\]|\([^)]*\)|\{[^}]*\})"        # bracketed groups
    r"|(\b\d{3,4}p\b)"                          # resolutions 720p/1080p
    r"|(\b(?:x|h)\.?26[45]\b)"                  # codecs
    r"|(\b(?:bluray|bdrip|dvdrip|webrip|web-?dl|webdl|hdtv|remux)\b)"
    r"|(\b(?:aac|ac3|flac|mp3|truehd|dts)\d?\b)"
    r"|(\b(?:10bit|8bit|hi10p?)\b)",
    re.IGNORECASE,
)


def _apply_removal(stem, strings, use_regex):
    """Return *stem* after removing every entry in *strings*."""
    result = stem
    for token in strings:
        token = token.strip()
        if not token:
            continue
        if use_regex:
            try:
                result = re.sub(token, " ", result)
            except re.error as exc:
                print("  ! invalid regex {!r}: {} - skipped.".format(token, exc))
        else:
            result = result.replace(token, " ")
    # Tidy up double separators / dangling punctuation left behind.
    result = result.replace(".", " ").replace("_", " ")
    result = re.sub(r"\s{2,}", " ", result)
    return result.strip(" -._")


def scancurrentfolder(strings=None, use_regex=False, strip_tags=False):
    """Rename media files in the current folder by removing text.

    Parameters
    ----------
    strings : list[str] | None
        Substrings / patterns to remove.  When *None* the user is prompted
        interactively (legacy behaviour).
    use_regex : bool
        Treat *strings* as regular expressions.
    strip_tags : bool
        Additionally strip common release-group tags.
    """
    interactive = strings is None
    if interactive:
        raw = utils_input("String(s) to remove (separate multiple with '|', "
                          "or type 'tags' for built-in noise removal): ")
        if raw.strip().lower() == "tags":
            strip_tags = True
            strings = []
        else:
            strings = [s for s in raw.split("|") if s.strip()]
        regex_answer = utils_input("Treat them as regex? (y/N): ")
        use_regex = regex_answer.strip().lower() == "y"

    if strip_tags:
        # Use the compiled tag pattern as an extra "regex" removal.
        strings = list(strings or []) + [TAG_PATTERN.pattern]
        use_regex = True

    renamed = 0
    unchanged = 0
    folder = os.getcwd()

    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not os.path.isfile(path) or not utils.is_media(name):
            continue

        stem, ext = os.path.splitext(name)
        new_stem = _apply_removal(stem, strings, use_regex)
        if not new_stem:
            # Never produce an empty name - fall back to the original stem.
            print("  ! '{}' would become empty, keeping original.".format(name))
            unchanged += 1
            continue
        new_name = new_stem + ext
        if new_name == name:
            unchanged += 1
            continue

        dst = utils.safe_rename(path, os.path.join(folder, new_name))
        if dst:
            renamed += 1
            print("  {}  ->  {}".format(name, os.path.basename(dst)))

    print("Done. {} file(s) renamed, {} unchanged.".format(renamed, unchanged))
    return renamed, unchanged


def utils_input(prompt):
    """Local ``input`` wrapper kept separate so it can be mocked in tests."""
    return input(prompt)


if __name__ == "__main__":
    scancurrentfolder()
