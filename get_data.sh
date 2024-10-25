#!/usr/bin/env bash
# Run this file to download some publically avaibale vcf data for testing

# Adapt python command 
VENV=".venv"
PYTHON='python3'
BIN='bin'

# Change python command based on OS
if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    PYTHON='python'
    BIN='Scripts'
fi

# Make venv if required, otheriwse activate it
if [ ! -d "$VENV" ]; then
    echo "=== Creating venv ==="
    "$PYTHON" -m venv "$VENV"
    source "$VENV"/"$BIN"/activate
    pip install -r requirements.txt
else
    source "$VENV"/"$BIN"/activate
fi

# Run script to get data
"$PYTHON" "util/getData.py"