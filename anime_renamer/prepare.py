"""Stage 1 - prepare the working folder.

Recursively flattens the directory tree: every video (and its sibling
subtitle) file found anywhere below the current folder is moved into the
root of the current folder.  Empty folders that become empty afterwards are
removed.  Name collisions between files coming from different sub-folders are
resolved automatically by appending a numeric suffix.

Works on Windows, Linux and macOS thanks to ``os.path`` based path handling.
"""

import os
import shutil

try:
    from anime_renamer import utils
except ImportError:  # standalone "copy & run" mode
    import utils


def preparefiles(root=None):
    """Flatten *root* (default: current directory) into a single level."""
    root = os.path.abspath(root or os.getcwd())
    print("Preparing folder: {}".format(root))

    moved = 0
    skipped = 0

    for current, dirs, files in os.walk(root, topdown=False):
        # Skip the root itself - files already at the top level stay put.
        if os.path.abspath(current) == root:
            continue

        for name in files:
            src = os.path.join(current, name)
            if not utils.is_media(name):
                continue

            # Compose a collision-free destination in the root folder.
            dst = utils.unique_path(os.path.join(root, name))
            try:
                shutil.move(src, dst)
            except (OSError, shutil.Error) as exc:
                print("  ! failed to move {} ({}). Skipped.".format(src, exc))
                skipped += 1
                continue
            utils.log_rename(src, dst)
            moved += 1
            print("  moved: {}  ->  {}".format(os.path.relpath(src, root),
                                               os.path.basename(dst)))

        # Remove the sub-folder when it is now empty (files only, not recursively).
        try:
            if not os.listdir(current):
                os.rmdir(current)
        except OSError:
            pass

    print("Done. {} file(s) moved, {} skipped.".format(moved, skipped))
    return moved, skipped


if __name__ == "__main__":
    preparefiles()
