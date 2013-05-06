Gusic - A Google Music player
=============================

Gusic is a GTK 3+ based music player written in python. It's my first complete GUI app. I know you can use the web interface, but this project
is to show me what the posibilities are from GTK & Python and how far I can go.

It's actually my self-learning project. But feel free to use it!

Installing
-----------

checkout the git 

```bash
git checkout http://github.com/subutux/gusic/
```

and run the makefile install section:

```bash
sudo make install
``` 

Make shure you've got the following dependicies:

```bash
python-setuptools python-gst0.10 libgirepository1.0-1 #and maybe others..
```

The makefile automatically installs the [gmusicapi](https://github.com/simon-weber/Unofficial-Google-Music-API/) by using easy_install


So, What does it do?
--------------------

It loads your Google Music library and makes it browsable & playable. It has the basic functionality of a media player.

Why does'nt [thing] work?
-------------------------

Because this is actually a playground for me & there is no strict development flow in this project. It's a "Do I want to code and do I have the time" - development flow.

