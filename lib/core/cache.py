# This file is part of google-music.

# google-music is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# google-music is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with google-music.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2013, Stijn Van Campenhout <stijn.vancampenhout@gmail.com>
import os
import urllib2
class Cache(object):
	def __init__(self):
		self.cacheLocation = os.environ['HOME'] + '/.local/share/gusic/cache'
		self.cacheImages = self.cacheLocation + '/images'
		if not os.path.isdir(self.cacheLocation):
			os.makedirs(self.cacheLocation)
		if not os.path.isdir(self.cacheImages):
			os.makedirs(self.cacheImages)
	def checkImageCache(self,cacheURLs,auto_cache=True,quiet=True):
		cache = []
		for url in cacheURLs:
			fname = url.rsplit('/',1)[1]
			if not os.path.stat(self.cacheImage + '/' + fname):
				if auto_cache:
					ul = urllib2.urlopen(url)
					open(self.cacheImage + '/' + fname,'w').write(ul.read())
			if not quiet:
				cache.append(self.chacheImage + '/' + fname)
			else:
				return True
	def getImageFromCache(self,url):
		fname = url.rsplit('/',1)[1]
		if os.path.stat(self.cacheImage + '/' + fname):
			return self.cacheImage + '/' + fname
		else:
			return False
	def imageIsCached(self,url):
		fname = url.rsplit('/',1)[1]
		if os.path.stat(self.cacheImage + '/' + fname):
			return True
		else:
			return False
