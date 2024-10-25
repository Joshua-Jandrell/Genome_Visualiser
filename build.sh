#!/usr/bin/env bash
# Run this file to set up all required venv dependancies
#pyinstaller --add-data "src/assets/bin/*.exe:assets/bin/" --add-data "src/assets/img/*.ico:assets/img/"  --add-data "src/*.toml:." --icon "src/assets/img/icon.ico" src/app.py

VENV=".venv"
PYTHON='python3'
BIN='bin'

BCFTOOLS_PATH='src/assets/bin/bcftools'

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    PYTHON='python'
    BIN='Scripts'

    BCFTOOLS_PATH='src/assets/bin/bcftools.exe'
fi

if [ ! -d "$VENV" ]; then
    echo "=== Creating venv ==="
    "$PYTHON" -m venv "$VENV"
    source "$VENV"/"$BIN"/activate
    pip install -r requirements.txt
else
    source "$VENV"/"$BIN"/activate
fi

if [ ! -f $BCFTOOLS_PATH ]; then
    echo "=== Building bcftools ==="
    "$PYTHON" build_bcftools.py
fi


pyinstaller app.spec
