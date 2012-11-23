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
from lib.core import tools
import threading
import urllib2

class Signals(Signals):
	def on_toolbutton_play_clicked(self,widget):
		if self.mSelf.gst.nowplaying == None:
			self.on_treeview_main_song_view_row_activated(None,None,None)

		else:
			self.mSelf.gst.playpause(None)
			self.mSelf.obj_song_progress.set_sensitive(True)
			model,tree_iter = self.mSelf.song['GtkSource']
			self.mSelf.start_checkProgress(model,tree_iter)
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
			try:
			 	songUrl = self.mSelf.api.get_stream_url(songId)
			except urllib2.HTTPError:
				self.mSelf.Error(title="Error retrieving stream",body="Gusic was unable to retrieve the streaming url. This likely means that you've exceeded your streaming limit. (Ouch!)")
				return False
			self.mSelf.set_song_title(songTitle)
			self.mSelf.set_song_artist(songArtist)
			play = threading.Thread(target=self.mSelf.gst.playpause,args=(songUrl,None))
			play.start()
			self.mSelf.obj_song_progress.set_sensitive(True)
			setImg = threading.Thread(target=tools.setImageFromUrl,args=(self.mSelf.mainBuilder.get_object("image_toolbar_art"),'http:' + model.get_value(tree_iter,11),[50,50]))
			setImg.start()
			setMImg = threading.Thread(target=tools.setImageFromUrl,args=(self.mSelf.mainBuilder.get_object("image_art"),'http:' + model.get_value(tree_iter,11),[200,200]))
			setMImg.start()
			self.mSelf.start_checkProgress(model,tree_iter)

