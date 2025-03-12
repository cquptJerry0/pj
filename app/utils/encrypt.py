import hashlib
from django.conf import settings


def md5(data_string):

    # salt = 'XXXXXXXXXXXXXX'    # 加严
    # obj = hashlib.md5(salt.encode('utf-8'))   #  md5 加严加密

    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))

    return obj.hexdigest()