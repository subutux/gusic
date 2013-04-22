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
# Copyright 2012-2013, Stijn Van Campenhout <stijn.vancampenhout@gmail.com
from gi.repository import Gtk
from cache import DB
import sqlite3
class sqliteListstore(object):
	def __init__(self,dbFile,name,tabelType):
		self.listStore = Gtk.ListStore(self.db.getListStoreCols(tableType))
		self.db = DB(dbFile)
		self.type = tableType
		self.table = tableType + '_' + name
		if not self.db._tableExists(self.table):
			self.db.createNew(self.type,self.table)
		else:
			#Fill the liststore with the table values
			for row in self.db.c.execute("SELECT ? from ?",", ".join(self.db.getListStoreTableMap(self.tableType)),self.table):
				self.listStore.append(list(row))

	def insert(self,dictValues):
		#This shoud work, not tested
		tableMap = self.db.getListStoreTableMap(self.tableType)
		for item in dictValues:
			v = []
			for mapper in tableMap:
				v.append(item[mapper])
			self.db.c.execute("INSERT INTO ? VALUES (?)",self.tableType,item)
			self.listStore.append(v)

		return True
	def update(self,treePath,dictValues):
		
		return True
	def remove(self,treePath):
		return True
	def getListstore(self):
		return self.listStore

