#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division, print_function, unicode_literals)

import copy
import math
import sys
import time
from collections import namedtuple

try:
	import Image
except ImportError:
	try:
		from PIL import Image
	except ImportError:
		sys.stderr.write("Please install PIL or Pillow\n")
		sys.exit(1)

def is_nude(path_or_io):
	nude = Nude(path_or_io)
	return nude.parse().result

class Nude(object):

	Skin = namedtuple("Skin", "skin id region x or y checked")

	def __init__(self, path_or_io):
		if isinstance(Image, type(path_or_io)):
			self.image = path_or_io
		else:
			self.image = Image.open(path_or_io)
		bands = self.image.getbands()
		# convert greyscale to rgb
		if len(bands) == 1:
			new_img = Image.new("RGB", self.image.size)
			new_img.paste(self.image)
			f = self.image.filename
			self.image = new_img
			self.image.filename = f
		self.skin_map = []
		self.skin_regions = []
		self.detected_regions = []
		self.merge_regions = []
		self.last_from, self.last_to = -1, -1
		self.result = None
		self.message = None
		self.width, self.height = self.image.size
		self.total_pixels = self.width * self.height

	def resize(self, maxwidth=1000, maxheight=1000):
		ret = 0
		if maxwidth:
			if self.width > maxwidth:
				wpercent = (maxwidth / float(self.width))
				hsize = int((float(self.height) * float(wpercent)))
				fname = self.image.filename
				self.image = self.image.resize((maxwidth, hsize), Image.ANTIALIAS)
				self.image.filename = fname
				self.width, self.height = self.image.size
				self.total_pixels = self.width * self.height
				ret += 1
		if maxheight:
			if self.height > maxheight:
				hpercent = (maxheight / float(self.height))
				wsize = int((float(self.width) * float(hpercent)))
				fname = self.image.filename
				self.image = self.image.resize((wsize, maxheight), Image.ANTIALIAS)
				self.image.filename = fname
				self.width, self.height = self.image.size
				self.total_pixels = self.width * self.height
				ret += 2
		return ret

def _testfile(fname, resize=False):
	start = time.time()
	n = Nude(fname)
	if resize:
		n.resize(maxheight=800, maxwidth=600)
	n.parse()
	totaltime = int(math.ceil(time.time() - start))
	size = str(n.height) + 'x' + str(n.width)
	return (fname, n.result, totaltime, size, n.message)

def _poolcallback(results):
	fname, result, totaltime, size, message = results
	print(fname, result, sep="\t")

def _poolcallbackverbose(results):
	fname, result, totaltime, size, message = results
	print(fname, result, totaltime, size, message, sep=', ')