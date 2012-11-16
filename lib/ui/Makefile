GLADE_FILES := $(wildcard *.glade)

build:$(GLADE_FILES).py

%.py:$(basename $@).py
	$(foreach FILE, $(GLADE_FILES), $(shell cp ui_template.py $(basename $(FILE)).py))