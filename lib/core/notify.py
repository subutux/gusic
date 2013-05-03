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
import logging
log = logging.getLogger('gusic')

from cache import Cache
from gi.repository import Notify ,Gtk, GdkPixbuf
class Notifier(object):
	def __init__(self):
		self.cache = Cache
		Notify.init('gusic')
		self.defaultIcon = self.createPixbuf('imgs/Gusic_logo-64.png')
		self.notification = None
	def _new_notif(self,title,text,icon=None):
		if self.notification:
			self.notification.update(title,text,Gtk.STOCK_DIALOG_INFO)
		else:
			self.notification = Notify.Notification.new(title,text,Gtk.STOCK_DIALOG_INFO)
		if icon:
			self.notification.set_icon_from_pixbuf(self.createPixbuf(icon))
		else:
			self.notification.set_icon_from_pixbuf(self.defaultIcon)
		
		self.notification.set_urgency(Notify.Urgency.LOW)
		self.notification.set_timeout(5)
		self.notification.show()

	def createPixbuf(self,file):
		return GdkPixbuf.Pixbuf.new_from_file(file)
	def NotifyfFromIter(self,iter):
		title = iter.get_value(1) + iter.get_value(4)
		text = iter.get_value(3)
		icon = self.cache.getImageFromCache(iter.get_value(11))
		self._new_notif(title,text,icon)
