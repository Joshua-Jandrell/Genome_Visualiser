#!/usr/bin/env bash
PYTHON='python3'

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    PYTHON='python'
fi

# Load files for testing
"$PYTHON" util/getData.py --random none
"$PYTHON" -m unittest discover test/ 