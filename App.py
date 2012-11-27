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
from lib.core.bus import Bus
from lib.core.cache import Cache
from lib.core import tools
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
		self.Bus = Bus()
		self.Bus.registerEvent("on-start-playing")
		self.Bus.registerEvent("on-pause")
		self.Bus.registerEvent("on-login")
		self.Bus.registerEvent("on-update-library")
		self.Bus.registerEvent("on-song-ended")
		self.Bus.connect("on-song-ended",self._playNext)
		self.Cache = Cache()
		self.treeview_media_view = self.mainBuilder.get_object('treeview_media_view')
		self.treeview_media_view.set_cursor(0)
		self.liststore_media = self.mainBuilder.get_object('liststore_media')
		self.treestore_media = self.mainBuilder.get_object('treestore_media')
		#TODO: set Style properties
		#self.mainBuilder.get_object("paned1").set_property('handle-size',1)


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
		songAdd = 0
		albumArtUrls = []
		for song in self.Library['songs']:
			if not 'albumArtUrl' in song:
				song['albumArtUrl'] = 'null'
			else:
				albumArtUrls.append('http:' + song['albumArtUrl'])
			if not 'disc' in song:
				song['disc'] = 0
			if not 'track' in song:
				song['track'] = 0
			if not 'totalTracks' in song:
				song['totalTracks'] = 0
			self.liststore_all_songs.append([song['type'],song['title'],str(song['lastPlayed']),song['album'],song['artist'],song['id'],song['disc'],song['track'],song['totalTracks'],song['genre'],song['url'],song['albumArtUrl'],song['durationMillis']])
		self.treeview_main_song_view.set_model(self.liststore_all_songs)
	def fetchPlaylistLibrary(self):
		self.Library['playlists'] = self.api.get_all_playlist_ids(auto=True,user=True)
		
		print self.Library['playlists']
		parent_media = self.treestore_media.append(None,['sys-all','All Media','sys'])
		parent_playlists = self.treestore_media.append(parent_media,['sys-pl','Playlists','sys'])
		parent_auto_pl = self.treestore_media.append(parent_playlists,['sys-pl-auto','Auto playlists','sys'])
		parent_user_pl = self.treestore_media.append(parent_playlists,['sys-pl-user','Your playlists','sys'])
		for pl in self.Library['playlists']['auto'].keys():
			if type(self.Library['playlists']['auto'][pl]) is list:
				for pl_ in self.Library['playlists']['auto'][pl]:
					self.treestore_media.append(parent_auto_pl,[pl_,pl,'gen'])
			else:
				self.treestore_media.append(parent_auto_pl,[self.Library['playlists']['auto'][pl],pl,'gen'])
		for pl in self.Library['playlists']['user'].keys():
			self.treestore_media.append(parent_user_pl,[self.Library['playlists']['user'][pl],pl,'gen'])
		self.treeview_media_view.set_model(self.treestore_media)
		return True
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
				self.Bus.emit('on-start-playing')
				self.toolbutton_play.set_property("stock-id","gtk-media-pause")
			position = self.gst.getposition() / gst.SECOND
			self.obj_song_progress.set_value(position)
			pretty_position = str(position / 60) + ":" + "%.2d" % (position % 60)
			self.label_song_time.set_text(pretty_position)
			return True
		elif self.gst.nowplaying is not None and self.gst.status is self.gst.PAUSED:
			if self.toolbutton_play.get_property("stock-id") != "gtk-media-play":
				self.Bus.emit('on-pause')
				self.toolbutton_play.set_property("stock-id","gtk-media-play")
		elif self.gst.status is self.gst.NULL:
			self.toolbutton_play.set_property("stock-id","gtk-media-play")
			self.Bus.emit("on-song-ended")
			self.obj_song_progress.set_value(0)
			self.label_song_time.set_text("00:00")
			return False
	def _playIter(self,model,tree_iter):
			songId = model.get_value(tree_iter,5)
			songTitle = model.get_value(tree_iter,1)
			songArtist = model.get_value(tree_iter,4)
			try:
			 	songUrl = self.api.get_stream_url(songId)
			except urllib2.HTTPError:
				self.Error(title="Error retrieving stream",body="Gusic was unable to retrieve the streaming url. This likely means that you've exceeded your streaming limit. (Ouch!)")
				return False
			self.set_song_title(songTitle)
			self.set_song_artist(songArtist)
			self.treeview_main_song_view.set_cursor(model.get_path(tree_iter))
			play = threading.Thread(target=self.gst.playpause,args=(songUrl,None))
			play.start()
			self.obj_song_progress.set_sensitive(True)
			imgUrl = 'http:' + model.get_value(tree_iter,11)
			if imgUrl is not 'http:null':
				# Setting size of album art to 400
				imgUrl = imgUrl.replace('s130','s400')
				threading.Thread(target=tools.setImageFromCache,args=(self.mainBuilder.get_object("image_toolbar_art"),imgUrl,self.Cache,[50,50])).start()
				threading.Thread(target=tools.setImageFromCache,args=(self.mainBuilder.get_object("image_art"),imgUrl,self.Cache,[200,200])).start()
			else:
				self.mainBuilder.get_object("image_toolbar_art").set_from_file("../../imgs/Gusic_logo-32.png")
				self.mainBuilder.get_object("image_art").set_from_file("../../imgs/Gusic_logo-128.png")
			self.start_checkProgress(model,tree_iter)
	def _playPrev(self):
		if self.gst.nowplaying is not None and self.gst.status is not self.gst.NULL:
			if self.gst.status is self.gst.PAUSED or self.gst.status is self.gst.PLAYING:
				if int(self.obj_song_progress.get_value()) < 3:
					tree_selection = self.treeview_main_song_view.get_selection()
					(model, pathlist) = tree_selection.get_selected_rows()
					tree_iter = model.get_iter(pathlist[0])
					prev_iter = tools.iter_prev(tree_iter,model)
					self._playIter(model,prev_iter)
				else:
					self.gst.seek(0)

	def _playNext(self):
		self.gst.playpause(None)
		tree_selection = self.treeview_main_song_view.get_selection()
		(model, pathlist) = tree_selection.get_selected_rows()
		tree_iter = model.get_iter(pathlist[0])
		next_iter = model.iter_next(tree_iter)
		self._playIter(model,next_iter)
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