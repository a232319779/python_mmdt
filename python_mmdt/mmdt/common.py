# -*- coding: utf-8 -*-
# @Time    :   2021/01/14 17:38:19
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   serialized.py
# @Software:   Visual Studio Code
# @Desc    :   None


import zipfile
import numpy as np
import _pickle as cPickle


def mmdt_save(name, datas):
    with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('data', cPickle.dumps(datas))


def mmdt_load(name):
    with zipfile.ZipFile(name, 'r') as zf:
        data = cPickle.loads(zf.open('data').read())
        return data


def mmdt_std(md):
    tmp = md.split(':')
    main_hash = tmp[1]
    main_values = []
    for i in range(0, len(main_hash), 2):
        main_values.append(int(main_hash[i:i+2], 16))
    std_main_values = main_values[2:14]
    std_main_values.pop(std_main_values.index(max(std_main_values)))
    std_main_values.pop(std_main_values.index(min(std_main_values)))
    #求标准差
    arr_std = np.std(std_main_values, ddof=1)
    return arr_std