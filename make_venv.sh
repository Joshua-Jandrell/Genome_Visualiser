#!/usr/bin/env bash

python -m venv .venv


if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Add depandancies
#python -m pip3 install customtkinter # For dashbaord app creation
#python -m pip install Flask
python -m pip install numpy
python -m pip install customtkinter
python -m pip install matplotlib