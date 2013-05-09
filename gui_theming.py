#!/usr/bin/env python
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
from gi.repository import Gtk, Gdk, GObject, GLib

from lib.ui import GoogleMusic_main
from lib.ui import GoogleMusic_dialog_login
from lib.ui import GoogleMusic_about
from lib.ui import GoogleMusic_log

GObject.threads_init()

class main(object):
	def __init__(self):
		GLib.threads_init()
		Gdk.threads_enter()
		self.window_main_builder = GoogleMusic_main.Build(None,None)
		self.window_main = self.window_main_builder.get_object('window1')
		self.window_main.set_wmclass ("Gusic", "Gusic")
		self.window_main.set_title('Gusic')
		self.window_main_builder.get_object('treeview_media_view').set_name('treeview_media_view')
		self.window_main_builder.get_object('treeview_main_song_view').set_name('treeview_main_song_view')
		self.window_main_builder.get_object('viewport1').set_name('display')
		self.window_main.set_name('window_main')
		self.GtkScreen = Gdk.Screen.get_default()
		self.style_context = Gtk.StyleContext()
		self.css_provider = Gtk.CssProvider()
		self.css_provider.load_from_path('lib/core/styles.css')
		self.style_context.add_provider_for_screen(self.GtkScreen,self.css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.window_main.show_all()
		Gtk.main()
		Gdk.threads_leave()
m = main()