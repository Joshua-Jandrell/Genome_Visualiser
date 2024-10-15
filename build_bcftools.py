import os, subprocess, wget, shutil
from src import _config_

# bcftools install details
VERSION = 1.21
BCFTOOLS_URL = f"https://github.com/samtools/bcftools/releases/download/1.21/bcftools-{VERSION}.tar.bz2"
BCFTOOLS_DIR = f"bcftools-{VERSION}"



def install_bcftools():
    """Downloads and installs bcftools."""

    _target_path = os.path.realpath(_config_.BCFTOOLS_PATH.strip('.*').strip('.exe')+'.exe')

    BASE_PATH = os.path.dirname(__file__)
    print(f"Installing bcftools in {_target_path}")

    # Download file
    print(f"> Downloading bcftools version {VERSION}:")
    wget.download(BCFTOOLS_URL)
    print("\nDownload completed.\n")

    # Extract contents
    BCFTOOLS_FILE = os.path.basename(BCFTOOLS_URL)
    subprocess.run(f"tar -xf {BCFTOOLS_FILE}")

    # Try to find make cmd
    make_cmd = 'make'
    try:
        subprocess.run(f"{make_cmd} --version", stdout = subprocess.DEVNULL)
    except:
        # try again with possible cmd for windows device
        make_cmd = 'mingw32-make'
        try:
            subprocess.run(f"{make_cmd} --version", stdout = subprocess.DEVNULL)
            print(f"{make_cmd} detected.")
        except:
            print("No version of cmake detected: cannot build executable.")
    finally:
        print(f"> Building executable with {make_cmd}:")

        # Configure and build bcftools
        subprocess.run("bash ./configure", cwd=os.path.join(BASE_PATH,BCFTOOLS_DIR))
        subprocess.run(make_cmd, cwd=os.path.join(BASE_PATH,BCFTOOLS_DIR))

        # Find and move .exe to desired location
        _tmp_bcf_tool_path = os.path.join(BASE_PATH,BCFTOOLS_DIR,'bcftools.exe')
        os.makedirs(os.path.dirname(_target_path), exist_ok=True)
        shutil.move(_tmp_bcf_tool_path, _target_path)

        print("=============================================\n")

        # Check that build succeeded
        try:
            subprocess.run(f"{_target_path} --version")
        except:
            print("\n=============================================")
            print("Build failed. Please attempt manual install.")
        finally:
            print("\n=============================================")
            print("Build competed successfully.")
            print(f"> bcftools installed at {_target_path}")


    # Delete unneeded files and directories
    os.remove(BCFTOOLS_FILE)
    shutil.rmtree(BCFTOOLS_DIR)

if __name__ == "__main__":
    install_bcftools()