from collections import defaultdict
import spacy
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

nlp = spacy.load("ru_core_news_sm")
stopwords = stopwords.words("russian")
docs_ids = set()
indexes = defaultdict(set)


def process(doc, doc_id):
    for token in doc:
        if token.is_alpha and not token.like_num and not token.is_punct and token.text not in stopwords:
            indexes[token.lemma_].add(doc_id)


def create_index():
    for i in range(1, 101):
        docs_ids.add(i)
        with open("results/выкачка-" + str(i) + ".txt") as file:
            html = BeautifulSoup(file, features="html.parser")
            process(nlp(str(html.get_text(" ").lower().strip())), i)


def search_and(str1, str2):
    return indexes[str1].union(indexes[str2])

def search_or(str1, str2):
    return indexes[str1].intersection(indexes[str2])

def search_not(str1):
    return docs_ids - indexes[str1]


if __name__ == '__main__':
    create_index()
    str1 = "поисковый"
    str2 = "запрос"
    print(search_and(str1, str2))
    print(search_or(str1, str2))
    print(search_not(str1))
