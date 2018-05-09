# coding=utf-8
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


@app.route('/')
def friend_list():
    rsp_data = copy.copy(settings.ERROR['SUCC'])

    name = request.values.get('name', '')
    if name:
        friends = itchat.search_friends(name=name)
    else:
        try:
            friends = itchat.get_friends(request.args.get('update', False))
        except Exception as e:
            rsp_data = copy.copy(settings.ERROR['ERROR'])
            rsp_data['data'] = e
            return Response(json.dumps(rsp_data), mimetype='application/json')
    records = list()

    for friend in friends:
        detail = {
            'nickname': friend['NickName'],
            'RemarkName': friend['RemarkName'],
            'signature': friend['Signature'],
            'sex': settings.SEX_MAPPING[int(friend['Sex'])],
            'City': friend['City'],
            'UserName': friend['UserName'],
        }
        records.append(detail)
    rsp_data['data'] = records
    rsp_data['name'] = name
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
    try:
        friends = itchat.get_friends(request.args.get('update', False))
    except Exception as e:
        rsp_data = copy.copy(settings.ERROR['ERROR'])
        rsp_data['data'] = e
        return Response(json.dumps(rsp_data), mimetype='application/json')
    man_count = woman_count = other_count = 0
    for friend in friends:
        sex_num = int(friend['Sex'])

        if settings.SexEnum.MAN == sex_num:
            man_count += 1
        elif settings.SexEnum.WOMAN == sex_num:
            woman_count += 1
        else:
            other_count += 1

    labels = settings.SEX_MAPPING.values()
    plt.pie([woman_count, man_count, other_count], labels=labels, autopct='%1.2f%%')
    plt.title("hello friend")

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
        friends = itchat.get_friends(request.args.get('update', False))
    except Exception as e:
        rsp_data = copy.copy(settings.ERROR['ERROR'])
        rsp_data['data'] = e
        return Response(json.dumps(rsp_data), mimetype='application/json')
    q = list()
    for friend in friends:
        q.append(friend["UserName"])
    gevent.joinall([gevent.spawn(tools.send_all_handler, username, msg) for username in friend_list])


if __name__ == '__main__':
    tools.clean_login_cache(settings.QR_PNG, settings.CHAT_PKL)
    login_thread = threading.Thread(target=itchat.auto_login,
                                    kwargs=(dict(hotReload=True, loginCallback=tools.loginCallback)))
    login_thread.start()
    sync = tools.sync_task()
    next(sync)
    app.run(host='127.0.0.1', port=8000, debug=False)
