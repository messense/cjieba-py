# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import sys
from os import path

from ._native import ffi, lib

__version__ = '0.1.0'

CURR_PATH = path.abspath(path.dirname(__file__))
PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
    int_types = (int, long)
    string_types = (str, unicode)
else:
    text_type = str
    int_types = (int,)
    string_types = (str,)


def to_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s


class Jieba(object):
    def __init__(self):
        self.__initialized = False
        self._jieba = None

    def initialize(self):
        if self.__initialized:
            return

        dict_dir = path.join(CURR_PATH, 'dict')
        dict_path = ffi.new('char []', to_bytes(path.join(dict_dir, 'jieba.dict.utf8')))
        hmm_path = ffi.new('char []', to_bytes(path.join(dict_dir, 'hmm_model.utf8')))
        user_dict_path = ffi.new('char []', to_bytes(path.join(dict_dir, 'user.dict.utf8')))
        idf_path = ffi.new('char []', to_bytes(path.join(dict_dir, 'idf.utf8')))
        stop_words_path = ffi.new('char []', to_bytes(path.join(dict_dir, 'stop_words.utf8')))
        self._jieba = lib.NewJieba(
            dict_path,
            hmm_path,
            user_dict_path,
            idf_path,
            stop_words_path
        )
        self.__initialized = True

    def __ptr_to_list(self, ptr):
        words = []
        if ptr == ffi.NULL:
            return words
        index = 0
        c_word = ptr[index]
        while c_word != ffi.NULL:
            words.append(ffi.string(c_word).decode('utf-8', 'replace'))
            index += 1
            c_word = ptr[index]
        return words

    def cut(self, text, cut_all=False, HMM=True):
        if cut_all:
            return self.cut_all(text)
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        is_hmm = 1 if HMM else 0
        ret = lib.Cut(self._jieba, sentence, is_hmm)
        ret = ffi.gc(ret, lib.FreeWords)
        words = self.__ptr_to_list(ret)
        return words

    def cut_all(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = lib.CutAll(self._jieba, sentence)
        ret = ffi.gc(ret, lib.FreeWords)
        words = self.__ptr_to_list(ret)
        return words

    def cut_for_search(self, text, HMM=True):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        is_hmm = 1 if HMM else 0
        ret = lib.CutForSearch(self._jieba, sentence, is_hmm)
        ret = ffi.gc(ret, lib.FreeWords)
        words = self.__ptr_to_list(ret)
        return words

    def tag(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = lib.Tag(self._jieba, sentence)
        ret = ffi.gc(ret, lib.FreeWords)
        words = self.__ptr_to_list(ret)
        return words

    def add_word(self, word):
        self.initialize()
        word = ffi.from_buffer(to_bytes(word))
        lib.AddWord(self._jieba, word)

    def __del__(self):
        if self._jieba is not None:
            lib.FreeJieba(self._jieba)

dt = Jieba()

initialize = dt.initialize
cut = dt.cut
cut_all = dt.cut_all
cut_for_search = dt.cut_for_search
tag = dt.tag
add_word = dt.add_word
