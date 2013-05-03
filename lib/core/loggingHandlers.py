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
from gi.repository import Gtk
class ListStoreLoggingHandler(logging.Handler):
	def __init__(self,liststore):
		self.liststore = liststore
		self.level = 9
		self.filters = []
		self.lock = False
		# Liststore:
		# - log_time
		# - log_type
		# - log_line
		# - log_color
		# - log_lineNo
		# - log_source
		# - log_module
		# - log_logname
		# - log_funcname
	def emit(self,r):
		if r.levelname == 'DEBUG':
			color = 'grey'
		elif r.levelname == 'INFO':
			color = 'yellow'
		elif r.levelname == 'WARNING':
			color = 'blue'
		elif r.levelname == 'ERROR' or r.levelname == 'CRITICAL':
			color = 'red'

		self.liststore.append([str(r.created),r.levelname,str(r.getMessage()),
			color,str(r.lineno),r.filename,r.module,r.name,r.funcName])
