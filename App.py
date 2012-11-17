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
from lib.ui import GoogleMusic_dialog_login
from lib.KeyRing import keyring
class Main_connectors(object):
	def __init__(self):
		self.mainBuilder = GoogleMusic_main.Build(None)
		self.main = self.mainBuilder.get_object('window1')
		self.keyring = keyring()
		if self.keyring.haveLoginDetails():
			self.main.show_all()
		else:
			self.loginBuilder = GoogleMusic_dialog_login.Build(None)
			self.loginDialog = self.loginBuilder.get_object('window_login')
			self.loginDialog.show_all()

class main():
	def __init__(self):
		app = Main_connectors()

		Gtk.main()


main()