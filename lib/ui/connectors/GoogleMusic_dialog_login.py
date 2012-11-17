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
from lib.core.signals import Signals
import threading
class Signals(Signals):
	def on_button_exit_clicked(self,widget):
		print "on_button_exit_clicked"
		self.destroy(None)
	def on_button_login_clicked(self,widget):
		print "on_button_login_clicked"
		entry_username = self.mSelf.loginBuilder.get_object("entry_google_account_user")
		entry_password = self.mSelf.loginBuilder.get_object("entry_google_account_password")
		label_status = self.mSelf.loginBuilder.get_object("label_login_status")
		img_ok_user = self.mSelf.loginBuilder.get_object("image_username_ok")
		img_ok_pass = self.mSelf.loginBuilder.get_object("image_password_ok")
		spinner_login = self.mSelf.loginBuilder.get_object("spinner_login")
		doLogin = threading.Thread(target=self.mSelf.api.login,args=(entry_username.get_text(),entry_password.get_text()))
		label_status.set_text("Logging in ...")
		spinner_login.set_visible(True)
		spinner_login.start()
		doLogin.start()
		while doLogin.isAlive():
			while Gtk.events_pending():
				Gtk.main_iteration()
		if self.mSelf.api.is_authenticated():
			label_status.set_text("Logged in!")
			img_ok_user.set_visible(True)
			img_ok_pass.set_visible(True)
			spinner_login.stop()
			spinner_login.set_visible(False)
		else:
			label_status.set_text("Unable to login.")

