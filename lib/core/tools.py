# This file is part of gusic.

# gusic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gusic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gusic.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2013, Stijn Van Campenhout <stijn.vancampenhout@gmail.com>
from gi.repository import GdkPixbuf, Gdk
import urllib2
import logging
log = logging.getLogger('gusic')
def setImageFromUrl(GtkImage,url,scale=None):
	pixbufl = GdkPixbuf.PixbufLoader()
	ulib = urllib2.urlopen(url)
	pixbufl.write(ulib.read())
	pixbufl.close()
	pixbuf = pixbufl.get_pixbuf()
	if scale is not None:
		log.debug("scaling w %s h %s",str(scale[0]),str(scale[1]))
		pixbuf = pixbuf.scale_simple(scale[0],scale[1],GdkPixbuf.InterpType.BILINEAR)
	GtkImage.set_from_pixbuf(GdkPixbuf.Pixbuf.copy(pixbuf))
def setImageFromCache(GtkImage,url,cache,scale=None):
	image = cache.checkImageCache([url],auto_cache=True,quiet=False)[0]
	if scale is None:
		try:
			pb = GdkPixbuf.Pixbuf.new_from_file(image)
		except:
			pass
	else:
		try:
			pb = GdkPixbuf.Pixbuf.new_from_file_at_size(image,scale[0],scale[1])
		except:
			pass
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

def model_get_iter_last( model, parent=None ):
  """
  source : http://stackoverflow.com/a/2915781
  Returns a gtk.TreeIter to the last row or None if there aren't any rows.
  If parent is None, returns a gtk.TreeIter to the last root row."""
  n = model.iter_n_children( parent )
  return n and model.iter_nth_child( parent, n - 1 )