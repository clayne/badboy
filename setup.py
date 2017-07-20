#!/usr/bin/env python3

# doc page:
# https://docs.python.org/3.5/distutils/setupscript.html
from setuptools import setup

setup(
	name = 'badboy',
	version = '0.1',
	description = 'Place holder',
	author = 'Adam Nunez',
	author_email = 'adam.a.nunez@gmail.com',
	license = 'GPLv3',
	url = 'https://github.com/aanunez/badboy',
	packages = ['badboy'],
	include_package_data = True,
    install_requires=[
        'praw'
    ],
    entry_points={
        'console_scripts': [
            'badboy = badboy.__main__:main'
        ]
    },
    classifiers=[
        # List here: https://pypi.python.org/pypi?%3Aaction=browse
        'Development Status :: 2 - Pre-Alpha',
        #'Intended Audience :: Developers',
        #'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='reddit'
)
