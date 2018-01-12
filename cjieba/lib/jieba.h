#ifndef CJIEBA_C_API_H
#define CJIEBA_C_API_H

#include <stdlib.h>
#include <stdbool.h>

typedef void* Jieba;
Jieba NewJieba(const char* dict_path, const char* hmm_path, const char* user_dict, const char* idf_path, const char* stop_word_path);
void FreeJieba(Jieba);

typedef struct {
  char* word;
  size_t len;
} CJiebaWord;

void FreeWords(CJiebaWord* words);

CJiebaWord* Cut(Jieba handle, const char* sentence, int is_hmm_used);
CJiebaWord* CutAll(Jieba handle, const char* sentence);
CJiebaWord* CutForSearch(Jieba handle, const char* sentence, int is_hmm_used);
CJiebaWord* Tag(Jieba handle, const char* sentence);
void AddWord(Jieba handle, const char* word);

struct CWordWeight {
  char* word;
  double weight;
};

CJiebaWord* Extract(Jieba handle, const char* sentence, int top_k);
struct CWordWeight* ExtractWithWeight(Jieba handle, const char* sentence, int top_k);
void FreeWordWeights(struct CWordWeight* wws);

#endif
