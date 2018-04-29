# coding=utf-8
import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, request, Response, render_template
import copy
import threading
import itchat
import ujson as json
import settings
import tools
import gevent
import matplotlib.pyplot as plt
import StringIO

app = Flask(__name__)


# @app.route('/')
# def test():
#     return render_template('friends.html')


@app.route('/')
def friend_list():
    rsp_data = copy.copy(settings.ERROR['SUCC'])

    name = request.values.get('name', '')
    if name:
        friend_list = itchat.search_friends(name=name)
    else:
        try:
            friend_list = itchat.get_friends(request.args.get('update', False))
        except Exception as e:
            rsp_data = copy.copy(settings.ERROR['ERROR'])
            rsp_data['data'] = e
            return Response(json.dumps(rsp_data), mimetype='application/json')
    records = list()

    for friend in friend_list:
        detail = {
            'nickname': friend['NickName'],
            'RemarkName': friend['RemarkName'],
            'signature': friend['Signature'],
            'sex': settings.SEX_CHOICES[int(friend['Sex'])],
            'City': friend['City'],
            'UserName': friend['UserName'],
        }
        records.append(detail)
    rsp_data['data'] = records
    rsp_data['name'] = name
    # return Response(json.dumps(rsp_data), mimetype='application/json')
    return render_template('friends_list.html', rsp_data=rsp_data)


@app.route('/chat/room/')
def chat_room():
    rsp_data = copy.copy(settings.ERROR['SUCC'])

    records = list()
    try:
        chatrooms = itchat.get_chatrooms(request.args.get('update', False))
    except Exception as e:
        rsp_data = copy.copy(settings.ERROR['ERROR'])
        rsp_data['data'] = e
        return Response(json.dumps(rsp_data), mimetype='application/json')
    for room in chatrooms:
        detail = {
            'nickname': room['NickName'],
            'memberCount': room['MemberCount'],
            'UserName': room['UserName']
        }
        records.append(detail)
    rsp_data['data'] = records
    return render_template('room_list.html', rsp_data=rsp_data)


@app.route('/sex/count/')
def sex_count():
    rsp_data = copy.copy(settings.ERROR['SUCC'])
    try:
        friend_list = itchat.get_friends(request.args.get('update', False))
    except Exception as e:
        rsp_data = copy.copy(settings.ERROR['ERROR'])
        rsp_data['data'] = e
        return Response(json.dumps(rsp_data), mimetype='application/json')
    man = woman = other = 0
    for friend in friend_list:
        sex = int(friend['Sex'])
        if sex == 1:
            man += 1
        elif sex == 0:
            woman += 1
        else:
            other += 1

    labels = ['man', 'woman', 'other']
    X = [man, woman, other]
    plt.pie(X, labels=labels, autopct='%1.2f%%')
    plt.title("friend sex count")

    s = StringIO.StringIO()
    plt.savefig(s)
    s.seek(0)
    return Response(s.read(), mimetype="image/png")


@app.route('/send/msg/')
def send_friend(times=1, name='', msg='', wait_time=0, split_time=1):
    rsp_data = copy.copy(settings.ERROR['SUCC'])
    times = int(request.values.get('times', 1))  # 发送次数
    split_time = times - 1 and int(request.values.get('split_time', 1))  # 每次发送间隔时间
    wait_time = int(request.values.get('wait_time', 0))  # 多少分钟后发送
    name = request.values.get('name', '') and request.values[name].decode('utf-8')  # 昵称
    msg = request.values.get('msg', '')

    username = request.values.get('username', None)
    if not username:
        user = itchat.search_friends(name=name) or itchat.search_chatrooms(name=name)
        if user:
            username = user[0]['UserName']
        else:
            rsp_data = copy.copy(settings.ERROR['NOT_EXIST_USER'])
            return Response(json.dumps(rsp_data), mimetype='application/json')
    params = {
        "times": times,
        "msg": msg,
        "toUsername": username,
        "split_time": split_time,
        "wait_time": wait_time
    }

    sync.send((tools.send_friend_handler, params))
    return Response(json.dumps(rsp_data), mimetype='application/json')


@app.route('/send/msg/all/')
def send_all():
    msg = request.values.get('msg', '')
    try:
        friend_list = itchat.get_friends(request.args.get('update', False))
    except Exception as e:
        rsp_data = copy.copy(settings.ERROR['ERROR'])
        rsp_data['data'] = e
        return Response(json.dumps(rsp_data), mimetype='application/json')
    q = list()
    for friend in friend_list:
        q.append(friend["UserName"])
    gevent.joinall([gevent.spawn(tools.send_all_handler, username, msg) for username in friend_list])


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    qr_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'QR.png')
    itchat_pkl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'itchat.pkl')
    if os.path.exists(qr_png):
        os.remove(qr_png)
    if os.path.exists(itchat_pkl):
        os.remove(itchat_pkl)
    login_thread = threading.Thread(target=itchat.auto_login,
                                    kwargs=(dict(hotReload=True, loginCallback=tools.loginCallback)))
    login_thread.start()
    sync = tools.sync_task()
    next(sync)
    app.run(host='127.0.0.1', port=8000, debug=False)
