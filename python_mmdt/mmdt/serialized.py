# -*- coding: utf-8 -*-
# @Time    :   2021/01/14 17:38:19
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   serialized.py
# @Software:   Visual Studio Code
# @Desc    :   None


import zipfile
import _pickle as cPickle


def mmdt_save(name, datas):
    with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('data', cPickle.dumps(datas))


def mmdt_load(name):
    with zipfile.ZipFile(name, 'r') as zf:
        data = cPickle.loads(zf.open('data').read())
        return data