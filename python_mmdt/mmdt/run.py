# -*- coding: utf-8 -*-
# @Time    :   2021/01/14 17:27:07
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   run.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
import sys
import shutil
from python_mmdt.mmdt.common import mmdt_std as __mmdt_std__
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
    dlt = 0.9
    classify_type = 1
    target = sys.argv[1]
    if len(sys.argv) > 2:
        dlt = float(sys.argv[2])
    if len(sys.argv) > 3:
        classify_type = int(sys.argv[3])
    if os.path.isdir(target):
        files = os.listdir(target)
        for f in files:
            full_file = os.path.join(target, f)
            mmdt.classify(full_file, dlt, classify_type)
    else:
        mmdt.classify(target, dlt, classify_type)


def mmdt_gen_sets():
    mmdtf = MMDTFeature()
    print('start gen mmdt set.')
    mmdtf.gen_datas(sys.argv[1], sys.argv[2])
    print('end gen mmdt set.')


def mmdt_filter_sets():
    mmdtf = MMDTFeature()
    print('start filter mmdt set.')
    mmdtf.filter_mmdt_hash(sys.argv[1], float(sys.argv[2]))
    print('end filter mmdt set.')


def mmdt_filter_simple_sets():
    mmdtf = MMDTFeature()
    print('start simple filter mmdt set.')
    mmdtf.filter_mmdt_hash_simpleclassify(sys.argv[1])
    print('end simple filter mmdt set.')

def mmdt_std():
    calc_std = __mmdt_std__(sys.argv[1])
    print('standard deviation: %f' % calc_std)

def mmdt_copy_data():
    cwd = os.path.abspath(os.path.dirname(__file__))
    source_file_path = sys.argv[1]
    source_file_basename = os.path.basename(source_file_path)
    target_file = os.path.join(cwd, source_file_basename)
    try:
        shutil.copy(source_file_path, target_file)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except Exception as e:
        print("Unexpected error: " % str(e))
