"""Standalone entry point for the "copy & run" workflow.

Copy every ``.py`` file from the ``anime_renamer`` folder into the base
folder of your anime and run::

    python main.py

It works whether or not the package is installed: it prefers the sibling
modules sitting next to it and falls back to the installed package.
"""

import sys


def main():
    try:
        from pipeline import run_interactive
    except ImportError:
        from anime_renamer.pipeline import run_interactive

    try:
        run_interactive()
    except KeyboardInterrupt:
        print("\nAborted by user.")


if __name__ == "__main__":
    main()
