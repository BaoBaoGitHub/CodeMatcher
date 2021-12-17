import pickle as pk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


def save_pkl(path, data):
    """
    将data序列化到路径为path的pkl文件中
    :param path: 文件路径
    :param data: 需要序列化的对象
    :return:
    """
    pk.dump(data, open(path, 'wb'))


def load_pkl(path):
    """
    从以path为路径的文件反序列化到内存中
    :param path: 文件路径
    :return: 反序列化的对象
    """
    return pk.load(open(path, 'rb'))


def load_txt(path):
    """
    读取path为路径的文件内容， 并返回以行为元素的内容列表
    :param path: 文件路径
    :return: 文件中的内容
    """
    with open(path, 'r', encoding='utf-8') as infile:
        return infile.readlines()


def save_txt(path, lines):
    """
    将lines列表的内容写入到路径为path的文件中
    :param path:文件路径
    :param lines: 要写入的内容
    :return:
    """
    with open(path, 'w', encoding='utf-8') as infile:
        infile.writelines(lines)


def get_stemmed(token):
    """
    提取{token}的词干

    :param token:
    :return:
    """
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def get_synonyms(token):
    """
    对给定的{token}，找出除了它本身以外的同义词，组成一个列表并返回

    :param token: 一个单词的词根
    :return:
    """
    synonyms = []
    for syn in wordnet.synsets(token):  #找wordnet中{token}的synsets（认知同义词），暂时简单理解为同义词
        for lemma in syn.lemmas():
            lem = lemma.name()
            if lem not in synonyms and lem != token:
                synonyms.append(lem)
    return synonyms


def get_tokens(line):
    """
    使用word_tokenize方法将line分词，再将用"-"隔开的单词进一步分词

    :param line: 需要分词的字符串
    :return: 分词后的列表
    """
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
