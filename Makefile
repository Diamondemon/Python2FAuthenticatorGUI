PHONY: ui
ifndef CONDA_PREFIX
CONDA_PREFIX = /home/julien/.conda/envs/dev
endif


UIDIR = UI
uiFiles = $(patsubst $(UIDIR)/%.ui,ui_%.py,$(wildcard **/*.ui))

ui: $(uiFiles)

ui_%.py: $(UIDIR)/%.ui
	pwd
	$(CONDA_PREFIX)/bin/pyside6-uic $< -o $(UIDIR)/$@
