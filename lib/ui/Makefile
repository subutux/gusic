GLADE_FILES := $(wildcard *.glade)

build:$(GLADE_FILES)
	$(echo "building files")
	$(foreach FILE, $(GLADE_FILES), $(shell cp ui_template.py $(basename $(FILE)).py))	
