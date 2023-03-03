import nltk
from collections import defaultdict
import spacy
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

nlp = spacy.load("ru_core_news_sm")
nltk.download('stopwords')

stopwords = stopwords.words("russian")
lemmas = defaultdict(set)
tokens = set()

def check_for_russian(string):
    alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]
    for one_char in str(string).lower():
        if one_char not in alphabet:
            return False
    return True

def process(doc):
    for token in doc:
        if token.is_alpha and not token.like_num and not token.is_punct and token.text not in stopwords \
                and check_for_russian(token):
            tokens.add(token.text)
            lemmas[token.lemma_].add(token.text)


def write_tokens():
    with open('tokens.txt', 'w') as file:
        file.write("\n".join(list(tokens)))


def write_lemmas():
    lemmas_list = []
    for key, values in lemmas.items():
        line = str(key).join(" ").join(list(values))
        lemmas_list.append(line)

    with open('lemmas.txt', 'w') as f:
        f.write('\n'.join(lemmas_list))


def tokenization():
    for i in range(1, 101):
        with open("../results/выкачка-" + str(i) + ".txt") as file:
            html = BeautifulSoup(file, features="html.parser")
            process(nlp(str(html.get_text(" ").lower().strip())))
    write_tokens()
    write_lemmas()


if __name__ == '__main__':
    tokenization()
