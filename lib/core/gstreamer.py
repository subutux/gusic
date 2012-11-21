# -*- coding: utf-8 -*-

# This file is part of google-music

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Original code from the Bluemindo project
# Bluemindo: A really simple but powerful audio player in Python/PyGTK.
# Copyright (C) 2007-2009  Erwan Briand

from random import randrange
from urllib import pathname2url
from os.path import exists
import gst

class GStreamer(object):
    ref = None
    ref2 = None

    def __new__(cls, *args, **kws):
        # Singleton
        if cls.ref is None:
            cls.ref = object.__new__(cls)
        return cls.ref

    def __init__(self): 
        if GStreamer.ref2 is None: 
            GStreamer.ref2 = 42 
            self.nowplaying = None
            self.status = 'NULL'
            self.player = None

    def set_playback(self, playback):
        # Gstreamer initialization
        self.playback = playback

        try:
            vol = self.player.get_property('volume')
            force_volume = True
        except AttributeError:
            force_volume = False

        if self.player is None:
            self.player = gst.element_factory_make('playbin2', 'gusic')
            #self.player.set_property('flags','soft-volume+audio+buffering')
            self.equalizer = gst.element_factory_make('equalizer-10bands')

            audioconvert = gst.element_factory_make('audioconvert')
            audiosink = gst.element_factory_make('autoaudiosink')

            # sinkbin = gst.Bin()
            # sinkbin.add(self.equalizer, audioconvert, audiosink)
            # gst.element_link_many(self.equalizer, audioconvert, audiosink)

            # sinkpad = self.equalizer.get_static_pad('sink')
            # sinkbin.add_pad(gst.GhostPad('sink', sinkpad))

            self.player.set_property('audio-sink', audiosink)

            bus = self.player.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self.on_message)

        if force_volume:
            self.player.set_property('volume', vol)

    def playpause(self, song):
        # We want to pause the current song
        if song == None and self.status == 'PLAYING':
            self.player.set_state(gst.STATE_PAUSED)
            self.status = 'PAUSED'
            return self.status
        # We want to play the current song
        elif song == None and self.status == 'PAUSED':
            self.player.set_state(gst.STATE_PLAYING)
            self.status = 'PLAYING'
            return self.status
        # Nothing have been done
        elif song == None and self.status == 'NULL':
            self.status = 'NULL'
            return self.status
        # Huh, we can't do anything
        elif song == None and self.status == 'STOP':
            return 42
        else:
            # Launch this song
            if self.nowplaying == None:
                self.launch(song)
                return 'PLAYING'
            else:
                # The sended song is already playing: pause it
                if song == self.nowplaying and self.status == 'PLAYING':
                    self.player.set_state(gst.STATE_PAUSED)
                    self.status = 'PAUSED'
                    return self.status
                # The sended song is already pausing: play it
                elif song == self.nowplaying and self.status == 'PAUSED':
                    self.player.set_state(gst.STATE_PLAYING)
                    self.status = 'PLAYING'
                    return self.status
                # Launch this song
                else:
                    self.stop()
                    self.launch(song)
                    return 'STOPPED'

    def stop(self):
        # Stop listening
        self.player.set_state(gst.STATE_NULL)
        self.nowplaying = None
        self.status = 'STOP'

    def launch(self, song):
        self.nowplaying = song

        # Launch a song by URI
        if song is not None and exists(song):
            song = pathname2url(song)
            self.player.set_property('uri', 'file://' + song)
        elif song is not None:
            self.player.set_property('uri', song)

        self.player.set_state(gst.STATE_PLAYING)
        self.status = 'PLAYING'

    def getnow(self):
        return self.nowplaying

    def getstatus(self):
        return self.status

    def getplayer(self):
        return self.player

    def getequalizer(self):
        return self.equalizer

    def getposition(self):
        # Return the position in the song
        return self.player.query_position(gst.FORMAT_TIME)[0]

    def seek(self, seconds):
        # Go to a position in the song
        value = int(gst.SECOND * seconds)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH,
                                value)

    def on_message(self, bus, message):
        # Handle Gstreamer messages
        if self.playback == 'gapless':
            return

        _type = message.type
        if _type == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.status = 'NULL'

        elif _type == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.nowplaying = None
            self.status = 'NULL'
            err, debug = message.parse_error()
            print 'Error: %s' % err, debug