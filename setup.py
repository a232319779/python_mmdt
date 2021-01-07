# -*- coding: utf-8 -*-
# @Time    : 2021/01/05 22:41:59
# @Author  : ddvv
# @Site    : https://ddvvmmzz.github.io
# @File    : setup.py
# @Software: Visual Studio Code


import platform
import glob
import os
import subprocess
import sys
import setuptools
from setuptools import Distribution as _Distribution, setup
import errno

try:
    from setuptools.command.build_clib import build_clib as _build_clib
except ImportError:
    # We ignore type checking because mypy shows an import error
    from distutils.command.build_clib import build_clib as _build_clib  # type: ignore

base_dir = os.path.dirname(__file__)
print('base dir is: %s' % base_dir)

SYSTEM_VER = platform.system().lower()

ENGINE_SUFFIX = {
    "windows": "dll",
    "darwin": "dylib",
    "linux": "so"
}

use_system_lib = False


class BuildClib(_build_clib):
    def build_libraries(self, libraries):
        raise Exception("build_libraries")

    def check_library_list(self, libraries):
        raise Exception("check_library_list")

    def get_source_files(self):
        files = glob.glob(os.path.relpath("python_mmdt/mmdt-lib/*"))
        return files

    def run(self):
        try:
            cmake_config = ''
            rm_cmd = 'rm'
            mv_cmd = 'mv'
            rm_param = '-fr'

            if SYSTEM_VER == 'windows':
                print("try to use Mingwin compile. ")
                cmake_config = '-G"Unix Makefiles"'
                rm_cmd = 'powershell.exe rm'
                mv_cmd = 'powershell.exe mv'
                rm_param = '-recurse'
            build_temp = os.path.abspath(self.build_temp)
            if os.path.exists(build_temp):
                cmds = list()
                cmds.extend(rm_cmd.split(' '))
                cmds.append(rm_param)
                cmds.append(build_temp)
                returncode = subprocess.call(cmds)
            print('temp build dir is: %s' % build_temp)
            os.makedirs(build_temp)

            returncode = subprocess.call(
                "(cd {build_temp} && cmake {cmake_config} ../lib/python_mmdt/mmdt-lib)".format(
                    build_temp=build_temp, cmake_config=cmake_config),
                shell=True
            )
            if returncode != 0:
                # try harder
                returncode = subprocess.call(
                    "(cd {build_temp} && cmake {cmake_config} ../lib/python_mmdt/mmdt-lib)".format(
                        build_temp=build_temp, cmake_config=cmake_config),
                    shell=True
                )
                if returncode != 0:
                    sys.exit("Failed to cmake the project build.")

            returncode = subprocess.call(
                ["make"],
                cwd=build_temp
            )

            if returncode != 0:
                sys.exit("Failed while building mmdt lib.")
            # mv libcore
            build_libcore = os.path.join(
                build_temp, "libcore.{}".format(ENGINE_SUFFIX[SYSTEM_VER]))
            install_libcore = os.path.join(
                build_temp, '..', 'lib', 'python_mmdt', 'mmdt')
            cmds = list()
            cmds.extend(mv_cmd.split(' '))
            cmds.append(build_libcore)
            cmds.append(install_libcore)
            returncode = subprocess.call(cmds)
            if returncode != 0:
                sys.exit("Failed while install mmdt lib.")

            # remove build
            cmds = list()
            cmds.extend(rm_cmd.split(' '))
            cmds.append(rm_param)
            cmds.append(build_temp)
            returncode = subprocess.call(cmds)
            if returncode != 0:
                sys.exit("Failed while remove mmdt build dir.")
            # remove mmdt-lib
            c_src_path = os.path.join(
                build_temp, '..', 'lib', 'python_mmdt', 'mmdt-lib')
            cmds = list()
            cmds.extend(rm_cmd.split(' '))
            cmds.append(rm_param)
            cmds.append(c_src_path)
            returncode = subprocess.call(cmds)
            if returncode != 0:
                sys.exit("Failed while remove c source build dir.")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


class Distribution(_Distribution):
    def has_c_libraries(self):
        return not use_system_lib


about = {}
with open(os.path.join(base_dir, "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md"), 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "mmdt-hash = python_mmdt.mmdt.mmdt:mmdt_hash",
            "mmdt-compare = python_mmdt.mmdt.mmdt:mmdt_compare",
        ]
    },
    python_requires='>=3.6',
    keywords="mmdt",
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    cmdclass={
        "build_clib": BuildClib,
    },
    distclass=Distribution,
)
