# -*- coding: utf-8 -*-
# @Time    :   2021/01/14 17:27:07
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   run.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
import sys
from python_mmdt.mmdt.mmdt import MMDT
from python_mmdt.mmdt.feature import MMDTFeature


def mmdt_hash():
    mmdt = MMDT()
    r = mmdt.mmdt_hash(sys.argv[1])
    print(r)


def mmdt_compare():
    mmdt = MMDT()
    sim = 0.0
    sim = mmdt.mmdt_compare(sys.argv[1], sys.argv[2])
    print(sim)


def mmdt_classfiy():
    mmdt = MMDT()
    target = sys.argv[1]
    dlt = float(sys.argv[2])
    if os.path.isdir(target):
        files = os.listdir(target)
        for f in files:
            full_file = os.path.join(target, f)
            mmdt.classify(full_file, dlt)
    else:
        mmdt.classify(target, dlt)


def mmdt_gen_sets():
    mmdtf = MMDTFeature()
    print('start gen mmdt set.')
    mmdtf.gen_datas(sys.argv[1], sys.argv[2])
    print('end gen mmdt set.')


def mmdt_filter_sets():
    mmdtf = MMDTFeature()
    print('start gen mmdt set.')
    mmdtf.filter_mmdt_hash(sys.argv[1], float(sys.argv[2]))
    print('end gen mmdt set.')


def mmdt_filter_simple_sets():
    mmdtf = MMDTFeature()
    print('start gen mmdt set.')
    mmdtf.filter_mmdt_hash_simpleclassify(sys.argv[1])
    print('end gen mmdt set.')