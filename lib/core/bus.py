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
import logging
class Bus(object):
	def __init__(self):
		self.events = {}
	def registerEvent(self,event):
		logging.debug("registering event %s",event)
		self.events[event] = [];
	def connect(self,event,function):
		logging.debug("connecting %s to event %s",function.__name__,event)
		self.events[event].append(function)
	def emit(self,event):
		logging.debug("emitting event %s",event)
		if self.events is not []:
			for function in self.events[event]:
				function()
