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
import argparse
import requests
from python_mmdt.mmdt.common import mmdt_load, mmdt_save, gen_md5, gen_sha1, mmdt_std as __mmdt_std__
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
    try:
        epilog = r"""
Use like:
    1. use simple classify
    mmdt-classify -s $sample_path -t 0.95 -c 1
    2. use knn classify
    mmdt-classify -s $sample_path -t 0.95 -c 2
        """
        parser = argparse.ArgumentParser(prog='python_mmdt malicious file scan tool',
                                        description='A malicious scanner tool based on mmdt_hash. Version 0.2.2',
                                        epilog=epilog,
                                        formatter_class=argparse.RawDescriptionHelpFormatter
                                        )
        parser.add_argument('-s', '--scans', help='set file/path to scan.',
                            type=str, dest='scans', action='store')
        parser.add_argument('-t', '--threshold', help='set threshold value to determine whether the file is a malicious file. (default 0.95)',
                            type=float, dest='threshold', action='store', default=0.95)
        parser.add_argument('-c', '--classify', help='set classify type.set 1 for simple classify, set 2 for knn classify.(default 1)',
                            type=int, dest='classify_type', action='store', default=1)

        args = parser.parse_args()
    except Exception as e:
        print('error: %s' % str(e))
        exit(0)

    mmdt = MMDT()
    threshold = args.threshold
    classify_type = args.classify_type
    target = args.scans
    mmdt.build_features(classify_type)
    if os.path.isdir(target):
        files = os.listdir(target)
        for f in files:
            full_file = os.path.join(target, f)
            mmdt.classify(full_file, threshold, classify_type)
    else:
        mmdt.classify(target, threshold, classify_type)


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
    target_file = os.path.join(cwd, 'mmdt_feature.data')
    try:
        shutil.copy(source_file_path, target_file)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except Exception as e:
        print("Unexpected error: " % str(e))

def mmdt_scan_online():
    mmdt = MMDT()
    file_name = sys.argv[1]
    file_md5 = gen_md5(file_name)
    file_sha1 = gen_sha1(file_name)
    file_mmdt = mmdt.mmdt_hash(file_name)
    data = {
        "md5": file_md5,
        "sha1": file_sha1,
        "file_name": file_name,
        "mmdt": file_mmdt,
        "data": {}
    }
    r = requests.post(url='http://mmdt.me/mmdt/scan', json=data)
    print(r.text)

def mmdt_feature_merge():
    """
    实现特征合并
    """
    file_name1 = sys.argv[1]
    file_name2 = sys.argv[2]
    data1 = mmdt_load(file_name1)
    data2 = mmdt_load(file_name2)
    data1.extend(data2)
    mmdt_save(file_name1, data1)
