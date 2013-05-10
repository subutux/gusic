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
from gi.repository import Gtk
from lib.core.signals import Signals
import time
import threading
import os
from lib.core.config import Config
config = Config()

class Signals(Signals):
	def on_button_exit_clicked(self,widget):
		self.destroy(None)
	def on_entry_google_account_password_activate(self,widget):
		self.on_button_login_clicked(widget)
	def on_button_login_clicked(self,widget):
		entry_username = self.mSelf.loginBuilder.get_object("entry_google_account_user")
		entry_password = self.mSelf.loginBuilder.get_object("entry_google_account_password")
		label_status = self.mSelf.loginBuilder.get_object("label_login_status")
		img_ok_user = self.mSelf.loginBuilder.get_object("image_username_ok")
		img_ok_pass = self.mSelf.loginBuilder.get_object("image_password_ok")
		spinner_login = self.mSelf.loginBuilder.get_object("spinner_login")
		if config['login']['save_login_username']:
			config['login']['save_login_username_content'] = entry_username.get_text()

		doLogin = threading.Thread(target=self.mSelf.api.login,args=(entry_username.get_text(),entry_password.get_text()))
		label_status.set_text("Logging in ...")
		spinner_login.set_visible(True)
		spinner_login.active = True
		spinner_login.start()
		doLogin.start()
		while doLogin.isAlive():
			while Gtk.events_pending():
				Gtk.main_iteration()
		time.sleep(0.1)
		if self.mSelf.api.is_authenticated():
			config['tmp']['username'] = entry_username.get_text()
			img_ok_user.set_visible(True)
			img_ok_pass.set_visible(True)
			label_status.set_text("Downloading music information ...")
			fetchSongs = threading.Thread(target=self.mSelf.fetchMusicLibrary,args=(label_status,None))
			fetchSongs.start()
			while fetchSongs.isAlive():
				while Gtk.events_pending():
					Gtk.main_iteration()
			label_status.set_text("Downloading playlist information ...")
			fetchPlaylist = threading.Thread(target=self.mSelf.fetchPlaylistLibrary)
			fetchPlaylist.start()
			while fetchPlaylist.isAlive():
				while Gtk.events_pending():
					Gtk.main_iteration()
			spinner_login.set_visible(False)
			self.mSelf.loggedIn = True
			if config['login']['save_login']:
				self.mSelf.keyring.saveLoginDetails(entry_username.get_text(),entry_password.get_text())

			self.mSelf.startGusic(True)
		else:
			label_status.set_text("Unable to login.")

