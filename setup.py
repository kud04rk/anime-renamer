from setuptools import setup, find_packages

setup(
    name="anime_renamer",
    version="0.6",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "anime_renamer = anime_renamer.__main__:main",
        ]
    },
    url="https://github.com/kud04rk/anime-renamer",
    license="MIT",
    author="kudoark",
    author_email="",
    description="A simple cross-platform command line renamer for anime "
                "files, powered by TheTVDB.",
    install_requires=["requests", "tvdbsimple"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
)
