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
import os
import urllib2
import logging
import sqlite3
from gi.repository import Gtk
from lib.core.config import Config
log = logging.getLogger('gusic')
class DB(object):
	def __init__(self,dbfile):
		self.dbfile = dbfile
		self.db = sqlite3.connect(dbfile)
		self.c = self.db.cursor()
		self.tableTypes = {
		"playlist": """CREATE TABLE ? (id,comment,rating,lastPlayed,disc,composer,year,album,title,
				deleted,albumArtist,type,titleNom,track,albumArtistNorm,totalTracks,
				beatsPerMinute,genre,playCount,creationDate,name,albumNorm,artist,
				url,totalDiscs,durationMilis,artistNorm,subjectToCuration,matchedId,
				albumArtUrl)"""
		}
		self.listStoreTypes = {
		"playlist" : (int,str,str,str,str,str,int,int,int,str,str,str,int)
		}
		self.listStoreTableMaps = {
		"playlist": ["type","title","lastPlayed","album","albumArtist","id","disc","track","totalTracks","genre","url","albumArtUrl","durationMilis"]
		}
	def cleanDB(self):
		log.info('closing DB')
		self.db.close()
		try:
			os.remove(self.dbfile)
		except:
			log.exeception('Exception while removing dbfile: %s',self.dbfile)
			return False
		self.db = sqlite3.connect(self.dbfile)
		self.c = self.db.cursor()
		self._initDB()
	def _initDB(self):
		log.info("Initializing database %s: TABLE settings",self.dbfile)
		self.c.execute('''CREATE TABLE settings 
			(id,setting,value)''')
		log.info("Initializing database %s: TABLE all_songs",self.dbfile)
		self.c.execute('''CREATE TABLE all_songs
			(id,comment,rating,lastPlayed,disc,composer,year,album,title,
				deleted,albumArtist,type,titleNom,track,albumArtistNorm,totalTracks,
				beatsPerMinute,genre,playCount,creationDate,name,albumNorm,artist,
				url,totalDiscs,durationMilis,artistNorm,subjectToCuration,matchedId,
				albumArtUrl)''')
	def convertForSqlite(songs):
		output = []
		for song in songs:
			if not albumArt in s:
				song['albumArt'] = 'null'
			if not 'disc' in song:
				song['disc'] = 0
			if not 'track' in song:
				song['track'] = 0
			if not 'totalTracks' in song:
				song['totalTracks'] = 0
			s = tuple(song['id'],song['comment'],song['rating'],song['lastPlayed'],song['disc'],song['composer'],
				song['year'],song['album'],song['title'],song['deleted'],song['albumArtist'],song['type'],
				song['titleNom'],song['track'],song['albumArtistNorm'],song['totalTracks'],song['beatsPerMinute'],
				song['genre'],song['playCount'],song['creationDate'],song['name'],song['albumNorm'],song['artist'],
				song['url'],song['totalDiscs'],song['durationMilis'],song['artistNorm'],song['subjectToCuration'],
				song['matchedId'],song['albumArtUrl'])
			output.append(s)
		return output
	def saveAllSongs(self,songs):
		try:
			self.c.executemany("INSERT INTO all_songs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",self.convertForSqlite(songs))
		except sqlite3.Error:
			log.exception("Exception while importing all songs:")
			return False
		else:
			return True
	def allIn(self,tableType,table):
		return self.c.execute("SELECT * FROM " + tableType + "_" + table + ";")
	def insert(self,tableType,table,data):
		return True
	def _tableExtist(self,table):
		ret = self.c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;",table)
		result = ret.fetchone()
		if result[0] == 1:
			return True
		else:
			return False
	def createNew(self,tableType,table):
		if tableType in self.tableTypes:
			self.c.execute(self.tableTypes[tableType],tableType + '_' + table)
		else:
			return False
		return True
	def getListStoreCols(self,tableType):
		if tableType in self.listStoreTypes:
			return self.listStoreTypes[tableType]
	def getListStoreTableMap(self,tableType):
		if tableType in self.listStoreTableMaps:
			return self.listStoreTableMaps[tableType]

class SqlListStore(Gtk.ListStore):
	def __init__(self,DBClass,tableType,table):
		self.db = DBClass
		Gtk.ListStore.__init__(self.db.listStoreTypes[tableType])
		if not self.db._tableExtist(tableType + '_' + table):
			self.db.createNew(tableType,table)
		else:
			for row in self.db.allIn(tableType,table):
				self.listStoreAppend(list(row))
	def listStoreAppend(self,data):
		return __parent__.append(data)
	def append(self,data):
		return True

class Cache(object):
	def __init__(self):
		config = Config()
		self.cacheLocation = config['locations']['basedir'] + '/' + config['locations']['cachedir'] + '/' + config['tmp']['username']
		self.cacheImages = self.cacheLocation + '/images'
		self.cacheDatabase = self.cacheLocation + '/gusic.cache.db'
		log.debug("CacheLocation = %s" % self.cacheLocation)
		if not os.path.isdir(self.cacheLocation):
			os.makedirs(self.cacheLocation)
		if not os.path.isdir(self.cacheImages):
			os.makedirs(self.cacheImages)
	def checkImageCache(self,cacheURLs,auto_cache=True,quiet=True):
		log.debug("starting with auto_cache=%s and quiet=%s",str(auto_cache),str(quiet))
		cache = []
		for url in cacheURLs:
			log.debug("starting url <%s>",url)
			try:
				fname = url.rsplit('/',1)[1]
			except:
				log.exception("Exception while splitting url %s",url)
				return False
			
			if not os.path.isfile(self.cacheImages + '/' + fname):
				log.debug("file %s is not cached",fname)
				if auto_cache:
					log.debug('downloading <%s> to %s',url,fname)
					ul = urllib2.urlopen(url)
					open(self.cacheImages + '/' + fname,'w').write(ul.read())
			if not quiet:
				cache.append(self.cacheImages + '/' + fname)
		if not quiet:
			return cache
		else:
			return True

	def getImageFromCache(self,url):
		fname = url.rsplit('/',1)[1]
		if os.path.isfile(self.cacheImages + '/' + fname):
			return self.cacheImages + '/' + fname
		else:
			return False
	def imageIsCached(self,url):
		fname = url.rsplit('/',1)[1]
		if os.path.isfile(self.cacheImages + '/' + fname):
			return True
		else:
			return False
	def getLibraryCache(self):

class LibraryCache(object):
	"""A Class for handling the library cache.

	It caches the raw JSON into gusic.db.json file in the default cache location
	and loads it when needed.

	"""
	def __init__(self,fetchLibraryFunction):
		self.fetchLib = fetchLibraryFunction
		self.cacheLocation = config['locations']['basedir'] + '/' + config['locations']['cachedir'] + '/' + config['tmp']['username']
		self.cachefile = self.cacheLocation + '/gusic.db.json'

	def backgroundSync(self):
		"""Function to sync the local library.

		This function is meant to run into a thread. It fetches the library via the self.fetchLib function,
		converts it to json, generates an md5 hash and compares it with the md5 hash of the current library.
		if those aren't equal, replace (or iterate over the current library) the current library with the new
		one and initiate a listStore resync.
		"""
		#TODO: How do I initiate a listStore resync, without breaking the treeView connection? Find the 
		#      differences and replace?

	def getLibrary(self):
		""" get the cached library """
		if os.path.isfile(self.cachefile):
			return json.loads(open(self.cachefile,'r').read())
		else:
			return False
			""" library not cached """
	def forceCache(self):
		""" Force a resync of the remote library, a clean dump """
		lib = self.fetchLib()
		if lib not None:
			jsonRaw = json.dumps(lib)
			open(self.cachefile,'w').write(jsonRaw)
		else:
			return False
	def find(self):
		lib = self.getLibrary()
		return searchDict(lib)

class searchDict(object):
	""" a simple dictsearch class

	using a simple "where" clause
	returns a instance of a searchDict with the results
	"""
	def __init__(self,dictionary):
		self.dict = dictionary
	def where(self,var,compare,value):
		comparitors = ['equals' ,'not equals', 'greater', 'lower']
		result = []
		if compare not in comparitors:
			return False
		else
		if compare == "equals":
			for i in self.dict:
				if i[var] == val:
					result.append(i)
		elif compare == "not equals":
			for i in self.dict:
				if i[var] != val:
					result.append(i)
		elif compare == "greater":
			for i in self.dict:
				if i[var] > val:
					result.append(i)
		elif compare == "lower":
			for i in self.dict:
				if i[var] < val:
					result.append(i)
		return searchDict(result)
	def __iter__(self):
		return self.dict.__iter__()
	def __getitem__(self,var):
		return self.dict[var]
