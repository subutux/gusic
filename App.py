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
from gi.repository import Gdk
from gi.repository import GLib
from lib.ui import GoogleMusic_main
from lib.ui import GoogleMusic_dialog_login
from lib.KeyRing import keyring
from gmusicapi.api import Api as gMusicApi
import threading
import time
class Gusic(object):
	def __init__(self):
		self.mainBuilder = GoogleMusic_main.Build(self,None)
		self.main = self.mainBuilder.get_object('window1')
		self.keyring = keyring()
		self.api = gMusicApi()
		self.Library = {}
		if self.keyring.haveLoginDetails():
			self.startGusic()
		else:
			self.loginBuilder = GoogleMusic_dialog_login.Build(self,None)
			self.loginDialog = self.loginBuilder.get_object('window_login')
			self.image_logo = self.loginBuilder.get_object('image_logo')
			self.image_logo.set_from_file('imgs/Gusic_logo.svg')
			self.loginDialog.show_all()

	def startGusic(self,fromLogin=False):
		self.main.show_all()
		if fromLogin:
			self.loginDialog.hide()
	def isLoggedIn(self):
		while self.loggedIn == False:
			time.sleep(0.5)
		return True
	def fetchMusicLibrary(self):
		self.Library['songs'] = self.api.get_all_songs()

class main():
	def __init__(self):
		GLib.threads_init()
		Gdk.threads_enter()
		app = Gusic()
		Gtk.main()
		Gdk.threads_leave()


main()