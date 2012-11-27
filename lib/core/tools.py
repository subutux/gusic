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
from gi.repository import GdkPixbuf, Gdk
import urllib2
def setImageFromUrl(GtkImage,url,scale=None):
	pixbufl = GdkPixbuf.PixbufLoader()
	ulib = urllib2.urlopen(url)
	pixbufl.write(ulib.read())
	pixbufl.close()
	pixbuf = pixbufl.get_pixbuf()
	if scale is not None:
		print "scaling",scale[0],scale[1]
		pixbuf = pixbuf.scale_simple(scale[0],scale[1],GdkPixbuf.InterpType.BILINEAR)
	GtkImage.set_from_pixbuf(GdkPixbuf.Pixbuf.copy(pixbuf))
def setImageFromCache(GtkImage,url,cache,scale=None):
	image = cache.checkImageCache([url],auto_cache=True,quiet=False)[0]
	if scale is None:
		pb = GdkPixbuf.Pixbuf.new_from_file(image)
	else:
		pb = GdkPixbuf.Pixbuf.new_from_file_at_size(image,scale[0],scale[1])
	GtkImage.set_from_pixbuf(pb)
	return True
def iter_prev(iter, model):
	'''
	source: http://faq.pygtk.org/index.py?req=show&file=faq13.051.htp
	'''
	path = model.get_path(iter)
	position = path[-1]
	if position == 0:
		return None
	prev_path = list(path)[:-1]
	prev_path.append(position - 1)
	prev = model.get_iter(tuple(prev_path))
	return prev

