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
from gi.repository import Gtk
from lib.core.signals import Signals
class Signals(Signals):
	def on_toolbutton_play_clicked(self,widget):
		print "on_toolbutton_play_clicked"
	def on_button_exit_clicked(self,widget):
		self.destroy(None)
	def on_treeview_main_song_view_row_activated(self,one,two,three) :
		tree_selection = self.mSelf.treeview_main_song_view.get_selection()
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			songId = model.get_value(tree_iter,5)
			songUrl = self.mSelf.api.get_stream_url(songId)
			print "url: %s" %songUrl
			self.mSelf.gst.playpause(songUrl)
