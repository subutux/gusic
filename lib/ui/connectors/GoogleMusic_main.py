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
import threading
class Signals(Signals):
	def on_toolbutton_play_clicked(self,widget):
		print "on_toolbutton_play_clicked"
		if self.mSelf.gst.nowplaying == None:
			self.on_treeview_main_song_view_row_activated(None,None,None)

		else:
			self.mSelf.gst.playpause(None)
	def on_button_exit_clicked(self,widget):
		self.destroy(None)
	def on_treeview_main_song_view_row_activated(self,one,two,three) :
		tree_selection = self.mSelf.treeview_main_song_view.get_selection()
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			songId = model.get_value(tree_iter,5)
			songTitle = model.get_value(tree_iter,1)
			songArtist = model.get_value(tree_iter,4)
			songUrl = self.mSelf.api.get_stream_url(songId)
			print "url: %s" %songUrl
			print "title: %s" %songTitle
			print "artist: %s" %songArtist
			self.mSelf.set_song_title(songTitle)
			self.mSelf.set_song_artist(songArtist)
			play = threading.Thread(target=self.mSelf.gst.playpause,args=(songUrl,None))
			play.start()
			self.mSelf.obj_song_progress.set_sensitive(True)
			self.mSelf.start_checkProgress(model,tree_iter)
