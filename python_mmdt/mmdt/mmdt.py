# -*- coding: utf-8 -*-
# @Time    :   2021/01/03 23:42:24
# @Author  :   ddvv
# @Site    :   https://www.cnblogs.com/ddvv
# @File    :   mmdt.py
# @Software:   Visual Studio Code
# @Desc    :   None


import os
import sys
import platform
from ctypes import *


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


def mmdt_hash():
    mmdt = MMDT()
    r = mmdt.mmdt_hash(sys.argv[1])
    print(r)


def mmdt_compare():
    mmdt = MMDT()
    sim = 0.0
    sim = mmdt.mmdt_compare(sys.argv[1], sys.argv[2])
    print(sim)
