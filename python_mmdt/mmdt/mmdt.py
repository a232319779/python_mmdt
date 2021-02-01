# -*- coding: utf-8 -*-
# @Time    :   2021/01/03 23:42:24
# @Author  :   ddvv
# @Site    :   https://www.cnblogs.com/ddvv
# @File    :   mmdt.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
import platform
import numpy as np
from ctypes import *
from python_mmdt.mmdt.common import mmdt_load,mmdt_std

SYSTEM_VER = platform.system().lower()

ENGINE_SUFFIX = {
    "windows": "dll",
    "darwin": "dylib",
    "linux": "so"
}

class MMDT_Data(Structure):
    _fields_ = [
        ("index_value", c_uint32),
        ("main_value1", c_uint32),
        ("main_value2", c_uint32),
        ("main_value3", c_uint32),
        ("main_value4", c_uint32),
    ]


class MMDT(object):
    def __init__(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        lib_core_path = os.path.join(cwd, "libcore.{}".format(ENGINE_SUFFIX[SYSTEM_VER]))
        mmdt_feature_file_name = os.path.join(cwd, "mmdt_feature.data")
        mmdt_feature_label_file_name = os.path.join(cwd, "mmdt_feature.label")
        self.datas = list()
        self.labels = list()
        self.build_datas = None
        self.build_labels = None

        if not os.path.exists(lib_core_path):
            raise Exception(lib_core_path)

        if os.path.exists(mmdt_feature_file_name):
            self.datas = mmdt_load(mmdt_feature_file_name)
        
        if os.path.exists(mmdt_feature_label_file_name):
            self.labels = mmdt_load(mmdt_feature_label_file_name)

        api = CDLL(lib_core_path)

        self.py_mmdt_hash = api.mmdt_hash
        self.py_mmdt_hash.argtypes = [c_char_p, POINTER(MMDT_Data)]
        self.py_mmdt_hash.restype = c_int

        self.py_mmdt_compare = api.mmdt_compare
        self.py_mmdt_compare.argtypes = [c_char_p, c_char_p]
        self.py_mmdt_compare.restype = c_double

        self.py_mmdt_hash_streaming = api.mmdt_hash_streaming
        self.py_mmdt_hash_streaming.argtypes = [c_char_p, c_uint32, POINTER(MMDT_Data)]
        self.py_mmdt_hash_streaming.restype = c_int

        self.py_mmdt_compare_hash = api.mmdt_compare_hash
        self.py_mmdt_compare_hash.argtypes = [MMDT_Data, MMDT_Data]
        self.py_mmdt_compare_hash.restype = c_double

    @staticmethod
    def __str_to_mmdt__(md_str):
        md = MMDT_Data()
        tmp = md_str.split(':')
        md.index_value = int(tmp[0], 16)
        md.main_value1 = int(tmp[1][:8], 16)
        md.main_value2 = int(tmp[1][8:16], 16)
        md.main_value3 = int(tmp[1][16:24], 16)
        md.main_value4 = int(tmp[1][24:32], 16)

        return md

    @staticmethod
    def __mmdt_to_str__(md):
        md_str = "%08X:%08X%08X%08X%08X" % (md.index_value, md.main_value1, md.main_value2, md.main_value3, md.main_value4)
        return md_str

    def mmdt_hash(self, filename):
        lp_filename = c_char_p(filename.encode())
        md = MMDT_Data()
        if not self.py_mmdt_hash(lp_filename, byref(md)):
            return self.__mmdt_to_str__(md)
        return None

    def mmdt_compare(self, filename1, filename2):
        lp_filename1 = c_char_p(filename1.encode())
        lp_filename2 = c_char_p(filename2.encode())
        sim = 0.0
        sim = self.py_mmdt_compare(lp_filename1, lp_filename2)
        return sim

    def mmdt_hash_streaming(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
        md = MMDT_Data()
        if not self.py_mmdt_hash_streaming(c_char_p(data), len(data), byref(md)):
            return self.__mmdt_to_str__(md)
        return None

    def mmdt_compare_hash(self, md1_str, md2_str):
        md1 = self.__str_to_mmdt__(md1_str)
        md2 = self.__str_to_mmdt__(md2_str)
        sim = 0.0
        sim = self.py_mmdt_compare_hash(md1, md2)
        return sim

    def build_features(self, classify_type=1):
        if classify_type == 1:
            self.build_datas = self.gen_simple_features()
        elif classify_type == 2:
            self.build_datas, self.build_labels = self.gen_knn_features()

    def gen_simple_features(self):
            datas = {}
            for data in self.datas:
                tmp = data.split(':')
                index_value = int(tmp[0], 16)
                if index_value not in datas.keys():
                    datas[index_value] = [('%s:%s' % (tmp[0], tmp[1]), int(tmp[2],10))]
                else:
                    datas[index_value].append(('%s:%s' % (tmp[0], tmp[1]), int(tmp[2],10)))
            return datas

    def simple_classify(self, md, dlt):
        datas = self.build_datas
        index_value = int(md.split(':')[0], 16)
        match_datas = datas.get(index_value, [])
        for match_data in match_datas:
            sim = self.mmdt_compare_hash(md, match_data[0])
            if sim > dlt:
                label_index = match_data[1]
                if self.labels:
                    label = self.labels[label_index]
                else:
                    label = 'match_%d' % label_index
                return sim, label
        return 0.0, 'unknown'

    def gen_knn_features(self):
        data_list = []
        label_list = []
        for data in self.datas:
            tmp = data.split(':')
            main_hash = tmp[1]
            main_values = []
            for i in range(0, len(main_hash), 2):
                main_values.append(int(main_hash[i:i+2], 16))
            data_list.append(main_values)
            label_list.append(int(tmp[2]))
        
        return data_list, label_list

    def knn_classify(self, md, dlt):
        def gen_knn_data(data):
            tmp = data.split(':')
            main_hash = tmp[1]
            main_values = []
            for i in range(0, len(main_hash), 2):
                main_values.append(int(main_hash[i:i+2], 16))

            return main_values
        
        datas = self.build_datas
        labels = self.build_labels
        
        train_datas = np.array(datas)
        t_data = gen_knn_data(md)
        rowSize = train_datas.shape[0]
        diff = np.tile(t_data, (rowSize, 1)) - train_datas
        sqr_diff = diff ** 2
        sqr_diff_sum = sqr_diff.sum(axis=1)
        distances = sqr_diff_sum ** 0.5
        sort_distance = distances.argsort()
        
        matched = sort_distance[0]

        label_index = labels[matched]
        sim = 1.0 - distances[matched]/1020.0
        if sim > dlt:
            if self.labels:
                label = self.labels[label_index]
            else:
                label = 'match_%d' % label_index
            return sim, label
        return 0.0, 'unknown'

    def classify(self, filename, dlt, classify_type=1):
        md = self.mmdt_hash(filename)
        if md:
            arr_std = mmdt_std(md)
            if classify_type == 1:
                sim, label = self.simple_classify(md, dlt)
            elif classify_type == 2:
                sim, label = self.knn_classify(md, dlt)
            else:
                sim = 0.0
                label = 'unknown'
            print('%s,%f,%s,%f' % (filename, sim, label, arr_std))
        else:
            print('%s mmdt_hash is None' % filename)
