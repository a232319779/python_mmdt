# -*- coding: utf-8 -*-
# @Time    :   2021/01/14 11:11:36
# @Author  :   ddvv
# @Site    :   https://ddvvmmzz.github.io
# @File    :   feature.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
from python_mmdt.mmdt.mmdt import MMDT
from python_mmdt.mmdt.common import mmdt_save, mmdt_load, mmdt_std


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
        arr_std = mmdt_std(md)
        if arr_std > self.mmdt_feature_dlt:
            return True
        return False

    @staticmethod
    def filter_mmdt_hash(name, dlt):
        datas = mmdt_load(name)
        print('old len: %d' % len(datas))
        new_datas = list()
        for data in datas:
            arr_std = mmdt_std(data)
            if arr_std > dlt:
                new_datas.append(data)
            else:
                print('remove: %s' % (data))
        new_datas = list(set(new_datas))
        print('new len: %d' % len(new_datas))
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
