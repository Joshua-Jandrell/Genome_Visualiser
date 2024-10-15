"""
This script is used to load in vcf data for testing according to data_config.toml
"""

import toml, wget, os, shutil

CONFIG_PATH = "data_config.toml"
CONFIG = toml.load(os.path.join(os.path.dirname(__file__),CONFIG_PATH))

def get_dest(url:str)->str:
    return os.path.join(CONFIG['directories']['data'], os.path.basename(url))

def load_vcf_data():
    """Loads in the vcf data case files"""

    print("\nDownloading .vcf files...\n")
    # Make data directory 
    os.makedirs(CONFIG['directories']['data'], exist_ok=True)

    # Load files
    files:dict = CONFIG['data']
    for url in files.values:
        _dest = get_dest(url)

        # Skip file if it already exists.
        if os.path.isfile(_dest):
            continue
        
        print(f"\n> Downloading {_dest}:")
        _file_path = wget.download(url)
        shutil.move(_file_path, _dest)

    print("\nAll .vcf files downloaded. \n------------------------------\n")


def load_case_data():
    """Downloads all case and control files to be used for testing."""

    print("\nDownloading case/ctrl files...\n")
    # Make data directory 
    os.makedirs(CONFIG['data_dir'], exist_ok=True)

    # Load files
    files:dict = CONFIG['case-ctrl']
    for url in files.values():
        _dest = get_dest(url)

        # Skip file if it already exists.
        if os.path.isfile(_dest):
            continue
        
        print(f"\n> Downloading {_dest}:")
        _file_path = wget.download(url)
        shutil.move(_file_path, _dest)

    print("\nAll case/ctrl files downloaded. \n------------------------------\n")

def all_data_loaded()->bool:
    """"Returns true if all data has been downloaded."""

    for type in ['case-ctrl', 'data']:
        for url in CONFIG[type].values():
            _dest = get_dest(url)

            if not os.path.isfile(_dest):
                return False
    
    # If this point is reached then all data has been loaded.
    return True

def load_all_data():
    if not all_data_loaded():
        load_vcf_data()
        load_case_data()


if __name__ == "__main__":
    if not all_data_loaded():
        load_all_data()
    else:
        print("All data is loaded.")
