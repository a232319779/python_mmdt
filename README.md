# python_mmdt

python_mmdt is a python-based mmdt library implementation. This library allows you to use mmdt through python to calculate sensitive hashes.

mmdt is a sensitive hash implementation that can be used to calculate file similarity

## Pre-Install

* `cmake`: 2.6 and above
* `windows`: The current version (0.2.2) requires `minGW` to be installed on windows

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

A malicious scanner tool based on mmdt_hash. Version 0.2.1

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