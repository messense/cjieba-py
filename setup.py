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
        cmd=[
            'c++',
            '-shared',
            '-std=c++11',
            '-fPIC',
            '-O3',
            '-I./cppjieba/deps/',
            '-I./cppjieba/include/',
            '-I./include/',
            '-o',
            lib,
            'lib/jieba.cc'
        ],
        path='./cjieba/cabi/'
    )

    spec.add_cffi_module(
        module_path='cjieba._native',
        dylib=lambda: build.find_dylib('jieba', in_path='.'),
        header_filename=lambda: build.find_header('jieba.h', in_path='include/'),
        rtld_flags=['NOW', 'NODELETE']
    )


setup(
    name='cjieba',
    version='0.4.1',
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/cjieba-py',
    description='Python cffi binding for cjieba',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    package_data={
        'cjieba': ['dict/*.utf8'],
    },
    zip_safe=False,
    platforms='any',
    setup_requires=['milksnake'],
    install_requires=['milksnake'],
    tests_require=['pytest', 'pytest-cov'],
    milksnake_tasks=[
        build_native
    ]
)
