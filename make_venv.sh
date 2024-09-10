#!/usr/bin/env bash

if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    python -m venv .venv
    source .venv/Scripts/activate
else
    python3 -m venv .venv_2
    source .venv_2/bin/activate
fi

# Add depandancies
#python -m pip3 install customtkinter # For dashbaord app creation
#python -m pip install Flask
pip install numpy
pip install customtkinter
pip install matplotlib
pip install scikit-allel
pip install pandas
# requires c++ version 14 or higher