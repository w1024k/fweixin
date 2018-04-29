# coding:utf-8

from time import ctime, sleep
# from socket import *
import webbrowser
import threading
import itchat
import matplotlib.pyplot as plt


def loginCallback():
    webbrowser.open("http://127.0.0.1:8000/")


# @app.task()
# def send_friend_cron(msg, toUsername):
#     itchat.send(msg=msg, toUserName=toUsername)
#     del app.conf['CELERYBEAT_SCHEDULE'][toUsername]



# def sock_server():
#     udpServer = socket(AF_INET, SOCK_DGRAM)
#     udpServer.bind(settings.SOCK_ADDR)
#
#     while True:
#         print('Waiting for connection...')
#         data, addr = udpServer.recvfrom()
#         data = "at %s :%s" % (ctime(), data)
#     udpServer.close()
#
#
# def sock_client(data):
#     udpClient = socket(AF_INET, SOCK_DGRAM)
#     udpClient.sendto(data, settings.SOCK_ADDR)
#     udpClient.close()



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
#
# def create_pie_image():
#
#     labels = ['China', 'Swiss', 'USA', 'UK', 'Laos', 'Spain']
#     X = [222, 42, 455, 664, 454, 334]
#     plt.pie(X, labels=labels, autopct='%1.2f%%')
#     plt.title("Pie chart")

    # plt.show()
    # plt.savefig("PieChart.jpg")





















