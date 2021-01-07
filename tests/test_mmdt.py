# -*- coding: utf-8 -*-
# @Time    : 2021/01/06 23:27:28
# @Author  : ddvv
# @Site    : https://ddvvmmzz.github.io
# @File    : test_mmdt.py
# @Software: Visual Studio Code


import unittest
import os
from python_mmdt.mmdt.mmdt import MMDT


class Testmmdt(unittest.TestCase):

    def test_process(self):
        mmdt = MMDT()
        test_path = os.path.dirname(__file__)
        test_samples = os.path.join(test_path, "samples")
        files = os.listdir(test_samples)
        for f in files:
            file_path = os.path.join(test_samples, f)
            r1 = mmdt.mmdt_hash(file_path)
            print(r1)
            r2 = mmdt.mmdt_hash_streaming(file_path)
            print(r2)
            sim1 = mmdt.mmdt_compare(file_path, file_path)
            print(sim1)
            sim2 = mmdt.mmdt_compare_hash(r1, r2)
            print(sim2)
