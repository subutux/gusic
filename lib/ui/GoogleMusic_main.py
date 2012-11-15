from gi.repository import Gtk
import os.path

def Build(connector):
	whereami =  os.path.dirname(os.path.realpath(__file__))
	whoami = os.path.splitext(__file__)[0]
	if os.path.exists(whoami + '.glade'):
		b =  Gtk.Builder()
		b.add_from_file(whoami + '.glade')
		b.connect_signals(connector)
		return b


