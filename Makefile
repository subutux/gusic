prefix=/usr
PREV_VERSION=$(shell cat VERSION.txt)
VERSION=$(shell git describe)
BIN=$(DESTDIR)$(prefix)/bin
DATADIR=$(DESTDIR)$(prefix)/share
MANDIR=$(DATADIR)/man
APPNAME=gusic
EASY_INSTALL=/usr/bin/easy_install
all:

package-prep:
		@echo "__version__ = \"$(VERSION)\"" > lib/_version.py
		@echo "$(VERSION)" > VERSION.txt

clean:
		rm -rf lib/*py[co]
		rm -rf lib/ui/*.py[co]
		rm -rf lib/core/*.py[co]
		rm -rf *.py[co]

changelog:
		@git log $(PREV_VERSION)... --pretty > CHANGELOG

changelog-append:
		@echo "" >> CHANGELOG
		@git log $(PREV_VERSION).. --pretty >> CHANGELOG

install:
		install -d $(BIN) $(DATADIR)/$(APPNAME) $(DATADIR)/$(APPNAME)/imgs $(DATADIR)/$(APPNAME)/lib $(DATADIR)/$(APPNAME)/lib/ui
		install -d $(DATADIR)/$(APPNAME)/lib/ui/connectors $(DATADIR)/$(APPNAME)/lib/core
 
		install -m644 imgs/*.png $(DATADIR)/$(APPNAME)/imgs
		install -m644 imgs/*.svg $(DATADIR)/$(APPNAME)/imgs

		install -m644 lib/*.py $(DATADIR)/$(APPNAME)/lib/
		install -m644 lib/ui/*.py $(DATADIR)/$(APPNAME)/lib/ui
		install -m644 lib/ui/*.glade $(DATADIR)/$(APPNAME)/lib/ui
		install -m644 lib/ui/*.xml $(DATADIR)/$(APPNAME)/lib/ui
		install -m644 lib/ui/connectors/*.py $(DATADIR)/$(APPNAME)/lib/ui/connectors/
		install -m644 lib/core/*.py $(DATADIR)/$(APPNAME)/lib/core/
		install -m644 lib/core/*.css $(DATADIR)/$(APPNAME)/lib/core/
 		
		install -m644 Gusic.desktop $(DATADIR)/applications
		install -m644 imgs/Gusic_logo-128.png $(DATADIR)/pixmaps
		install -m755 gusic $(BIN)
		install -m755 App.py $(DATADIR)/$(APPNAME)/
		cd lib/ui; make build
		${EASY_INSTALL} gmusicapi


uninstall:
		rm -f $(DATADIR)/applications/Gusic.desktop
		rm -f $(DATADIR)/pixmaps/Gusic_logo-128.png
		rm -f $(BIN)/gusic
		rm -rf $(DATADIR)/$(APPNAME)
 