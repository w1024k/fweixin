# coding:utf-8

from time import sleep
import webbrowser
import threading
import itchat
import os
import settings


def loginCallback():
    webbrowser.open("http://127.0.0.1:8000/")


def sync_task():
    i = 0
    while True:
        run, params = yield
        threading.Thread(target=run, kwargs=params).start()
        print '%s start' % i
        i += 1


def send_friend_handler(times, msg, toUsername, split_time, wait_time):
    sleep(wait_time)
    for i in range(times):
        itchat.send(msg=msg, toUserName=toUsername)
        print '%s sucess' % i
        sleep(split_time)


def send_all_handler(username, msg):
    itchat.send(toUserName=username, msg=msg)


def clean_login_cache(*args):
    for file_name in args:
        file_path = os.path.join(settings.BASE_DIR, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
