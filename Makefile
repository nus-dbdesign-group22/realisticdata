# set up the dev environment for a python project

# define the name of the virtual environment
VENV_NAME := venv

# define the path to the python executable in the virtual environment
PYTHON := $(VENV_NAME)/bin/python

# define the path to the pip executable in the virtual environment
PIP := $(VENV_NAME)/bin/pip

# define the list of requirements for the project
REQUIREMENTS := requirements.txt

# create the virtual environment
setup_env:
	python3 -m venv $(VENV_NAME)

# install the requirements
install: setup_env
	$(PIP) install -r $(REQUIREMENTS)

# build is just setup & install all at once
build: install

# remove the virtual environment and all installed packages
clean:
	rm -rf $(VENV_NAME)

# define the default target
.DEFAULT_GOAL := setup_env