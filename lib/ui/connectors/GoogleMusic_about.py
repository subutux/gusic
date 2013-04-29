from gi.repository import Gtk
from lib.core.signals import Signals
from lib.core import tools
import threading
import logging
import urllib2

class Signals(Signals):
	def on_click(self,widget):
		return True