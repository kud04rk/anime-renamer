"""Interactive pipeline that ties every stage together.

Both entry points (``python -m anime_renamer`` and the standalone
``main.py``) delegate here so the flow is defined once.  Every stage is
invoked as a direct function call - never via ``os.system`` - which makes the
tool work identically on Windows, Linux and macOS.
"""

import tvdbsimple as tvdb

tvdb.KEYS.API_KEY = "UB0SOLRB8XH3I39L"

# Import the stage functions.  Works both as an installed package and when the
# .py files are copied loose next to main.py.
try:
    from anime_renamer.prepare import preparefiles
    from anime_renamer.remover import scancurrentfolder
    from anime_renamer.renamer import mainpackage as rename_episodes
    from anime_renamer.organiser import move_files
    from anime_renamer.downloader import mainpackage as download_metadata
    from anime_renamer.rollback import rollback
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    from prepare import preparefiles
    from remover import scancurrentfolder
    from renamer import mainpackage as rename_episodes
    from organiser import move_files
    from downloader import mainpackage as download_metadata
    from rollback import rollback
    import utils


def _prompt(message):
    """Ask a yes/no question, returns True for yes."""
    answer = input(message).strip().lower()
    return answer in ("y", "yes")


def _run_network_stage(func, *args, **kwargs):
    """Run a stage that needs TheTVDB/network access, failing gracefully.

    Returns True on success, False if a network/API error occurred.
    """
    try:
        func(*args, **kwargs)
        return True
    except Exception as exc:  # noqa - broad: tvdbsimple raises bare Exception
        print("  ! TheTVDB / network error: {}".format(exc))
        return False


def _choose_series():
    """Search TheTVDB and let the user pick a series. Returns its id."""
    name = input("What's the name of the anime? (e.g. Naruto, One Piece) "
                 "Be precise with spelling/capitalisation: ").strip()
    while not name:
        name = input("Series name cannot be empty, try again: ").strip()

    results = tvdb.Search().series(name) or []
    if not results:
        print("No matches found for {!r}.".format(name))
        return _choose_series()

    print("\nFound {} match(es):\n".format(len(results)))
    for index, series in enumerate(results, start=1):
        utils.sep(width=60)
        print("No              : {}".format(index))
        print("Series name     : {}".format(series.get("seriesName", "?")))
        overview = series.get("overview")
        if overview:
            print("Overview        : {}".format(overview))
    utils.sep(width=60)

    while True:
        choice = input("\nEnter the NUMBER of the correct series: ").strip()
        try:
            picked = results[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice, try again.")
            continue
        break

    series_id = picked["id"]
    print("\nSelected: {} (id: {})".format(picked.get("seriesName", "?"), series_id))
    return series_id


def run_interactive():
    """Run the full interactive pipeline."""
    utils.sep()
    print("ANIME RENAMER".center(80))
    utils.sep()

    rollback_now = _prompt("Roll back a previous run instead? (y/N): ")
    if rollback_now:
        rollback()
        return

    series_id = _choose_series()
    utils.sep()

    # Stage 1 - flatten the folder structure.
    if _prompt("Prepare folder (flatten sub-folders)? (y/N): "):
        preparefiles()
    else:
        print("Skipping - assuming files are already in the base folder.")
    utils.sep()

    # Stage 2 - strip unwanted text (loop until satisfied).
    while _prompt("Remove text from file names? (y/N): "):
        scancurrentfolder()
    utils.sep()

    # Stage 3 - rename using TheTVDB metadata.
    if _prompt("Rename episodes with metadata? (y/N): "):
        if not _run_network_stage(rename_episodes, series_id):
            print("Rename could not be completed. Check your internet "
                  "connection / TheTVDB availability and try again.")
        else:
            print("Tip: any leftover files can be moved to another folder and "
                  "renamed separately.")
    utils.sep()

    # Stage 4 - organise into season folders.
    if _prompt("Organise into season folders? (y/N): "):
        move_files()
    utils.sep()

    # Stage 5 - download metadata.
    if _prompt("Download artwork & metadata (.nfo)? (y/N): "):
        if not _run_network_stage(download_metadata, series_id):
            print("Metadata download could not be completed. Check your "
                  "internet connection / TheTVDB availability and try again.")
    utils.sep()

    print("All done! If something looks off you can re-run and choose "
          "'Roll back' to undo everything.")
