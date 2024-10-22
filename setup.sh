#!/usr/bin/env bash
# Run this file to download some publically avaibale vcf data for testing

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

# Make venv if required, otheriwse activate it
if [ ! -d "$VENV" ]; then
    echo "=== Creating venv ==="
    "$PYTHON" -m venv "$VENV"
    source "$VENV"/"$BIN"/activate
    pip install -r requirements.txt
else
    source "$VENV"/"$BIN"/activate
fi

if [ ! -z "$1" ]; then
    if [ "$1" == 'Local' ]; then 
        if [ ! -f $BCFTOOLS_PATH ]; then
            echo "=== Building bcftools ==="
            "$PYTHON" build_bcftools.py
        else
            echo "Bcftools build exists"
        fi
    else
        echo "Use 'bash setup.sh Local' to build bcftools locally"
    fi
fi

