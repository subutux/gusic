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
# Copyright 2012-2013, Stijn Van Campenhout <stijn.vancampenhout@gmail.com
from gi.repository import Gtk
from cache import DB
import sqlite3
class sqliteListstore(object):
	def __init__(self,listStore,dbFile,table,tabelType):
		self.listStore = listStore
		self.db = DB(dbFile)
		self.table = table
		self.type = tableType
		if not self.db._tableExists(self.table):
			self.db.createNew(self.type,self.table)
	def insert(self,dictValues):
		return True
	def update(self,treePath,dictValues):
		return True
	def remove(self,treePath):
		return True

