import os
from collections import defaultdict
import spacy
from nltk.corpus import stopwords
import numpy as np
from bs4 import BeautifulSoup

nlp = spacy.load("ru_core_news_sm")

stopwords = stopwords.words("russian")
#lemmas = defaultdict(set)
#tokens = set()
docs_frq_tokens = defaultdict(dict)
docs_frq_lemmas = defaultdict(dict)
token_in_docs_frq = defaultdict(int)
lemmas_in_docs_frq = defaultdict(int)

def check_for_russian(string):
    alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]
    for one_char in str(string).lower():
        if one_char not in alphabet:
            return False
    return True

def process(doc_id, doc):
    used_tokens = []
    used_lemmas = []
    docs_frq_tokens[doc_id] = dict()
    docs_frq_lemmas[doc_id] = dict()
    for token in doc:
        if token.is_alpha and not token.like_num and not token.is_punct and token.text not in stopwords \
                and check_for_russian(token):
            if docs_frq_lemmas[doc_id].__contains__(token.lemma_):
                docs_frq_lemmas[doc_id][token.lemma_] += 1
            else:
                docs_frq_lemmas[doc_id][token.lemma_] = 1
            if docs_frq_tokens[doc_id].__contains__(token.text):
                docs_frq_tokens[doc_id][token.text] += 1
            else:
                docs_frq_tokens[doc_id][token.text] = 1
            if token.text not in used_tokens:
                if token_in_docs_frq.__contains__(token.text):
                    token_in_docs_frq[token.text] += 1
                else:
                    token_in_docs_frq[token.text] = 1
                used_tokens.append(token.text)
            if token.lemma_ not in used_lemmas:
                if lemmas_in_docs_frq.__contains__(token.lemma_):
                    lemmas_in_docs_frq[token.lemma_] += 1
                else:
                    lemmas_in_docs_frq[token.lemma_] = 1
                used_lemmas.append(token.lemma_)
def tokenization():
    for i in range(1, 101):
        with open("results/выкачка-" + str(i) + ".txt") as file:
            html = BeautifulSoup(file, features="html.parser")
            process(i, nlp(str(html.get_text(" ").lower().strip())))


def write_tf_ids_lemmas():
    i = 0
    dir_name = "lemmas"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    for doc_id in docs_frq_lemmas:
        i += 1
        with open(dir_name + '/tf-ids_lemmas-' + str(i) + '.txt', 'w') as file:
            for lemmas in docs_frq_lemmas[doc_id]:
                tf = docs_frq_lemmas[doc_id][lemmas] / len(docs_frq_lemmas[doc_id])
                idf = np.log10(len(lemmas_in_docs_frq) / lemmas_in_docs_frq[lemmas])
                file.write(lemmas + " " + str(idf) + " " + str(tf * idf) + "\n")


def write_tf_ids_tokens():
    i = 0
    dir_name = "tokens"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    for doc_id in docs_frq_tokens:
        i += 1
        with open(dir_name + '/tf-ids_tokens-' + str(i) + '.txt', 'w') as file:
            for token in docs_frq_tokens[doc_id]:
                tf = docs_frq_tokens[doc_id][token] / len(docs_frq_tokens[doc_id])
                idf = np.log10(len(token_in_docs_frq) / token_in_docs_frq[token])
                file.write(token + " " + str(idf) + " " + str(tf * idf) + "\n")

if __name__ == '__main__':
    tokenization()
    write_tf_ids_tokens()
    write_tf_ids_lemmas()
