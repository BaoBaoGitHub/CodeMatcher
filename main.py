import parsing
import reranking
from indexing import SearchEngine

if __name__ == '__main__':
    query = 'convert an inputstream to a string'
    print('This is your query:'+query)
    '''parsing'''
    query_parse = parsing.parse(query)

    '''fuzzy searching'''
    se = SearchEngine()
    data, cmds = se.fuzzy_search(query_parse, top_k=10)

    '''reranking'''
    results = reranking.reranking(query_parse, data, cmds)
    print(results)
