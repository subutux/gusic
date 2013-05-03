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
from gi.repository import Gtk
from lib.core.signals import Signals
from lib.core import tools
import threading
import logging
import urllib2

class Signals(Signals):
	def on_toolbutton_pause_toggled(self,widget):
		if self.mSelf.log_scroll == True:
			self.mSelf.log_scroll = False
		else:
			self.mSelf.log_scroll = True

		return True
	def on_toolbutton_clear_clicked(self,widget):
		self.mSelf.logBuilder.get_object('liststore_log').clear()
		return True
	def on_treeview_log_size_allocate(self,widget,event,data=None):
		if self.mSelf.log_scroll == True:
			adj = widget.get_vadjustment()
			adj.set_value(adj.get_upper() - adj.get_page_size())
		return True