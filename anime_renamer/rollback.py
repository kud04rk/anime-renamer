"""Rollback - undo every file move/rename performed by the pipeline.

Previous versions tried to parse the *output* file name to guess the original
name, which broke the moment renaming failed or produced an unexpected name.
This version reads the hidden transaction log (``.anime_renamer_log.json``)
written by every stage and reverses each operation in reverse order, which
always restores the exact original layout - regardless of which stage
produced the name.
"""

import os

try:
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    import utils


def rollback(base=None, keep_log=False):
    """Reverse every recorded rename in *base* (default cwd).

    Operations are applied newest-first so the original tree is restored even
    when multiple stages ran on top of each other.
    """
    base = os.path.abspath(base or os.getcwd())
    operations = utils.load_log(base)

    if not operations:
        print("No rename history found in {} - nothing to roll back.".format(base))
        return 0

    print("Rolling back {} operation(s)...".format(len(operations)))
    undone = 0
    failed = 0

    for record in reversed(operations):
        src = record.get("dst")   # current location (where it was moved to)
        dst = record.get("src")   # original location (where it came from)
        if not src or not dst:
            continue
        if not os.path.exists(src):
            # Already moved / deleted - nothing to do here.
            continue

        # Make sure the destination directory exists (a flattened sub-folder may
        # have been removed during prepare).
        utils.ensure_dir(os.path.dirname(dst))

        try:
            # Never clobber an existing file at the destination.
            if os.path.exists(dst) and os.path.abspath(src) != os.path.abspath(dst):
                dst = utils.unique_path(dst)
            os.rename(src, dst)
            undone += 1
            print("  {}  ->  {}".format(os.path.relpath(src, base),
                                         os.path.relpath(dst, base)))
        except OSError as exc:
            failed += 1
            print("  ! failed to restore {} ({}).".format(src, exc))

    # Tidy up any season / specials folders left empty by the reversal.
    _remove_empty_folders(base)

    if not keep_log:
        utils.clear_log(base)

    print("Done. {} operation(s) reversed, {} failed.".format(undone, failed))
    return undone


def _remove_empty_folders(base):
    """Delete empty ``Season N`` / ``Specials`` folders under *base*."""
    for name in os.listdir(base):
        child = os.path.join(base, name)
        if not os.path.isdir(child):
            continue
        lower = name.lower()
        if not (lower.startswith("season ") or lower == "specials"):
            continue
        try:
            if not os.listdir(child):
                os.rmdir(child)
                print("  removed empty folder: {}".format(name))
        except OSError:
            pass


if __name__ == "__main__":
    rollback()
