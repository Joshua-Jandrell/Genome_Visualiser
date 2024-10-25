"""
This script is used to load in assets.
NOTE This script must be in the same folder as app.py
"""
import os, toml, sys

BASE_PATH = os.path.dirname(__file__)
"""The base path to all application assets."""

# Read in config data from toml
with open(os.path.join(BASE_PATH,'config.toml'), 'r') as f:
    config = toml.load(f)

# ==== Configure bcf tools ====
BCFTOOLS_PATH:str = os.path.realpath(os.path.join(BASE_PATH, config['bcftools']['path']))
if sys.platform not in ["cygwin", "msys", "win32"]:
    BCFTOOLS_PATH = BCFTOOLS_PATH.strip(".exe")
"""The path to local bcftools erectable, if it exists."""

BCFTOOLS_CMD:str=BCFTOOLS_PATH
"""The command used to run bcftools"""
if not config['bcftools']['local']:
    BCFTOOLS_CMD = 'bcftools'
    
print(BASE_PATH, "is base")
IMG_PATH:str = os.path.realpath(os.path.join(BASE_PATH, config['assets']['images']))
"""Path to all images (.png and .ico files)"""

ERROR_RED = "#FF8585"


