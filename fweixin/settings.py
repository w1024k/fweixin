# coding:utf-8
# from celery import Celery
#
# app = Celery('tasks', backend='redis://:DhG7n&5q@localhost:6379/0', broker='redis://:DhG7n&5q@localhost:6379/0')
# app.conf.update(CELERY_ACCEPT_CONTENT=['json'], CELERYBEAT_SCHEDULE=dict())
#
# SOCK_ADDR = ('127.0.0.1', 13141)

# SEX_CHOICES = {
#     '0': '女',
#     '1': '男',
#     '2': '其他',
# }

SEX_CHOICES = ['女', '男', '其他']

ERROR = {
    'SUCC': {'code': '10000', 'msg': u'成功'},
    'ERROR': {'code': '10001', 'msg': u'未知错误'},
    'NOT_EXIST_USER': {'code': '10003', 'msg': u'未找到用户'},
}
