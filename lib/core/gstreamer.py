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
import pygst
pygst.require("0.10")
import gst
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
            self.player = gst.element_factory_make('playbin2','gusic')
            bus = self.player.get_bus()
            bus.add_signal_watch()
            bus.connect('message',self.on_message)
    def playpause(self,song,nope=None):
        if song == None and self.status == self.PLAYING:
            logging.debug('song is %b and self.status is %s',song,self.status)
            self.player.set_state(gst.STATE_PAUSED)
            self.status = self.PAUSED
            return self.status
        elif song == None and self.status == self.PAUSED:
            logging.debug('song is %b and self.status is %s',song,self.status)
            self.player.set_state(gst.STATE_PLAYING)
            self.status = self.PLAYING
            return self.status
        elif song == None and self.status == self.NULL:
            logging.debug('song is %b and self.status is %s',song,self.status)
            self.status = self.NULL
            return self.status
        elif song == None and self.status == self.STOP:
            logging.debug('song is %b and self.status is %s',song,self.status)
            return 42
        else:
            if self.nowplaying == None:
                logging.debug('song is %s, self.nowplaying is %b and self.status is %s',song,self.nowplaying,self.status)
                self.launch(song)
                return self.PLAYING
            elif song == self.nowplaying and self.status == self.PLAYING:
                logging.debug('song is %s, self.nowplaying is %b and self.status is %s',song,self.nowplaying,self.status)
                self.player.set_state(gst.STATE_PAUSED)
                self.state = self.PAUSED
                return self.state
            elif song == self.nowplaying and self.state == self.PAUSED:
                logging.debug('song is %s, self.nowplaying is %b and self.status is %s',song,self.nowplaying,self.status)
                self.player.set_state(gst.STATE_PLAYING)
                self.state = self.PAUSED
                return self.state
            else:
                self.stop()
                self.launch(song)
                return self.STOPPED
    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.nowplaying = None
        self.status = self.STOP
    def launch(self,song):
        if song is not None:
            self.player.set_property('uri',song)
            self.player.set_state(gst.STATE_PLAYING)
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
            timeF = gst.Format(gst.FORMAT_TIME)
            position =  self.player.query_position(timeF,None)[0]
        except gst.QueryError:
            position = 0
        return position
    def seek (self, seconds):
        value = int(gst.SECOND * seconds)
        time = gst.Format(gst.FORMAT_TIME)
        self.player.seek_simple(time,gst.SEEK_FLAG_FLUSH,value)
    def on_message(self,bus,message):
        _type = message.type
        if _type == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.status = self.NULL
        elif _type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.nowplaying = None
            self.status = self.NULL
            err, debug = message.parse_error()
            print 'GST-Error: %s' % err, debug