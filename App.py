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
from gi.repository import Gdk
from gi.repository import GLib
import gobject
gobject.threads_init()

from lib.ui import GoogleMusic_main
from lib.ui import GoogleMusic_dialog_login
from lib.KeyRing import keyring
from lib.core.gstreamer import GStreamer
from gmusicapi.api import Api as gMusicApi
import threading
import gst
import time
class Gusic(object):
	def __init__(self):
		self.mainBuilder = GoogleMusic_main.Build(self,None)
		self.main = self.mainBuilder.get_object('window1')
		self.keyring = keyring()
		self.api = gMusicApi()
		self.song = {
			"duration": [],
			"GtkSource": []
		}
		self.Library = {}
		self.gst = GStreamer()
		self.gst.set_playback()
		self.obj_song_progress = self.mainBuilder.get_object('song_progress')
		self.label_song_time = self.mainBuilder.get_object('label_song_time')
		self.toolbutton_play = self.mainBuilder.get_object('toolbutton_play')


		if self.keyring.haveLoginDetails():
			self.startGusic()
		else:
			self.loginBuilder = GoogleMusic_dialog_login.Build(self,None)
			self.loginDialog = self.loginBuilder.get_object('window_login')
			self.image_logo = self.loginBuilder.get_object('image_logo')
			self.image_logo.set_from_file('imgs/Gusic_logo.svg')
			self.loginDialog.show_all()

	def startGusic(self,fromLogin=False):
		self.main.show_all()
		if fromLogin:
			self.loginDialog.hide()
	def isLoggedIn(self):
		while self.loggedIn == False:
			time.sleep(0.5)
		return True
	def fetchMusicLibrary(self):
		self.Library['songs'] = self.api.get_all_songs()
		self.liststore_all_songs = self.mainBuilder.get_object('liststore_all_songs')
		self.treeview_main_song_view = self.mainBuilder.get_object('treeview_main_song_view')
		#self.treeview_main_song_view.freeze_child_notify()
		#self.treeview_main_song_view.set_model(self.liststore_all_songs)
		songAdd = 0
		for song in self.Library['songs']:
			if not 'albumArtUrl' in song:
				song['albumArtUrl'] = 'null'
			if not 'disc' in song:
				song['disc'] = 0
			if not 'track' in song:
				song['track'] = 0
			if not 'totalTracks' in song:
				song['totalTracks'] = 0
			#print "adding %s" % song['title']
			#print song
			self.liststore_all_songs.append([song['type'],song['title'],str(song['lastPlayed']),song['album'],song['artist'],song['id'],song['disc'],song['track'],song['totalTracks'],song['genre'],song['url'],song['albumArtUrl'],song['durationMillis']])
		#print "setting model"
		self.treeview_main_song_view.set_model(self.liststore_all_songs)
		#self.treeview_main_song_view.thaw_child_notify()
	def set_song_title(self,title):
		label = self.mainBuilder.get_object("label_song_title")
		label.set_text(title)
	def set_song_artist(self,artist):
		label = self.mainBuilder.get_object("label_song_details")
		label.set_text(artist)
	def start_checkProgress(self,model,tree_iter):
		duration = model.get_value(tree_iter,12) / 1000
		pretty_duration = str(duration / 60) + ":" + "%.2d" % (duration % 60)
		self.obj_song_progress.set_range(0,duration)
		self.song["duration"] = [duration,pretty_duration]
		self.song['GtkSource'] = [model,tree_iter]
		gobject.timeout_add(250,self._checkProgress)
	def _checkProgress(self):
		if self.gst.nowplaying is not None and self.gst.status is self.gst.PLAYING:
			if self.toolbutton_play.get_property("stock-id") != "gtk-media-pause":
				self.toolbutton_play.set_property("stock-id","gtk-media-pause")
			position = self.gst.getposition() / gst.SECOND
			self.obj_song_progress.set_value(position)
			pretty_position = str(position / 60) + ":" + "%.2d" % (position % 60)
			self.label_song_time.set_text(pretty_position)
			return True
		elif self.gst.nowplaying is not None and self.gst.status is self.gst.PAUSED:
			if self.toolbutton_play.get_property("stock-id") != "gtk-media-play":
				self.toolbutton_play.set_property("stock-id","gtk-media-play")
		else:
			self.toolbutton_play.set_property("stock-id","gtk-media-play")
			self.label_song_time.set_text("00:00")
			return False

	def Error(self,title,body):
		dialog = Gtk.MessageDialog(parent=self.main,flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.ERROR,buttons=Gtk.ButtonsType.CANCEL,message_format=title)
		dialog.format_secondary_text(body)
		dialog.run()
		dialog.destroy()


class main():
	def __init__(self):
		GLib.threads_init()
		Gdk.threads_enter()
		app = Gusic()
		Gtk.main()
		Gdk.threads_leave()


main()