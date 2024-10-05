"""
This script is used to load in assets.
NOTE This script must be in the same folder as app.py
"""
import os, toml

BASE_PATH = os.path.dirname(__file__)
"""The base path to all application assets."""

# Read in config data from toml
with open(os.path.join(BASE_PATH,'config.toml'), 'r') as f:
    config = toml.load(f)

# ==== Configure bcf tools ====

BCFTOOLS_PATH:str = os.path.join(BASE_PATH, config['bcftools']['path'])
"""The path to local bcftools erectable, if it exists."""

BCFTOOLS_CMD:str=BCFTOOLS_PATH
"""The command used to run bcftools"""
if not config['bcftools']['local']:
    BCFTOOLS_CMD = 'bcftools'
    

IMG_PATH:str = os.path.join(BASE_PATH, config['assets']['images'])
"""Path to all images (.png and .ico files)"""


