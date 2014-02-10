#!/usr/bin/env python

import re
from setuptools import setup

requires = ['jinja2==2.7.1']

version = re.search('__version__ = "(.+?)"',
                    open('src/main.py').read()).group(1)

setup(
    name='movieinfo',
    author='Kim Bratzel',
    author_email='kim.bratzel@gmail.com',
    url='https://bitbucket.org/kimbratzel/movie-info',
    version=version,
    packages=['src'],
    description='Movie Info Getter',
    long_description="Movie Collection Information Gatherer",
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Video',
    ],
    install_requires=requires,
    entry_points = {
        'console_scripts':[
            'movieinfo = src.main:main'
        ]
    },
)