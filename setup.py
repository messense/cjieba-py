# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages


def build_native(spec):
    name = 'jieba'
    if sys.platform == 'darwin':
        lib = 'lib%s.dylib' % name
    elif sys.platform == 'win32':
        lib = '%s.dll' % name
    else:
        lib = 'lib%s.so' % name
    build = spec.add_external_build(
        cmd=['c++', '-shared', '-I./cjieba/deps/', '-fPIC', '-O3', '-o', lib, 'cjieba/lib/jieba.cpp'],
        path='.'
    )

    spec.add_cffi_module(
        module_path='cjieba._native',
        dylib=lambda: build.find_dylib('jieba', in_path='.'),
        header_filename=lambda: build.find_header('jieba.h', in_path='cjieba/lib/'),
        rtld_flags=['NOW', 'NODELETE']
    )


setup(
    name='cjieba',
    version='0.1.0',
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/cjieba-py',
    description='Python cffi binding for cjieba',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cjieba': ['dict/*.utf8'],
    },
    zip_safe=False,
    platforms='any',
    setup_requires=['milksnake'],
    install_requires=['milksnake'],
    milksnake_tasks=[
        build_native
    ]
)
