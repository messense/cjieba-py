extern "C" {
    #include "jieba.h"
}

#include "cppjieba/Jieba.hpp"
#include "cppjieba/KeywordExtractor.hpp"

using namespace std;

static CJiebaWord* ConvertWords(const std::vector<string>& words) {
    CJiebaWord* res = (CJiebaWord*)malloc(sizeof(CJiebaWord) * (words.size() + 1));
    for (size_t i = 0; i < words.size(); i++) {
        res[i].word = (char *) malloc(words[i].size());
        strncpy(res[i].word, words[i].data(), words[i].size());
        res[i].len = words[i].size();
    }
    res[words.size()].word = NULL;
    res[words.size()].len = 0;
    return res;
}

static struct CWordWeight* ConvertWords(const std::vector<std::pair<std::string, double> >& words) {
  struct CWordWeight* res = (struct CWordWeight*)malloc(sizeof(struct CWordWeight) * (words.size() + 1));
  for (size_t i = 0; i < words.size(); i++) {
    res[i].word = (char*)malloc(sizeof(char) * (words[i].first.length() + 1));
    strcpy(res[i].word, words[i].first.c_str());
    res[i].weight = words[i].second;
  }
  res[words.size()].word = NULL;
  return res;
}

extern "C" {

Jieba NewJieba(const char* dict_path, const char* hmm_path, const char* user_dict, const char* idf_path, const char* stop_words_path) {
  Jieba handle = (Jieba)(new cppjieba::Jieba(dict_path, hmm_path, user_dict, idf_path, stop_words_path));
  return handle;
}

void FreeJieba(Jieba handle) {
  cppjieba::Jieba* x = (cppjieba::Jieba*)handle;
  delete x;
}

void FreeWords(CJiebaWord* words) {
  CJiebaWord* x = words;
  while (x && x->word) {
    free(x->word);
    x->word = NULL;
    x++;
  }
  free(words);
}

CJiebaWord* Cut(Jieba x, const char* sentence, int is_hmm_used) {
  std::vector<std::string> words;
  ((cppjieba::Jieba*)x)->Cut(sentence, words, is_hmm_used);
  return ConvertWords(words);
}

CJiebaWord* CutAll(Jieba x, const char* sentence) {
  std::vector<std::string> words;
  ((cppjieba::Jieba*)x)->CutAll(sentence, words);
  return ConvertWords(words);
}

CJiebaWord* CutForSearch(Jieba x, const char* sentence, int is_hmm_used) {
  std::vector<std::string> words;
  ((cppjieba::Jieba*)x)->CutForSearch(sentence, words, is_hmm_used);
  return ConvertWords(words);
}

CJiebaWord* Tag(Jieba x, const char* sentence) {
  std::vector<std::pair<std::string, std::string> > result;
  ((cppjieba::Jieba*)x)->Tag(sentence, result);
  std::vector<std::string> words;
  words.reserve(result.size());
  for (size_t i = 0; i < result.size(); ++i) {
    words.push_back(result[i].first + "/" + result[i].second);
  }
  return ConvertWords(words);
}

void AddWord(Jieba x, const char* word) {
  ((cppjieba::Jieba*)x)->InsertUserWord(word);
}

struct CWordWeight* ExtractWithWeight(Jieba handle, const char* sentence, int top_k) {
  std::vector<std::pair<std::string, double> > words;
  ((cppjieba::Jieba*)handle)->extractor.Extract(sentence, words, top_k);
  struct CWordWeight* res = ConvertWords(words);
  return res;
}

CJiebaWord* Extract(Jieba handle, const char* sentence, int top_k) {
  std::vector<std::string> words;
  ((cppjieba::Jieba*)handle)->extractor.Extract(sentence, words, top_k);
  return ConvertWords(words);
}

void FreeWordWeights(struct CWordWeight* wws) {
  struct CWordWeight* x = wws;
  while (x && x->word) {
    free(x->word);
    x->word = NULL;
    x++;
  }
  free(wws);
}

} // extern "C"
