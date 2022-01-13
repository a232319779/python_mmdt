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
from python_mmdt.mmdt.common import mmdt_load, mmdt_std

SYSTEM_VER = platform.system().lower()

ENGINE_SUFFIX = {"windows": "dll", "darwin": "dylib", "linux": "so"}


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
        lib_core_path = os.path.join(
            cwd, "libcore.{}".format(ENGINE_SUFFIX[SYSTEM_VER])
        )
        self.mmdt_feature_file_name = os.path.join(cwd, "mmdt_feature.data")
        self.simple_datas = dict()
        self.knn_train_datas = None
        self.knn_train_labels = list()
        self.knn_train_sha1s = list()

        if not os.path.exists(lib_core_path):
            raise Exception(lib_core_path)

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
        tmp = md_str.split(":")
        md.index_value = int(tmp[0], 16)
        md.main_value1 = int(tmp[1][:8], 16)
        md.main_value2 = int(tmp[1][8:16], 16)
        md.main_value3 = int(tmp[1][16:24], 16)
        md.main_value4 = int(tmp[1][24:32], 16)

        return md

    @staticmethod
    def __mmdt_to_str__(md):
        md_str = "%08X:%08X%08X%08X%08X" % (
            md.index_value,
            md.main_value1,
            md.main_value2,
            md.main_value3,
            md.main_value4,
        )
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
        with open(filename, "rb") as f:
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
            self.gen_simple_features()
        elif classify_type == 2:
            self.gen_knn_features()

    def gen_simple_features(self):
        if os.path.exists(self.mmdt_feature_file_name):
            datas = mmdt_load(self.mmdt_feature_file_name)
            for data in datas:
                tmp = data.split(":")
                index_value = int(tmp[0], 16)
                if index_value not in self.simple_datas.keys():
                    self.simple_datas[index_value] = [("%s:%s" % (tmp[0], tmp[1]), tmp[2], tmp[3])]
                else:
                    self.simple_datas[index_value].append(("%s:%s" % (tmp[0], tmp[1]), tmp[2], tmp[3]))
        else:
            print('缺少特征文件')
            exit(0)

    def simple_classify(self, md, dlt):
        index_value = int(md.split(":")[0], 16)
        match_datas = self.simple_datas.get(index_value, [])
        for match_data in match_datas:
            sim = self.mmdt_compare_hash(md, match_data[0])
            if sim > dlt:
                sim_label = match_data[1]
                sim_sha1 = match_data[2]
                return sim, sim_label, sim_sha1
        return 0.0, "unknown", "unknown"

    def simple_classify_2(self, md, dlt, number=10):
        """
        return data:
            {
            "label": "xxx",
            "labels": [
                {
                    "label": "xxx",
                    "ratio": xx.xx%,
                }
            ],
            "similars": [
                {
                    "hash": "xxxxx",
                    "label": "xxx",
                    "sim": 0.1
                }
            ]
        }
        """
        index_value = int(md.split(":")[0], 16)
        match_datas = self.simple_datas.get(index_value, [])
        max_sim = 0.0
        max_label = 'unknown'
        return_data = {'label': max_label, 'labels': list(), 'similars': list()}
        labels = {}
        for match_data in match_datas:
            sim = self.mmdt_compare_hash(md, match_data[0])
            if sim > dlt:
                if match_data[1] not in labels.keys():
                    labels[match_data[1]] = 1
                else:
                    labels[match_data[1]] += 1
                similar = {'hash': match_data[2], 'label': match_data[1], 'sim': sim}
                return_data['similars'].append(similar)
                if sim > max_sim:
                    max_label = match_data[1]
                    max_sim = sim
            if len(return_data['similars']) > number:
                break
        sum_count = sum(labels.values())
        for label, count in labels.items():
            l = {'label': label, 'ratio': '%.2f%%' % float(count/sum_count*100)}
            return_data['labels'].append(l)
        return_data['label'] = max_label
        return return_data

    def gen_knn_features(self):
        if os.path.exists(self.mmdt_feature_file_name):
            data_list = list()
            datas = mmdt_load(self.mmdt_feature_file_name)
            for data in datas:
                tmp = data.split(":")
                main_hash = tmp[1]
                main_values = []
                for i in range(0, len(main_hash), 2):
                    main_values.append(int(main_hash[i : i + 2], 16))
                data_list.append(main_values)
                self.knn_train_labels.append(tmp[2])
                self.knn_train_sha1s.append(tmp[3])

            self.knn_train_datas = np.array(data_list)
        else:
            print('缺少特征文件')
            exit(0)

    def knn_classify(self, md, dlt):
        def gen_knn_data(data):
            tmp = data.split(":")
            main_hash = tmp[1]
            main_values = []
            for i in range(0, len(main_hash), 2):
                main_values.append(int(main_hash[i : i + 2], 16))

            return main_values

        t_data = gen_knn_data(md)
        rowSize = self.knn_train_datas.shape[0]
        diff = np.tile(t_data, (rowSize, 1)) - self.knn_train_datas
        sqr_diff = diff ** 2
        sqr_diff_sum = sqr_diff.sum(axis=1)
        distances = sqr_diff_sum ** 0.5
        sort_distance = distances.argsort()

        matched = sort_distance[0]

        sim_label = self.knn_train_labels[matched]
        sim_sha1 = self.knn_train_sha1s[matched]
        sim = 1.0 - distances[matched] / 1020.0
        if sim > dlt:
            return sim, sim_label, sim_sha1
        return 0.0, "unknown", "unknown"

    def knn_classify_2(self, md, dlt, number=10):
        def gen_knn_data(data):
            tmp = data.split(":")
            main_hash = tmp[1]
            main_values = []
            for i in range(0, len(main_hash), 2):
                main_values.append(int(main_hash[i : i + 2], 16))

            return main_values

        t_data = gen_knn_data(md)
        rowSize = self.knn_train_datas.shape[0]
        diff = np.tile(t_data, (rowSize, 1)) - self.knn_train_datas
        sqr_diff = diff ** 2
        sqr_diff_sum = sqr_diff.sum(axis=1)
        distances = sqr_diff_sum ** 0.5
        sort_distance = distances.argsort()

        return_data = {'label': 'unknown', 'labels': list(), 'similars': list()}
        sim_labels = {}
        for matched in sort_distance:
            sim = 1.0 - distances[matched] / 1020.0
            if sim > dlt:
                sim_label = self.knn_train_labels[matched]
                if sim_label not in sim_labels.keys():
                        sim_labels[sim_label] = 1
                else:
                    sim_labels[sim_label] += 1
                sim_sha1 = self.knn_train_sha1s[matched]
                similar = {'hash': sim_sha1, 'label': sim_label, 'sim': sim}
                return_data['similars'].append(similar)
            
                if len(return_data['similars']) >= number:
                    break
                continue
            break
        sum_count = sum(sim_labels.values())
        for label, count in sim_labels.items():
            l = {'label': label, 'ratio': '%.2f%%' % float(count/sum_count*100)}
            return_data['labels'].append(l)
        return_data['label'] = self.knn_train_labels[sort_distance[0]]
        return return_data

    def classify(self, filename, dlt, classify_type=1):
        md = self.mmdt_hash(filename)
        if md:
            arr_std = mmdt_std(md)
            if classify_type == 1:
                data = self.simple_classify_2(md, dlt)
            elif classify_type == 2:
                data = self.knn_classify_2(md, dlt)
            else:
                data = {
                "label": "unknown",
                "labels": [
                    {
                        "label": "unknown",
                        "ratio": "100.00%",
                    }
                ],
                "similars": []
                }
            print(data)
        else:
            print("%s mmdt_hash is None" % filename)

