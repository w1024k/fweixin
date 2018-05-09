# coding:utf-8
import os


class SexEnum:
    WOMAN = 0
    MAN = 1
    OTHER = 2


SEX_MAPPING = dict((
    (SexEnum.WOMAN, 'woman'),
    (SexEnum.MAN, 'MAN'),
    (SexEnum.OTHER, 'OTHER')
))

ERROR = {
    'SUCC': {'code': '10000', 'msg': u'成功'},
    'ERROR': {'code': '10001', 'msg': u'未知错误'},
    'NOT_EXIST_USER': {'code': '10003', 'msg': u'未找到用户'},
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

QR_PNG = 'QR.png'
CHAT_PKL = 'itchat.pkl'

