# python_mmdt

python_mmdt is a python-based mmdt library implementation. This library allows you to use mmdt through python to calculate sensitive hashes.

mmdt is a sensitive hash implementation that can be used to calculate file similarity

## Pre-Install

* `cmake`: 2.6 and above
* `windows`: The current version (0.3.1) requires `minGW` to be installed on windows

## Install from Pypi

```
$ pip install python_mmdt
```

## Install by Whl

`.whl` download from [`Release`](https://github.com/a232319779/python_mmdt/releases)

```
$ pip install python_mmdt-xxx.whl
```

## Usage

### Command Line

```sh
# calculate mmdt sensitive
➜ mmdt-hash $file_path

# calculate file similarity
➜ mmdt-compare $file_path1 $file_path2

# use classifier to detected malicious file
➜ mmdt-classify -h
usage: python_mmdt malicious file scan tool [-h] [-s SCANS] [-t THRESHOLD]
                                            [-c CLASSIFY_TYPE]

A malicious scanner tool based on mmdt_hash. Version 0.3.1

optional arguments:
  -h, --help            show this help message and exit
  -s SCANS, --scans SCANS
                        set file/path to scan.
  -t THRESHOLD, --threshold THRESHOLD
                        set threshold value to determine whether the file is a
                        malicious file. (default 0.95)
  -c CLASSIFY_TYPE, --classify CLASSIFY_TYPE
                        set classify type.set 1 for simple classify, set 2 for
                        knn classify.(default 1)

Use like:
    1. use simple classify
    mmdt-classify -s $sample_path -t 0.95 -c 1
    2. use knn classify
    mmdt-classify -s $sample_path -t 0.95 -c 2

# submit mmdt_hash
➜ mmdt-scan-online .\test\2f04b8eb993ca4a3d98607824a10acfb
{
    "sha1": "a5ad744088e2739dc8b6a0622432106158d0abd8",
    "md5": "2f04b8eb993ca4a3d98607824a10acfb",
    "file_name": ".\\test\\2f04b8eb993ca4a3d98607824a10acfb",
    "message": "查询任务已添加至查询队列，当前队列中还有0个任务",
    "status": 20001,
    "data": {}
}

# get check result
➜ mmdt-scan-online .\test\2f04b8eb993ca4a3d98607824a10acfb
{
    "sha1": "a5ad744088e2739dc8b6a0622432106158d0abd8",
    "md5": "2f04b8eb993ca4a3d98607824a10acfb",
    "file_name": ".\\test\\2f04b8eb993ca4a3d98607824a10acfb",
    "message": "success",
    "status": 20000,
    "data": {
        "label": "APT28",
        "labels": [
            {
                "label": "APT28",
                "ratio": "20.00%"
            },
            {
                "label": "virlock",
                "ratio": "50.00%"
            },
            {
                "label": "coinminer",
                "ratio": "30.00%"
            }
        ],
        "similars": [
            {
                "hash": "a5ad744088e2739dc8b6a0622432106158d0abd8",
                "label": "APT28",
                "sim": 1.0
            },
            {
                "hash": "9001f4cfe62367a282efc08b072a13a5e2e403db",
                "label": "APT28",
                "sim": 0.9896245046624919
            },
            {
                "hash": "0d3d452a7e8d7d328bfe9862cbcee33ad1ce4cf4",
                "label": "virlock",
                "sim": 0.8511449567066024
            },
            ...
    }
}
```

### python code

```python
# -*- coding: utf-8 -*-

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
```

## Screenshot

### calculate file similarity
![](./pictures/python-mmdt.jpg)

### use classifier to detected malicious file
![](./pictures/scan.png)

### scan online
![](./pictures/submit.jpg)
![](./pictures/scan_online.jpg)