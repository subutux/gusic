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
	def __init__(self):
		self.storeDir = os.environ['HOME'] + '/.local/share/gusic'
		self.configFile = open(self.storeDir + '/config.json','r+')
		if self.configFile.read() == "":
			self.configFile.write('{}')
		self.jsonConfig = json.loads(self.configFile.read())
	def set(self,var,val):
		self.jsonConfig[var] = val;
		self.save()
	def get(self,var):
		return self.jsonConfig[var]
	def delete(self,var):
		del self.jsonConfig[var]
		self.save()
	def save(self):
		self.configFile.write(json.dumps(self.jsonConfig))
	def __getattr__(self,var):
		return self.get(var)
	def __setattr__(self,var,val):
		return self.set(var,val)
	def __delattr__(self,var):
		return self.delete(var)
	def __str__(self):
		return json.dumps(self.jsonConfig)
