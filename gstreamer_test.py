import pygst
pygst.require("0.10")
import gst

def on_tag(bus, msg):
    taglist = msg.parse_tag()
    print 'on_tag:'
    for key in taglist.keys():
        print '\t%s = %s' % (key, taglist[key])

#our stream to play
music_stream_uri = 'http://o-o---preferred---sn-bvvbax-5ogl---v14---lscache7.c.doc-0-0-sj.sj.googleusercontent.com/videoplayback?id=4868ae8d7ad957a8&itag=25&source=skyjam&o=06072533456067211717&ip=0.0.0.0&ipbits=0&expire=1353595342&sparams=id,itag,source,o,ip,ipbits,expire&signature=5A39341A6856F75BF700C7265CEA801B17B310C5.4C0F08A062E41FA4B2064EB49827B996FEB90EA3&key=sj2'

#creates a playbin (plays media form an uri) 
player = gst.element_factory_make("playbin", "player")

#set the uri
player.set_property('uri', music_stream_uri)

#start playing
player.set_state(gst.STATE_PLAYING)

#listen for tags on the message bus; tag event might be called more than once
bus = player.get_bus()
bus.enable_sync_message_emission()
bus.add_signal_watch()
bus.connect('message::tag', on_tag)

#wait and let the music play
raw_input('Press enter to stop playing...')
