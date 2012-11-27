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
class Playlists(object):
	def __init__(self):
		self.playlist_collection = []
	def addPlaylist(self,p):
		if type(p) == Playlist:
			self.playlist_collection.append({p.id:p})
	def playlistExists(self,Plid):
		if Plid in self.playlist_collection:
			return True
	def getPlaylistModel(self,Plid):
		if self.playlistExists(Plid):
			return self.playlist_collection[Plid].getModel()



class Playlist(object):
	def __init__(self,songs,Plid,name):
		self.songs = songs
		self.id = Plid
		self.name = name
		self.store = Gtk.ListStore(int,str,str,str,str,str,int,int,int,str,str,str,int)
		for song in self.songs:
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
			self.store.append([song['type'],song['title'],str(song['lastPlayed']),song['album'],song['artist'],song['id'],song['disc'],song['track'],song['totalTracks'],song['genre'],song['url'],song['albumArtUrl'],song['durationMillis']])

		def getModel(self):
			return self.model