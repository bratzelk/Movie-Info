#!/usr/bin/env python

import re
from setuptools import setup

requires = ['jinja2==2.7.1']

version = re.search('__version__ = "(.+?)"',
                    open('movieinfo/src/main.py').read()).group(1)

files = ["src/templates/*", ]


setup(
    name='movieinfo',
    author='Kim Bratzel',
    author_email='kim.bratzel@gmail.com',
    url='https://github.com/bratzelk/movie-info',
    version=version,

    packages = ['movieinfo'],
    package_data = {'' : files },
    include_package_data=True,

    scripts = ["runner"],

    description='Movie Info Getter',
    long_description="Movie Collection Meta-Data Gatherer",
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Video',
    ],

    install_requires=requires,
    entry_points = {
        'console_scripts':[
            'movieinfo = movieinfo.src.main:start'
        ]
    },
)