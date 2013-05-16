#!/usr/bin/env python
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
from gi.repository import Gdk
from gi.repository import GLib
import os
import shutil
# change to current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
## CONFIG loader ##
from lib.core.config import Config
config =  Config({
		'login': {
			'save_login': False,
			'save_login_username': True,
			'save_login_username_content': ''
		},
		'notifications': {
			'use_notifications': True,
			'on_background_only': False,
			'timeout': 5,
			'timeout_max': 60,
			'timeout_min': 1
		},
		'tasks': {
			'library_updater' : False,
			'library_updater_interval': 30,
			'library_updater_interval_max': 60,
			'library_updater_interval_min': 10
		},
		'locations': {
			'basedir': '~/.local/share/gusic',
			'logfile': 'gusic.log',
			'cachefile': 'gusic.cache.sql',
			'cachedir': 'cache'
		},
	})
if "~" in config['locations']['basedir']:
	config['locations']['basedir'] = os.path.expanduser(config['locations']['basedir'])
config['tmp'] = {'username' : '', 'resync_library_on_startup': False}
## CONFIG loader ##
import gobject
gobject.threads_init()
from lib._version import __version__
from lib.ui import GoogleMusic_main
from lib.ui import GoogleMusic_dialog_login
from lib.ui import GoogleMusic_about
from lib.ui import GoogleMusic_log
from lib.ui import GoogleMusic_settings
from lib.KeyRing import keyring
from lib.core.gstreamer import GStreamer
from lib.core.bus import Bus
from lib.core.cache import Cache
from lib.core.loggingHandlers import ListStoreLoggingHandler
from lib.core.notify import Notifier
from lib.core import tools
from lib.core.SearchCompletion import SearchCompletion
from lib.core.playlists import Playlists, Playlist
from gmusicapi import Webclient as gMusicApi
import threading
import logging
import gst
import time
import urllib2
from random import randrange
from gmusicapi.utils import utils
logfile = config['locations']['basedir'] + '/' + config['locations']['logfile']
logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s [%(levelname)s]:{%(filename)s[%(lineno)d]%(funcName)s}:%(message)s')
log = logging.getLogger('gusic')
class Gusic(object):
	def __init__(self):
		self.logBuilder = GoogleMusic_log.Build(self,None)
		self.logBuilder.get_object('window_log').connect('delete-event', lambda w, e: w.hide() or True)
		self.log_scroll = True
		logging._handlers.ListStoreLoggingHandler = ListStoreLoggingHandler
		log.addHandler(logging._handlers.ListStoreLoggingHandler(self.logBuilder.get_object('liststore_log')))
		utils.log = log
		log.debug("loading main window builder")
		self.mainBuilder = GoogleMusic_main.Build(self,None)
		self.main = self.mainBuilder.get_object('window1')
		self.main.set_wmclass ("Gusic", "Gusic")
		self.main.set_title('Gusic')
		self.aboutBuilder = GoogleMusic_about.Build(self,None)
		self.aboutBuilder.get_object('aboutdialog1').set_version(__version__)
		self.keyring = keyring()
		self.api = gMusicApi()
		self.song = {
			"duration": [],
			"GtkSource": []
		}
		self.playmode = []
		self.Library = {}
		log.debug('loading GStreamer')
		self.gst = GStreamer()
		self.gst.set_playback()
		self.obj_song_progress = self.mainBuilder.get_object('song_progress')
		self.label_song_time = self.mainBuilder.get_object('label_song_time')
		self.toolbutton_play = self.mainBuilder.get_object('toolbutton_play')
		self.image_playpause = self.mainBuilder.get_object('image_playpause')

		self.notifier = Notifier()
		self.Playlists = Playlists()
		log.debug('Registering Bus events')
		self.Bus = Bus()
		self.Bus.registerEvent("on-start-playing")
		self.Bus.registerEvent("on-pause")
		self.Bus.registerEvent("on-login")
		self.Bus.registerEvent("on-update-library")
		self.Bus.registerEvent("on-song-ended")
		log.debug('connecting self._playNext to bus event "on-song-ended"')
		self.Bus.connect("on-song-ended",self._playNext)
		self.treeview_media_view = self.mainBuilder.get_object('treeview_media_view')
		self.treeview_media_view.set_cursor(0)
		self.liststore_media = self.mainBuilder.get_object('liststore_media')
		self.treestore_media = self.mainBuilder.get_object('treestore_media')

		self.settingsBuilder = GoogleMusic_settings.Build(self,None)
		self.settingsBuilder.get_object('window1').connect('delete-event', lambda w, e: w.hide() or True)
		
		## THEMING ##
		#self.mainBuilder.get_object('treeview_main_song_view').set_name('treeview_main_song_view')
		#self.mainBuilder.get_object('viewport1').set_name('display')
		#self.main.set_name('window_main')
		self.mainBuilder.get_object('treeview_media_view').set_name('treeview_media_view')
		self.GtkScreen = Gdk.Screen.get_default()
		self.style_context = Gtk.StyleContext()
		self.css_provider = Gtk.CssProvider()
		self.css_provider.load_from_path('lib/core/styles.css')
		self.style_context.add_provider_for_screen(self.GtkScreen,self.css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		## THEMING ##

		if self.keyring.haveLoginDetails():
			log.info("Got login details in keyring. Loading Gusic")
			self.startGusic()
		else:

			log.info("Haven't got any login details. Asking nicely for some")
			self.loginBuilder = GoogleMusic_dialog_login.Build(self,None)
			self.loginDialog = self.loginBuilder.get_object('window_login')
			self.loginDialog.set_wmclass ("Gusic", "Gusic")
			self.loginDialog.set_title('Gusic')
			if config['login']['save_login_username']:
				username_input = self.loginBuilder.get_object('entry_google_account_user')
				username_input.set_text(config['login']['save_login_username_content'])

			self.image_logo = self.loginBuilder.get_object('image_logo')
			self.image_logo.set_from_file('imgs/Gusic_logo-256.png')
			self.loginDialog.show_all()

	def startGusic(self,fromLogin=False):
		# Cache depends on the username, so setting the cache class later
		self.Cache = Cache()
		self.main.show_all()
		if fromLogin:
			self.loginDialog.hide()
	def isLoggedIn(self):
		while self.loggedIn == False:
			time.sleep(0.2)
		return True
	def fetchMusicLibrary(self,status,other):
		log.info("loading fist api call: self.api.get_all_songs()")
		get_all_songs = self.api.get_all_songs(True)
		self.Library['songs'] = []
		for chunk in get_all_songs:
		 	for song in chunk:
		 		self.Library['songs'].append(song)
		 	status.set_text('Downloading music information ... (' + str(len(self.Library['songs'])) + ' songs)')
		
		self.liststore_all_songs = self.mainBuilder.get_object('liststore_all_songs')
		self.treeview_main_song_view = self.mainBuilder.get_object('treeview_main_song_view')
		log.info('removing model from treeview_main_song_view')
		self.treeview_main_song_view.set_model(None)
		songAdd = 0
		albumArtUrls = []
		log.info('storing song info into self.liststore_all_songs')
		status.set_text('Saving music information into database ... (1/2)')
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
		log.info('setting treeview_main_song_view model to self.liststore_all_songs')
		self.treeview_main_song_view.set_model(self.liststore_all_songs)
		self.mainBuilder.get_object('treeviewcolumn_title').set_sort_column_id(1)
		self.mainBuilder.get_object('treeviewcolumn_artist').set_sort_column_id(4)
		self.mainBuilder.get_object('treeviewcolumn_album').set_sort_column_id(3)
		self.treeview_main_song_view.set_cursor(0)
		status.set_text('Saving music information into database ... (2/2)')
		self.searchCompletion = SearchCompletion(self.liststore_all_songs)
		self.searchField = self.mainBuilder.get_object('entry_search_field')
		Completion = Gtk.EntryCompletion()
		Completion.set_model(self.searchCompletion.get_matchStore())
		#TODO: Multi column completion (songs, albums and artists) [DONE]
		
		cell = Gtk.CellRendererPixbuf()
		Completion.pack_end(cell,True)
		Completion.add_attribute(cell,'pixbuf',3)
		self.searchField.set_completion(Completion)
		Completion.set_text_column(1)
		Completion.connect('match-selected',self.completion_action_match_selected)
	def fetchPlaylistLibrary(self):
		log.info('fetching all playlists')
		self.Library['playlists'] = self.api.get_all_playlist_ids(auto=True,user=True)
		log.info('setting main tree items')
		parent_media = self.treestore_media.append(None,['sys-all','All Media','sys-all',900])
		parent_searches = self.treestore_media.append(parent_media,['self-gen-pl','Searches','self-gen-pl',700])
		self.search_playlists = parent_searches
		parent_playlists = self.treestore_media.append(parent_media,['sys-pl','Playlists','sys',700])
		parent_auto_pl = self.treestore_media.append(parent_playlists,['sys-pl-auto','Auto playlists','sys-pl-auto',500])
		parent_user_pl = self.treestore_media.append(parent_playlists,['sys-pl-user','Your playlists','sys-pl-user',500])
		log.info('setting dynamic fetched playlists')
		for pl in self.Library['playlists']['auto'].keys():
			if type(self.Library['playlists']['auto'][pl]) is list:
				for pl_ in self.Library['playlists']['auto'][pl]:
					log.debug('appending auto-playlist:%s id: %s',pl,pl_)
					self.treestore_media.append(parent_auto_pl,[pl,pl_,'gen'])
			else:
				log.debug('appending auto-playlist:%s id: %s',pl,self.Library['playlists']['auto'][pl])
				self.treestore_media.append(parent_auto_pl,[self.Library['playlists']['auto'][pl],pl,'sys-pl-auto-gen',400])
		for pl in self.Library['playlists']['user'].keys():
			if type(self.Library['playlists']['user'][pl]) is list:
				for pl_ in self.Library['playlists']['user'][pl]:
					log.debug('appending user-playlist:%s id: %s',pl,pl_)
					self.treestore_media.append(parent_user_pl,[pl_,pl,'gen',400])
			else:
				log.debug('appending auto-playlist:%s id: %s',pl,self.Library['playlists']['user'][pl])
				self.treestore_media.append(parent_user_pl,[self.Library['playlists']['user'][pl],pl,'sys-pl-user-gen',400])
		log.info('setting treeview_media_view model to self.treestore_media')
		self.treeview_media_view.set_model(self.treestore_media)
		self.treeview_media_view.expand_all()
		self.treeview_media_view.set_cursor(0)
		return True
	def viewPlaylist(self,Plid,name,Local=False):
		log.info('request for %s with id %s',name,Plid)
		if Local:
			log.info('Local Playlist')
			self.treeview_main_song_view.set_model(self.Playlists.getPlaylist(Plid).getModel())
		else:
			if self.Playlists.playlistExists(Plid):
				log.info('%s exists, setting treeview_main_song_view to playlist model',Plid)
				self.treeview_main_song_view.set_model(self.Playlists.getPlaylist(Plid).getModel())
			else:		
				log.info("%s doesn't exists. Fetching playlist and store in self.Playlists as a Playlist class",Plid)
				playlist = Playlist(self.api.get_playlist_songs(Plid),Plid,name)
				self.Playlists.addPlaylist(playlist)
				log.info('setting treeview_main_song_view model to playlist %s model',Plid)
				self.treeview_main_song_view.set_model(self.Playlists.getPlaylist(Plid).getModel())
		return True
	def completion_action_match_selected(self,completion,model,tree_iter):

		log.info('selected %s (%s,id=%s) from completion',model[tree_iter][1],model[tree_iter][0],model[tree_iter][2])

		if model[tree_iter][0] == 'song':
			self.select_playlist_from_id('sys-all')
			self.load_playlist_into_main_view('sys-all')
			songIter = self.get_song_from_id(model[tree_iter][2],playIt=True)
			#self.treeview_main_song_view.set_cursor(model[tree_iter][3])
		elif model[tree_iter][0] == 'album':
			#Creating a new playlist of al songs that has the album name
			song_list = []		
			item = self.liststore_all_songs.get_iter_first()
			while (item != None):
				if model[tree_iter][1] == self.liststore_all_songs.get_value(item,3):
					for song in self.Library['songs']:
						if song['id'] == self.liststore_all_songs.get_value(item,5):
							song_list.append(song)
				item = self.liststore_all_songs.iter_next(item)
			playlist = Playlist(song_list,"search-" + model[tree_iter][1],model[tree_iter][1])
			self.Playlists.addPlaylist(playlist)
			media_iter = self.treestore_media.append(self.search_playlists,["search-" + model[tree_iter][1],model[tree_iter][1],'search',400])
			self.treeview_media_view.expand_all()
			media_selection = self.treeview_media_view.get_selection()
			media_selection.select_iter(media_iter)
			self.load_playlist_into_main_view(self.treeview_media_view)

		elif model[tree_iter][0] == 'artist':
			#Creating a new playlist of al songs that has the album name
			song_list = []		
			item = self.liststore_all_songs.get_iter_first()
			while (item != None):
				if model[tree_iter][1] == self.liststore_all_songs.get_value(item,4):
					for song in self.Library['songs']:
						if song['id'] == self.liststore_all_songs.get_value(item,5):
							song_list.append(song)
				item = self.liststore_all_songs.iter_next(item)
			playlist = Playlist(song_list,"search-" + model[tree_iter][1],model[tree_iter][1])
			self.Playlists.addPlaylist(playlist)
			media_iter = self.treestore_media.append(self.search_playlists,["search-" + model[tree_iter][1],model[tree_iter][1],'search',400])
			self.treeview_media_view.expand_all()
			media_selection = self.treeview_media_view.get_selection()
			media_selection.select_iter(media_iter)
			self.load_playlist_into_main_view(self.treeview_media_view)
	def search_all(self,text):
			song_list = []
			id_list = []
			item = self.liststore_all_songs.get_iter_first()
			while (item != None):
				# Title
				if text.lower() in self.liststore_all_songs.get_value(item,1).lower():
					for song in self.Library['songs']:
						if song['id'] == self.liststore_all_songs.get_value(item,5) and song['id'] not in id_list:
							song_list.append(song)
							id_list.append(song['id'])

				# Album
				if text.lower() in self.liststore_all_songs.get_value(item,3).lower():
					for song in self.Library['songs']:
						if song['id'] == self.liststore_all_songs.get_value(item,5) and song['id'] not in id_list:
							song_list.append(song)
							id_list.append(song['id'])

				# Artist
				if text.lower() in self.liststore_all_songs.get_value(item,4).lower():
					for song in self.Library['songs']:
						if song['id'] == self.liststore_all_songs.get_value(item,5) and song['id'] not in id_list:
							song_list.append(song)
							id_list.append(song['id'])

				item = self.liststore_all_songs.iter_next(item)
			playlist = Playlist(song_list,"search-" + text,text)
			self.Playlists.addPlaylist(playlist)
			media_iter = self.treestore_media.append(self.search_playlists,["search-" + text,text,'search',400])
			self.treeview_media_view.expand_all()
			media_selection = self.treeview_media_view.get_selection()
			media_selection.select_iter(media_iter)
			self.load_playlist_into_main_view(self.treeview_media_view)
	def get_song_from_id(self,songId,playIt):
		item = self.liststore_all_songs.get_iter_first()
		while (item != None):		
			if self.liststore_all_songs.get_value(item,5) == songId:
				tree_selection = self.treeview_main_song_view.get_selection()
				tree_selection.select_iter(item)
				(model,pathlist) = tree_selection.get_selected_rows()
				self.treeview_main_song_view.scroll_to_cell(pathlist[0])
				if playIt:
					self._playIter(model,item)
				return item

			item = self.liststore_all_songs.iter_next(item)
	def select_playlist_from_id(self,playlistId):
		item = self.liststore_media.get_iter_first()
		while (item != None):
			if self.liststore_media.get_value(item,2) == playlistId:
				tree_selection = self.treeview_media_view.get_selection()
				tree_selection.select_iter(item)
				item = None
			item = self.liststore_media.iter_next(item)
	def load_playlist_into_main_view(self,treeview):
		log.info("Treeview type is %s",str(type(treeview)))
		if type(treeview) is None:
			return False
		elif type(treeview) is str:
			rowType = treeview
		else:
			tree_selection = treeview.get_selection()
			(model,pathlist) = tree_selection.get_selected_rows()
			if len(pathlist) == 0:
				log.info("Nothing selected")
				return False

			tree_iter = model.get_iter(pathlist[0])
			log.debug("treeview pathlist: %s", str(pathlist))
			rowType = model.get_value(tree_iter,2)
		log.debug("rowType: %s",rowType)
		if rowType == 'sys-all':
			self.treeview_main_song_view.set_model(self.liststore_all_songs)
		elif rowType == "sys-pl-auto-gen" or rowType == "sys-pl-user-gen" or rowType == "gen" or rowType == "search":
			ShowPl = threading.Thread(target=self.viewPlaylist,args=(model.get_value(tree_iter,0),model.get_value(tree_iter,1)))
			ShowPl.start()
			while ShowPl.isAlive():
			 	while Gtk.events_pending():
			 		Gtk.main_iteration()
	def toggle_playmode(self,mode):
		if mode in self.playmode:
			self.playmode.remove(mode)
			log.info('disabled playmode %s',mode)
		else:
			self.playmode.append(mode)
			log.info('enabled playmode %s',mode)

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
			if self.image_playpause.get_stock() != ("gtk-media-pause",6):
				self.Bus.emit('on-start-playing')
				self.image_playpause.set_from_stock("gtk-media-pause",6)
			position = self.gst.getposition() / gst.SECOND
			self.obj_song_progress.set_value(position)
			pretty_position = str(position / 60) + ":" + "%.2d" % (position % 60)
			self.label_song_time.set_text(pretty_position)
			return True
		elif self.gst.nowplaying is not None and self.gst.status is self.gst.PAUSED:
			if self.image_playpause.get_stock() != ("gtk-media-play",6):
				self.Bus.emit('on-pause')
				self.image_playpause.set_from_stock("gtk-media-play",6)
		elif self.gst.status is self.gst.NULL:
			self.image_playpause.set_from_stock("gtk-media-play",6)
			self.Bus.emit("on-song-ended")
			self.obj_song_progress.set_value(0)
			self.label_song_time.set_text("00:00")
			return False
	def _playIter(self,model,tree_iter):
			songId = model.get_value(tree_iter,5)
			songTitle = model.get_value(tree_iter,1)
			songArtist = model.get_value(tree_iter,4)
			songAlbum = model.get_value(tree_iter,3)
			log.info('playrequest for %s(%s)',songTitle,songId)
			try:
			 	songUrl = self.api.get_stream_url(songId)
			 	log.info('streaming url: <%s>',songUrl)
			except urllib2.HTTPError:
				log.exception("Exception while retreaving stream url")
				self.Error(title="Error retrieving stream",body="Gusic was unable to retrieve the streaming url. This likely means that you've exceeded your streaming limit. (Ouch!)")
				return False
			self.set_song_title(songTitle)
			self.set_song_artist(songArtist)
			self.treeview_main_song_view.set_cursor(model.get_path(tree_iter))
			log.info('starting play thread')
			play = threading.Thread(target=self.gst.playpause,args=(songUrl,None))
			play.start()
			self.obj_song_progress.set_sensitive(True)
			imgUrl = 'http:' + model.get_value(tree_iter,11)
			log.debug('album art url: <%s>',imgUrl)
			if imgUrl != 'http:null':
				# Setting size of album art to 400
				imgUrl = imgUrl.replace('s130','s400')
				threading.Thread(target=tools.setImageFromCache,args=(self.mainBuilder.get_object("image_toolbar_art"),imgUrl,self.Cache,[50,50])).start()
				threading.Thread(target=tools.setImageFromCache,args=(self.mainBuilder.get_object("image_art"),imgUrl,self.Cache,[200,200])).start()
			else:
				imgUrl = None
				self.mainBuilder.get_object("image_toolbar_art").set_from_file("imgs/Gusic_logo-32.png")
				self.mainBuilder.get_object("image_art").set_from_file("imgs/Gusic_logo-128.png")
			self.start_checkProgress(model,tree_iter)
			self.notifier._new_notif(songTitle + ' - ' + songArtist, songAlbum, self.Cache.getImageFromCache(imgUrl))
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
		if next_iter != None:
			if 'loop' in self.playmode:
				next_iter = model.get_iter_first()
			elif 'loop-one' in self.playmode:
				next_iter = tree_iter
			elif 'shuffle' in self.playmode:
				total_songs = model.iter_n_children( None )
				total_songs = total_songs - 1
				next_iter = model.iter_nth_child(None,randrange(0,total_songs))
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
