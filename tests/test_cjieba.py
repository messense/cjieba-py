# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import os
import sys

import pytest

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJ_DIR = os.path.dirname(CURR_DIR)
if PROJ_DIR not in sys.path:
    sys.path.insert(0, PROJ_DIR)

import cjieba


cjieba.initialize()


def test_cut():
    ret = cjieba.cut('')
    assert ret == []

    ret = cjieba.cut('南京市长江大桥')
    assert ret == ['南京市', '长江大桥']

    ret = cjieba.cut('南京市长江大桥', cut_all=True)
    assert ret == ['南京', '南京市', '京市', '市长', '长江', '长江大桥', '大桥']


def test_cut_all():
    ret = cjieba.cut_all('')
    assert ret == []

    ret = cjieba.cut_all('南京市长江大桥')
    assert ret == ['南京', '南京市', '京市', '市长', '长江', '长江大桥', '大桥']


def test_cut_for_search():
    ret = cjieba.cut_for_search('')
    assert ret == []

    ret = cjieba.cut_for_search('南京市长江大桥')
    assert ret == ['南京', '京市', '南京市', '长江', '大桥', '长江大桥']


def test_cut_hmm():
    ret = cjieba.cut_hmm('')
    assert ret == []

    ret = cjieba.cut_hmm('南京长江大桥')
    assert ret == ['南京长', '江大桥']


def test_cut_small():
    ret = cjieba.cut_small('', 2)
    assert ret == []

    ret = cjieba.cut_small('南京长江大桥', 2)
    assert ret == ['南京', '长江', '大桥']


def test_tag():
    ret = cjieba.tag('')
    assert ret == []

    ret = cjieba.tag('南京市长江大桥')
    assert len(ret) == 2
    assert ret[0] == ('南京市', 'ns')
    assert ret[1] == ('长江大桥', 'ns')


def test_tag_with_slash():
    ret = cjieba.tag('/ .')
    assert len(ret) == 3
    assert ret[0] == ('/', 'x')
    assert ret[1] == (' ', 'x')
    assert ret[2] == ('.', 'x')


def test_lookup_tag():
    flag = cjieba.lookup_tag('工作')
    assert flag == 'vn'


def test_tokenize():
    ret = cjieba.tokenize('')
    assert ret == []

    ret = cjieba.tokenize('南京市长江大桥')
    assert len(ret) == 2
    assert ret[0] == ('南京市', 0, 3)
    assert ret[1] == ('长江大桥', 3, 7)

    ret = cjieba.tokenize('南京南京')
    assert len(ret) == 2
    assert ret[0] == ('南京', 0, 2)
    assert ret[1] == ('南京', 2, 4)

    ret = cjieba.tokenize('南京市长江大桥', mode='search')
    assert len(ret) == 6
    assert ret[0] == ('南京', 0, 2)
    assert ret[1] == ('京市', 1, 3)
    assert ret[2] == ('南京市', 0, 3)
    assert ret[3] == ('长江', 3, 5)
    assert ret[4] == ('大桥', 5, 7)
    assert ret[5] == ('长江大桥', 3, 7)

    with pytest.raises(ValueError):
        cjieba.tokenize('南京市长江大桥', mode='foo')


def test_extract():
    ret = cjieba.extract('')
    assert ret == []

    ret = cjieba.extract('南京市长江大桥')
    assert ret == ['长江大桥', '南京市']

    ret = cjieba.extract('南京市长江大桥', top_k=1)
    assert ret == ['长江大桥']


def test_extract_with_weight():
    ret = cjieba.extract('', with_weight=True)
    assert ret == []

    ret = cjieba.extract('南京市长江大桥', with_weight=True)
    assert ret[0].word == '长江大桥'
    assert ret[0].weight > 11
    assert ret[1].word == '南京市'
    assert ret[1].weight > 8

    ret = cjieba.extract('南京市长江大桥', top_k=1, with_weight=True)
    assert ret[0].word == '长江大桥'
    assert ret[0].weight > 11


def test_add_user_word():
    cjieba.add_user_word('WTF')


def test_free_jieba():
    lib = cjieba.Jieba()
    lib.initialize()
    del lib
