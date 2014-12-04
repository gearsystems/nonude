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

	def parse(self):
		if self.result:
			return self

		pixels = self.image.load()
		for y in range(self.height):
			for x in range(self.width):
				r = pixels[x, y][0]   # red
				g = pixels[x, y][1]   # green
				b = pixels[x, y][2]   # blue
				_id = x + y * self.width + 1

				if not self._classify_skin(r, g, b):
					self.skin_map.append(self.Skin(_id, False, 0, x, y, False))
				else:
					self.skin_map.append(self.Skin(_id, True, 0, x, y, False))

					region = -1
					check_indexes = [_id - 2,
										_id - self.width - 2,
										_id - self.width - 1,
										_id - self.width]
					checker = False

					for index in check_indexes:
						try:
							self.skin_map[index]
						except IndexError:
							break
						if self.skin_map[index].skin:
							if (self.skin_map[index].region != region and
									region != -1 and
									self.last_from != region and
									self.last_to != self.skin_map[index].region):
							self._add_merge(region, self.skin_map[index].region)
							region = self.skin_map[index].region
							checker = True

					if not checker:
						_skin = self.skin_map[_id - 1]._replace(region=len(self.detected_regions))
						self.skin_map[_id - 1] = _skin
						self.detected_regions.append([self.skin_map[_id - 1]])
						continue
					else:
						if region > -1:
							try:
								self.detected_regions[region]
							except IndexError:
								self.detected_regions.append([])
							_skin = self.skin_map[_id - 1]._replace(region=region)
							self.skin_map[_id - 1] = _skin
							self.detected_regions[region].append(self.skin_map[_id - 1])

		self._merge(self.detected_regions, self.merge_regions)
		self._analyse_regions()
		return self

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