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
	def on_menuitem_toggle_mini_activate(self,widget):
		paned = self.mSelf.mainBuilder.get_object("paned1")
		if paned.get_property('visible'):
			paned.set_property('visible',False)
		else:
			paned.set_property('visible',True)
		return True
	def on_toolbutton_next_clicked(self,widget):
		self.mSelf._playNext()
		return True
	def on_toolbutton_prev_clicked(self,widget):
		self.mSelf._playPrev()
		return True
	def on_treeview_main_song_view_row_activated(self,one,two,three) :
		tree_selection = self.mSelf.treeview_main_song_view.get_selection()
		(model, pathlist) = tree_selection.get_selected_rows()
		self.mSelf._playIter(model,model.get_iter(pathlist[0]))
	def on_treeview_media_view_cursor_changed(self,treeview,user_param=False):
		tree_selection = treeview.get_selection()
		(model,pathlist) = tree_selection.get_selected_rows()
		tree_iter = model.get_iter(pathlist[0])
		rowType = model.get_value(tree_iter,2)
		if rowType == 'sys-all':
			self.mSelf.treeview_main_song_view.set_model(self.mSelf.liststore_all_songs)
		elif rowType == "sys-pl-auto-gen" or rowType == "sys-pl-user-gen":
			ShowPl = threading.Thread(target=self.mSelf.viewPlaylist,args=(model.get_value(tree_iter,0),model.get_value(tree_iter,1)))
			ShowPl.start()
			while ShowPl.isAlive():
				while Gtk.events_pending():
					Gtk.main_iteration()

		#TODO: check what is selected
		#TODO: - check the type of the row
		#TODO:  - if row is type of sys-all: set treeview_main_song_view to model liststore_all_songs
		#TODO:  - if row is type of sys-pl-(user,auto)-gen: check if there is a liststore
		#TODO:   - if none found: create one (using id in name like liststore_id_songs) and fetch playlist contents
		#TODO:   - set the model to the playlist liststore
		#TODO:  - if row is other type: ignore selection

	def on_song_progress_change_value(self,widget,scroll,value,user_param=False):
		self.mSelf.gst.seek(int(value))
		return True

