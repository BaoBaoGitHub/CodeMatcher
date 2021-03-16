import pickle as pk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


def save_pkl(path, data):
    pk.dump(data, open(path, 'wb'))


def load_pkl(path):
    return pk.load(open(path, 'rb'))


def load_txt(path):
    with open(path, 'r', encoding='utf-8') as infile:
        return infile.readlines()


def save_txt(path, lines):
    with open(path, 'w', encoding='utf-8') as infile:
        infile.writelines(lines)


def get_stemmed(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def get_synonyms(token):
    synonyms = []
    for syn in wordnet.synsets(token):
        for lemma in syn.lemmas():
            lem = lemma.name()
            if lem not in synonyms and lem != token:
                synonyms.append(lem)
    return synonyms


def get_tokens(line):
    tokens = list()
    for token in word_tokenize(line, 'english'):
        if len(token) > 1:
            if '-' in token:
                ts = token.split('-')
                for t in ts:
                    tokens.append(t)
            else:
                tokens.append(token)
    return tokens
