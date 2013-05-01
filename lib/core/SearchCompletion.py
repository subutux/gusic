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
from gi.repository import Gtk, GdkPixbuf
class SearchCompletion():
	"""
	Builds a ListStore with information of the mainStore
	containing all the song, album an artist names for
	matching angainst a completion form.
	"""
	def __init__(self,mainStore):
		self.mainStore = mainStore
		self.tmpStore = {
			'albums' : [],
			'artists' : []
		}
		self.matchStore = Gtk.ListStore(str,str,str,GdkPixbuf.Pixbuf)
		#										 |
		#								 |	 |	id (if any, else 'none')
		#								 |	text
		#								type (song,album,artist)
		self.iconSong = GdkPixbuf.Pixbuf.new_from_file('imgs/icon-song-16.png')
		self.iconArtist = GdkPixbuf.Pixbuf.new_from_file('imgs/icon-artist-16.png')
		self.iconAlbum = GdkPixbuf.Pixbuf.new_from_file('imgs/icon-album-16.png')
		
		self.update_matchStore()

	def update_matchStore(self):
		"""
		Updates the matchStore with the information of the mainStore
		"""
		self.matchStore.clear()
		self.tmpStore['albums'] = []
		self.tmpStore['artists'] = []
		item = self.mainStore.get_iter_first()
		while (item != None):
			song = self.mainStore.get_value(item,1)
			album = self.mainStore.get_value(item,3)
			artist = self.mainStore.get_value(item,4)
			#song
			self.matchStore.append(['song',song,self.mainStore.get_value(item,5),self.iconSong])
			#album
			if album not in self.tmpStore['albums']:
				self.tmpStore['albums'].append(album)
				self.matchStore.append(['album',album,'none',self.iconAlbum])
			#artist
			if artist not in self.tmpStore['artists']:
				self.tmpStore['artists'].append(artist)
				self.matchStore.append(['artist',artist,'none',self.iconArtist])
			item = self.mainStore.iter_next(item)
	def get_matchStore(self):
		return self.matchStore

