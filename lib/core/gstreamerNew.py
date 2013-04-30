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
# import pygst
# pygst.require("0.10")
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst as gst
gst.is_initialized() or gst.init(None)
import logging
class GStreamer(object):
    def __init__(self):
        self.status = 'NULL'
        self.player = None
        self.nowplaying = None
        self.PLAYING = 'PLAYING'
        self.STOPPED = 'STOPPED'
        self.STOP = 'STOP'
        self.PAUSED = 'PAUSED'
        self.NULL = 'NULL'
    def set_playback(self):
        if self.player is None:

            self.player = gst.ElementFactory.make('playbin','gusic')
            bus = self.player.get_bus()

            bus.add_signal_watch_full(1)
            bus.connect('message',self.on_message)

    def playpause(self,song,nope=None):
        if song == None and self.status == self.PLAYING:
            logging.debug('song is %s and self.status is %s',song,self.status)
            self.player.set_state(gst.State.PAUSED)
            self.status = self.PAUSED
            return self.status
        elif song == None and self.status == self.PAUSED:
            logging.debug('song is %s and self.status is %s',song,self.status)
            self.player.set_state(gst.State.PLAYING)
            self.status = self.PLAYING
            return self.status
        elif song == None and self.status == self.NULL:
            logging.debug('song is %s and self.status is %s',song,self.status)
            self.status = self.NULL
            return self.status
        elif song == None and self.status == self.STOP:
            logging.debug('song is %s and self.status is %s',song,self.status)
            return 42
        else:
            if self.nowplaying == None:
                logging.debug('song is %s, self.nowplaying is %s and self.status is %s',song,self.nowplaying,self.status)
                self.launch(song)
                return self.PLAYING
            elif song == self.nowplaying and self.status == self.PLAYING:
                logging.debug('song is %s, self.nowplaying is %s and self.status is %s',song,self.nowplaying,self.status)
                self.player.set_state(gst.State.PAUSED)
                self.state = self.PAUSED
                return self.state
            elif song == self.nowplaying and self.state == self.PAUSED:
                logging.debug('song is %s, self.nowplaying is %s and self.status is %s',song,self.nowplaying,self.status)
                self.player.set_state(gst.State.PLAYING)
                self.state = self.PAUSED
                return self.state
            else:
                self.stop()
                self.launch(song)
                return self.STOPPED
    def stop(self):
        self.player.set_state(gst.State.NULL)
        self.nowplaying = None
        self.status = self.STOP
    def launch(self,song):
        if song is not None:
            self.player.set_property('uri',song)
            self.player.set_state(gst.State.PLAYING)
            self.status = self.PLAYING
            self.nowplaying = song
    def getnow(self):
        return self.nowplaying
    def getstatus(self):
        return self.status
    def getplayer(self):
        return self.player
    def getposition(self):
        try:
            timeF = gst.Format(gst.Format.TIME)
            position =  self.player.query_position(timeF,None)[0]
        except:
            position = 0
        return position
    def seek (self, seconds):
        value = int(gst.SECOND * seconds)
        time = gst.Format(gst.Format.TIME)
        self.player.seek_simple(time,gst.SeekFlags.FLUSH,value)
    def on_message(self,bus,message):

        print dir(message)
        _type = message.type
        if _type == gst.Message.new_eos:
            self.player.set_state(gst.State.NULL)
            self.status = self.NULL
        elif _type == gst.Message.new_error:
            self.player.set_state(gst.State.NULL)
            self.nowplaying = None
            self.status = self.NULL
            err, debug = message.parse_error()
            print 'GST-Error: %s' % err, debug