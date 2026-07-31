"""Package entry point: ``python -m anime_renamer`` or the ``anime_renamer``
console script installed by setup.py.
"""

from anime_renamer.pipeline import run_interactive


def main():
    try:
        run_interactive()
    except KeyboardInterrupt:
        print("\nAborted by user.")


if __name__ == "__main__":
    main()
