import util
import operator
import re


def matcher_name(words, line, cmd):
    cmd = str(cmd).replace('.*', ' ').strip().split(' ')
    line = str(line).replace('\n', '')

    word_usage = len(cmd) / len(words)
    line_coverage = len(''.join(cmd)) / len(line)
    score = word_usage * line_coverage
    return score


def matcher_api(query, line, jdk):
    line = str(line).replace('\n', '').lower()
    index = []
    freq = 0
    count = 0
    for word in query:
        pattern = re.compile(word.lower())
        wi = [i.start() for i in pattern.finditer(line)]
        if len(wi) > 0:
            freq += len(wi) * len(word)
            count += 1
            index.append(wi)
    word_usage = count / len(query)
    line_coverage = freq / len(line)
    max_sequence = len(sequence(index)) / len(query)

    apis = line.split(',')
    api_count = 0
    jdk_count = 0
    for api in apis:
        if '.' in api:
            api_count += 1
            if '(' in api or '[' in api or '<' in api:
                api = api[:api.rfind('.')]
            if api in jdk:
                jdk_count += 1
    jdk_percent = 0
    if api_count > 0:
        jdk_percent = jdk_count / api_count

    score = word_usage * line_coverage * max_sequence * jdk_percent
    return score


def sequence(seq):
    orders = []
    scores = []
    for i in range(len(seq)):
        scores.append(0)
        for si in seq[i]:
            orders.append([si])
        for k in range(len(orders)):
            sik = orders[k][-1]

            for j in range(i + 1, len(seq)):
                for l in range(len(seq[j])):
                    sjl = seq[j][l]

                    if sik < sjl:
                        temp = []
                        temp.extend(orders[k])
                        temp.append(sjl)
                        orders.append(temp)
    for o in orders:
        scores[len(o) - 1] += 1
    return scores


def reranking(query_parse, data, cmds):
    jdk = util.load_pkl('data/jdk_vocab.pkl')
    query = query_parse[0]

    lines = []

    scores = list()
    for j in range(len(data)):
        res = data[j]['_source']
        line = res['method']
        cmd = cmds[j]
        scores.append([j, matcher_name(query, line, cmd)])
    scores.sort(key=operator.itemgetter(1), reverse=True)

    scores = scores[:100]
    for j in range(len(scores)):
        idx = scores[j][0]
        res = data[idx]['_source']
        line = res['parsed']
        scores[j].append(matcher_api(query, line, jdk))
    scores.sort(key=operator.itemgetter(1, 2), reverse=True)

    count = 10
    if len(data) < 10:
        count = len(data)
    for j in range(count):
        idx = scores[j][0]
        lines.append(data[idx]['_source']['source'])

    return lines
