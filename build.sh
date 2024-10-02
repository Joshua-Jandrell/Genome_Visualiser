#!/usr/bin/env bash

# Activate .vnev
if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    source .venv/Scripts/activate
else
    # Running on other (Unix/Linux/MacOs/etc)
    source .venv/bin/activate
fi

# Build file 
