nonude
=======
[![PyPI version](https://badge.fury.io/py/nonude.svg)](http://badge.fury.io/py/nonude)
[![Code Health](https://landscape.io/github/gearsystems/nonude/master/landscape.svg?style=flat)](https://landscape.io/github/gearsystems/nonude/master)
Quick Installations
-------------------
We are now a pip entry, you could just do `pip install nonude` to get the entry.

About
-----
A nudity detection plugin on the system level that is used to check if the photographs uploaded have nudity or not.

Requirements
------------
* Python2.7+ and Python3.3+
* PIL or Pillow

Development setup instructions
==============================
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install Pillow`
* `python setup.py install`

`make clean` in case you want to remove it.

Usage
=====
`$ nonude IMAGEPATH/NAME`

Known issues
============
There are known issues where the installation of Pillow might fail, one of it being `jpeg -- no option found`, to fix these please install
`sudo apt-get install libjpeg-dev` on debian based systems.
