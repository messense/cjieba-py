# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import sys
from os import path
from collections import namedtuple

from ._native import ffi, lib

__version__ = '0.2.1'

CURR_PATH = path.abspath(path.dirname(__file__))
PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
else:
    text_type = str


def to_bytes(s):
    if isinstance(s, text_type):
        return s.encode('utf-8')
    return s


Tag = namedtuple('Tag', ['word', 'flag'])


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
        c_words = ffi.unpack(ptr.words, ptr.len)
        words = [ffi.string(s).decode('utf-8', 'replace') for s in c_words]
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
        ret = ffi.gc(ret, lib.FreeCJiebaWords)
        words = self.__ptr_to_list(ret)
        return words

    def cut_all(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = lib.CutAll(self._jieba, sentence)
        ret = ffi.gc(ret, lib.FreeCJiebaWords)
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
        ret = ffi.gc(ret, lib.FreeCJiebaWords)
        words = self.__ptr_to_list(ret)
        return words

    def tag(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = lib.Tag(self._jieba, sentence)
        ret = ffi.gc(ret, lib.FreeCJiebaWords)
        words = self.__ptr_to_list(ret)
        tags = []
        for item in words:
            word, flag  = item.split('/', 1)
            tags.append(Tag(word, flag))
        return tags

    def add_word(self, word):
        self.initialize()
        word = ffi.from_buffer(to_bytes(word))
        lib.AddWord(self._jieba, word)

    def tokenize(self, text, mode='default', HMM=True):
        if mode == 'default':
            c_mode = lib.DefaultMode
        elif mode == 'search':
            c_mode = lib.SearchMode
        else:
            raise ValueError('Invalid tokenize mode, only default and search are supported')
        if not text:
            return []
        self.initialize()

        text_bytes = to_bytes(text)
        sentence = ffi.from_buffer(text_bytes)
        is_hmm = 1 if HMM else 0
        ret = lib.Tokenize(self._jieba, sentence, c_mode, is_hmm)
        ret = ffi.gc(ret, lib.FreeToken)

        char_indices = {}
        bytes_offset = 0
        for char_index, char in enumerate(text):
            length = len(char.encode('utf-8'))
            char_indices[bytes_offset] = char_index
            bytes_offset += length

        tokens = []
        index = 0
        c_token = ffi.addressof(ret, index)
        while c_token and c_token.len > 0:
            word = text_bytes[c_token.offset:c_token.offset + c_token.len].decode('utf-8')
            start = char_indices[c_token.offset]
            end = start + len(word)
            tokens.append((word, start, end))
            index += 1
            c_token = ffi.addressof(ret, index)
        return tokens

    def __del__(self):
        if self._jieba is not None:
            lib.FreeJieba(self._jieba)

dt = Jieba()

initialize = dt.initialize
cut = dt.cut
lcut = cut
cut_all = dt.cut_all
cut_for_search = dt.cut_for_search
lcut_for_search = cut_for_search
tag = dt.tag
add_word = dt.add_word
tokenize = dt.tokenize
