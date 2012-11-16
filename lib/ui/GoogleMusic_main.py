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
import os.path

def Build(connector):
	whereami =  os.path.dirname(os.path.realpath(__file__))
	whoami = os.path.splitext(__file__)[0]
	print whoami
	if os.path.exists(whoami + '.glade'):
		b =  Gtk.Builder()

		b.add_from_file(whoami + '.glade')
		b.connect_signals(connector)
		return b
Build("self")