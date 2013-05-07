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

import json
import os
class Config(object):
	def __init__(self,contents=None):
		self.storeDir = os.environ['HOME'] + '/.local/share/gusic'
		self.configFile = self.storeDir + '/config.json'
		self.jsonConfig = []
		self.default = json.dumps(contents)
		self._load(self.configFile)
	def _createFile(self,filePath):
		if not self.default:
			self.default = "{}"
		fdw = open(filePath,'w+')
		fdw.write(self.default)
		fdw.close()
	def _load(self,filePath):
		try:
			fdr = open(filePath,'r')
			if fdr.read() == "":
				fdr.close()
				self._createFile()
				fdr = open(filePath,'r')
		except:
			self._createFile(filePath)
			fdr = open(filePath,'r')
		print fdr.read()
		fdr.seek(0)
		self.jsonConfig = json.loads(fdr.read())
		fdr.close()
	def set(self,var,val):
		self.jsonConfig[var] = val;
		self._save()
	def get(self,var):
		if isinstance(self.jsonConfig[var],dict):
			print "got dict"
			return ConfigProxy(self,var,self.jsonConfig[var])
		else:
			return self.jsonConfig[var]
	def delete(self,var):
		del self.jsonConfig[var]
		self.save()
	def _save(self):
		fd = open(self.configFile,'w')
		fd.write(json.dumps(self.jsonConfig))
		fd.close()
	def __getitem__(self,var):
		return self.get(var)
	def __setitem__(self,var,val):
		return self.set(var,val)
	def __delitem__(self,var):
		return self.delete(var)
	def __iter__(self):
		return self.jsonConfig.__iter__()
	def __str__(self):
		return json.dumps(self.jsonConfig)

class ConfigProxy(object):
	def __init__(self,ConfigObj,name,var):
		self.configObj = ConfigObj
		self.jsonSubConfig = var
		self.name = name
	def __getitem__(self,var):
		return self.jsonSubConfig.get(var)
	def __setitem__(self,var,val):
		self.jsonSubConfig[var] = val
		return self.configObj.set(self.name,self.jsonSubConfig)
	def __delitem__(self,var):
		del(self.jsonSubConfig[var])
		return self.configObj.set(self.name,self.jsonSubConfig)
	def __str__(self):
		return json.dumps(self.jsonSubConfig)
	def __iter__(self):
		return self.jsonSubConfig.__iter__()
