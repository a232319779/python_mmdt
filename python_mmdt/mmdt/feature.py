# -*- coding: utf-8 -*-
# @Time    :   2021/01/14 11:11:36
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   feature.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
import numpy as np
from python_mmdt.mmdt.mmdt import MMDT
from python_mmdt.mmdt.serialized import mmdt_save, mmdt_load


class MMDTFeature(object):
    def __init__(self, dlt=10.0):
        self.mmdt_feature_file_name = 'mmdt_feature.data'
        self.mmdt_feature_label_file_name = 'mmdt_feature.label'
        self.mmdt_feature_dlt = dlt
        self.mmdt_feature_labels = list()
        self.mmdt = MMDT()

    @staticmethod
    def read_lables(file_name):
        with open(file_name, 'r') as target:
            lines = target.readlines()

        labels = dict()
        for line in lines:
            line = line.strip()
            tmp = line.split(',')
            if tmp:
                labels[tmp[0]] = tmp[1]
        
        return labels

    @staticmethod
    def list_dir(root_dir):
        files = os.listdir(root_dir)
        for f in files:
            file_path = os.path.join(root_dir, f)
            yield file_path, f

    def check_mmdt_hash(self, md):
        tmp = md.split(':')
        main_hash = tmp[1]
        main_values = []
        for i in range(0, len(main_hash), 2):
            main_values.append(int(main_hash[i:i+2], 16))
        #求标准差
        arr_std = np.std(main_values[4:12], ddof=1)
        if arr_std > self.mmdt_feature_dlt:
            return True
        return False

    @staticmethod
    def filter_mmdt_hash(name, dlt):
        datas = mmdt_load(name)
        new_datas = list()
        for data in datas:
            tmp = data.split(':')
            main_hash = tmp[1]
            main_values = []
            for i in range(0, len(main_hash), 2):
                main_values.append(int(main_hash[i:i+2], 16))
            #求标准差
            arr_std = np.std(main_values[4:12], ddof=1)
            if arr_std > dlt:
                new_datas.append(data)
            else:
                print('remove: %s' % (data))

        mmdt_save(name, new_datas)

    @staticmethod
    def filter_mmdt_hash_simpleclassify(name):
        datas = mmdt_load(name)
        print('old len: %d' % len(datas))
        datas = list(set(datas))
        print('new len: %d' % len(datas))
        mmdt_save(name, datas)

    def gen_datas(self, samples_path, samples_label_file):
        labels = self.read_lables(samples_label_file)
        count = 0
        datas = list()
        for full_path, file_name in self.list_dir(samples_path):
            count += 1
            print('process: %s, %d' % (file_name, count))
            mmdt_hash = self.mmdt.mmdt_hash(full_path)
            if self.check_mmdt_hash(mmdt_hash):
                label = labels.get(file_name)
                if label not in self.mmdt_feature_labels:
                    self.mmdt_feature_labels.append(label)
                label_indx = self.mmdt_feature_labels.index(label)
                data = '%s:%d' % (mmdt_hash, label_indx)
                datas.append(data)
        
        mmdt_save(self.mmdt_feature_file_name, datas)
        mmdt_save(self.mmdt_feature_label_file_name, self.mmdt_feature_labels)
