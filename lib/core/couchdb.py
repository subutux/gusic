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
from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record

class GusicRecordTypes(object):
	self.music = 'http://dev.subutux.be/couchdb/GusicRecord_music'
	self.setting = 'http://dev.subutux.be/couchdb/GusicRecord_setting'
	self.playlist = 'http://dev.subutux.be/couchdb/GusicRecord_playlist'

class DB(object):
	def __init__(self):
		self.db = CouchDatabase('Gusic',create=True)
		self.RecordType = GusicRecordTypes()
		self.getPlaylistMethod = """function(doc) {emit(doc_id,doc)}"""
	def AddSong(self,songObj,quiet=True):
		r = Record(songObj,record_type=self.RecordType.music,record_id=songObj['songid'])
		if self.db.record_exists(songObj['songid']):
			rid = db.update_records(songObj['songid'],r)
		else:
			rid = db.put_record(r)
		if not quiet:
			return rid
		else:
			return True
	def AddSetting(self,settingObj,quiet=True):
		r = Record(settingObj,record_type=self.RecordType.setting)
		rid = db.put.record(r)
		if not quiet:
			return rid
		else:
			return True
	def AddPlaylist(self,playlistObj,quiet=True):
		r = Record(playlistObj,record_type=self.RecordType.playlist)
		rid = db.put.record(r)
		if not quiet:
			return rid
		else:
			return True