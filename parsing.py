import util
import nltk
import operator
from nltk.stem import PorterStemmer

type_cd = ['CD']
type_cc = ['CC']
type_in = ['IN']
type_to = ['TO']
type_jj = ['JJ', 'JJR', 'JJS']
type_nn = ['NN', 'NNS', 'NNP', 'NNPS']
type_rb = ['RB', 'RBR', 'RBS']
type_vb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
type_ky = ['KY']
type_all = type_cd + type_cc + type_in + type_to + type_jj + type_nn + type_rb + type_vb + type_ky


def query_parse(query, path_parsed_vocab, path_method_vocab):
    vjdk = dict(util.load_pkl(path_parsed_vocab))
    vword = dict(util.load_pkl(path_method_vocab))
    stemmer = PorterStemmer()
    str_replace = ['in java', 'using java', 'java', 'how to', 'how do', 'what is']

    for str_re in str_replace:
        query = query.replace(str_re, '')

    data = []
    tokens = util.get_tokens(query)
    tokens = nltk.pos_tag(tokens)

    for token in tokens:
        tvalue = token[0]
        ttype = token[1]
        if ttype in type_all:
            para = 0
            impact = 0
            stem = stemmer.stem(tvalue)
            if stem in vword:
                para = 1
                impact = vword[stem]
            else:
                freq = []
                syns = util.get_synonyms(stem)
                for syn in syns:
                    score = 0
                    stem = util.get_stemmed(syn)
                    if stem in vword:
                        score = vword[stem]
                    freq.append(score)
                idx_max_freq = -1
                if len(freq) > 0:
                    idx_max_freq = freq.index(max(freq))
                if idx_max_freq > -1:
                    tvalue = syns[idx_max_freq]
                    para = 1
                    impact = vword[tvalue]
            if ttype in type_nn and stem in vjdk:
                para = 2
                impact = vjdk[stem]
            tvalue = util.get_stemmed(tvalue)

            vector = [tvalue, ttype, para, impact]
            data.append(vector)
    return data


def parse(query):
    items = query_parse(query,
                        path_parsed_vocab='data/parsed_vocab_jdk_item.pkl',
                        path_method_vocab='data/method_vocab_stemed.pkl')

    # sorting words
    mid_list1 = list()
    mid_list2 = list()
    word_list1 = list()
    word_list2 = list()
    other_list1 = list()
    other_list2 = list()
    for j in range(len(items)):
        item = items[j]
        if item[1] in type_cc + type_to + type_in:
            if item[2] is 1:
                mid_list1.append([j, items[j][3]])
            else:
                mid_list2.append([j, items[j][3]])
        elif item[1] in type_vb + type_nn:
            if item[2] is 1:
                word_list1.append([j, items[j][3]])
            else:
                word_list2.append([j, items[j][3]])
        else:
            if item[2] is 1:
                other_list1.append([j, items[j][3]])
            else:
                other_list2.append([j, items[j][3]])

    mid_list1.sort(key=operator.itemgetter(1))
    mid_list2.sort(key=operator.itemgetter(1))
    word_list1.sort(key=operator.itemgetter(1))
    word_list2.sort(key=operator.itemgetter(1))
    other_list1.sort(key=operator.itemgetter(1))
    other_list2.sort(key=operator.itemgetter(1))

    sort_list = mid_list1 + mid_list2 + other_list1 + other_list2 + word_list1 + word_list2
    for j in range(len(sort_list)):
        sort_list[j] = sort_list[j][0]

    query_list = list()
    for item in items:
        query_list.append(item[0])

    line = [query_list, sort_list]
    return line
