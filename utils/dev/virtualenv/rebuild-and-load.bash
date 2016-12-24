#!/usr/bin/env bash

PROJECTNAME="python-access"
VIRTUALENVS="$HOME/.virtualenvs"

rm -rf $VIRTUALENVS/$PROJECTNAME/
virtualenv -p python3 $VIRTUALENVS/$PROJECTNAME/
source $VIRTUALENVS/$PROJECTNAME/bin/activate

set -x
pip install --upgrade pip
pip install -r requirements_dev.txt
pip install -e ./
set +x
