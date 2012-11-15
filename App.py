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