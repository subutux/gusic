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
from lib.ui import GoogleMusic_main
class Main_connectors(object):
	def __init__(self):
		self.Builder = GoogleMusic_main.Build(self)
		self.main = self.Builder.get_object('window1')
		self.main.show_all()
	def on_toolbutton_play_clicked(self,widget):
		print "on_toolbutton_play_clicked"
	def destroy(self,window):
		Gtk.main_quit()
class main():
	def __init__(self):
		app = Main_connectors()

		Gtk.main()


main()