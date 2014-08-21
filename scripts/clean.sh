#!/bin/sh

find . -name '*.pyc' -delete
find . -name '.DS_Store' -delete

sudo rm -rf dist
sudo rm -rf build
sudo rm -rf movieinfo.egg-info