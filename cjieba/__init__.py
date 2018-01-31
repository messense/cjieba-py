# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import sys
from os import path
from collections import namedtuple

from ._native import ffi, lib

__version__ = '0.4.1'

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
WordWeight = namedtuple('WordWeight', ['word', 'weight'])


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
        self._jieba = lib.jieba_new(
            dict_path,
            hmm_path,
            user_dict_path,
            idf_path,
            stop_words_path
        )
        self.__initialized = True

    def __ptr_to_list(self, ptr):
        c_words = ffi.unpack(ptr.words, ptr.length)
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
        ret = None
        try:
            ret = lib.jieba_cut(self._jieba, sentence, is_hmm)
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        return words

    def cut_all(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = None
        try:
            ret = lib.jieba_cut_all(self._jieba, sentence)
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        return words

    def cut_for_search(self, text, HMM=True):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        is_hmm = 1 if HMM else 0
        ret = None
        try:
            ret = lib.jieba_cut_for_search(self._jieba, sentence, is_hmm)
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        return words

    def cut_hmm(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = None
        try:
            ret = lib.jieba_cut_hmm(self._jieba, sentence)
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        return words

    def cut_small(self, text, max_word_len):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = None
        try:
            ret = lib.jieba_cut_small(self._jieba, sentence, int(max_word_len))
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        return words

    def tag(self, text):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = None
        try:
            ret = lib.jieba_tag(self._jieba, sentence)
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        tags = []
        for item in words:
            word, flag  = item.split('/', 1)
            tags.append(Tag(word, flag))
        return tags

    def lookup_tag(self, word):
        self.initialize()

        word = ffi.from_buffer(to_bytes(word))
        ret = None
        try:
            ret = lib.jieba_lookup_tag(self._jieba, word)
            return ffi.string(ret).decode('utf-8')
        finally:
            if ret is not None:
                lib.jieba_str_free(ret)

    def add_user_word(self, word):
        self.initialize()
        word = ffi.from_buffer(to_bytes(word))
        lib.jieba_add_user_word(self._jieba, word)

    def tokenize(self, text, mode='default', HMM=True):
        if mode == 'default':
            c_mode = lib.JIEBA_TOKENIZE_MODE_DEFAULT
        elif mode == 'search':
            c_mode = lib.JIEBA_TOKENIZE_MODE_SEARCH
        else:
            raise ValueError('Invalid tokenize mode, only default and search are supported')
        if not text:
            return []
        self.initialize()

        text_bytes = to_bytes(text)
        sentence = ffi.from_buffer(text_bytes)
        is_hmm = 1 if HMM else 0
        tokens = []
        ret = None
        try:
            ret = lib.jieba_tokenize(self._jieba, sentence, c_mode, is_hmm)
            index = 0
            c_token = ffi.addressof(ret, index)
            while c_token and c_token.length > 0:
                start = c_token.unicode_offset
                end = start + c_token.unicode_length
                word = text[start:end]
                tokens.append((word, start, end))
                index += 1
                c_token = ffi.addressof(ret, index)
        finally:
            if ret is not None:
                lib.jieba_token_free(ret)
        return tokens

    def extract(self, text, top_k=20, with_weight=False):
        if with_weight:
            return self._extract_with_weight(text, top_k)
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        ret = None
        try:
            ret = lib.jieba_extract(self._jieba, sentence, int(top_k))
            words = self.__ptr_to_list(ret)
        finally:
            if ret is not None:
                lib.jieba_words_free(ret)
        return words

    def _extract_with_weight(self, text, top_k=20):
        if not text:
            return []
        self.initialize()

        text = to_bytes(text)
        sentence = ffi.from_buffer(text)
        words = []
        ret = None
        try:
            ret = lib.jieba_extract_with_weight(self._jieba, sentence, int(top_k))
            index = 0
            c_word = ffi.addressof(ret, index)
            while c_word and c_word.word != ffi.NULL:
                words.append(WordWeight(
                    ffi.string(c_word.word).decode('utf-8'),
                    c_word.weight
                ))
                index += 1
                c_word = ffi.addressof(ret, index)
        finally:
            if ret is not None:
                lib.jieba_word_weight_free(ret)
        return words

    def __del__(self):
        if self._jieba is not None:
            lib.jieba_free(self._jieba)

dt = Jieba()

initialize = dt.initialize
cut = dt.cut
lcut = cut
cut_all = dt.cut_all
cut_for_search = dt.cut_for_search
cut_hmm = dt.cut_hmm
cut_small = dt.cut_small
lcut_for_search = cut_for_search
tag = dt.tag
lookup_tag = dt.lookup_tag
add_user_word = dt.add_user_word
tokenize = dt.tokenize
extract = dt.extract
