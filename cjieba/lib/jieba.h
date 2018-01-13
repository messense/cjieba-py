#ifndef CJIEBA_C_API_H
#define CJIEBA_C_API_H

#include <stdlib.h>
#include <stdbool.h>

typedef void* Jieba;
Jieba NewJieba(const char* dict_path, const char* hmm_path, const char* user_dict, const char* idf_path, const char* stop_word_path);
void FreeJieba(Jieba);

typedef struct {
  char** words;
  size_t len;
} CJiebaWords;

void FreeCJiebaWords(CJiebaWords* words);

CJiebaWords* Cut(Jieba handle, const char* sentence, int is_hmm_used);
CJiebaWords* CutAll(Jieba handle, const char* sentence);
CJiebaWords* CutForSearch(Jieba handle, const char* sentence, int is_hmm_used);
CJiebaWords* Tag(Jieba handle, const char* sentence);
void AddWord(Jieba handle, const char* word);

typedef struct {
  size_t offset;
  size_t len;
} Token;

typedef enum {
  DefaultMode = 0,
  SearchMode = 1,
} TokenizeMode;

Token* Tokenize(Jieba x, const char* sentence, TokenizeMode mode, int is_hmm_used);
void FreeToken(Token* tokens);

struct CWordWeight {
  char* word;
  double weight;
};

CJiebaWords* Extract(Jieba handle, const char* sentence, int top_k);
struct CWordWeight* ExtractWithWeight(Jieba handle, const char* sentence, int top_k);
void FreeWordWeights(struct CWordWeight* wws);

#endif
