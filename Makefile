.PHONY: ui conda_setup conda_rel_setup pip_setup
ifndef CONDA_PREFIX
CONDA_PREFIX = $(HOME)/.conda/envs/2fa_env
endif


UIDIR = UI
uiFiles = $(patsubst $(UIDIR)/%.ui,ui_%.py,$(wildcard **/*.ui))

ui: $(uiFiles)

ui_%.py: $(UIDIR)/%.ui
	$(CONDA_PREFIX)/bin/pyside6-uic $< -o $(UIDIR)/$@

conda_setup:
	conda env create --file environment.yml

pip_setup:
	pip install -r requirements.txt

run: ui
	python main.py