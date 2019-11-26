from setuptools import setup

setup(
    name='anime_renamer',
    version='0.3',
    packages=['anime_renamer'],
    entry_points={
        'console_scripts': [
            'anime_renamer = anime_renamer.__main__:main'
        ]
    },
    url='https://github.com/smsriharsha/anime-renamer',
    license='MIT',
    author='kudoark',
    author_email='',
    description='', install_requires=['requests', 'tvdbsimple'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities"
    ],

)
