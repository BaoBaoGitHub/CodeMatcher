from elasticsearch import Elasticsearch
from elasticsearch import helpers
import hashlib
import util


class SearchEngine:
    def __init__(self):
        self.index_name = "search_engine"
        self.ip = "localhost:9200"
        self.es = Elasticsearch([self.ip])
        self.id = 0

    def create_index(self):
        body = {"mappings":
                    {"properties":
                      {
                       "comment": {"type": "text"},
                       "javadoc": {"type": "text"},
                       "method": {"type": "text"},
                       "modifier": {"type": "text"},
                       "package": {"type": "text"},
                       "parameter": {"type": "text"},
                       "parsed": {"type": "text"},
                       "return": {"type": "text"},
                       "source": {"type": "text"}
                       }
                }
               }
        self.es.indices.create(index=self.index_name, body=body)

    def delete_index(self, index_name):
        self.es.indices.delete(index_name)

    def fill_data(self, path_formatted_repos):
        for i in range(10):
            print(str(i) + '-9')
            body = util.load_pkl(path_formatted_repos + 'body' + str(i) + '.pkl')
            helpers.bulk(self.es, body)
            print('success')

    def fuzzy_search(self, query_parse, top_k):
        query = query_parse
        query_words = list(query[0])
        query_sorts = list(query[1])

        cmd = '.*' + '.*'.join(query_words) + '.*'
        data = []
        cmds = []
        source_hash = []
        respond, query_cmd = self.search_respond(cmd, source_hash)
        data.extend(respond)
        cmds.extend(query_cmd)
        idx = 0
        while len(data) < top_k and len(query_words) - idx >= 2:
            temp = []
            if idx == 0:
                s = [query_sorts[0]]
            else:
                s = query_sorts[:idx]
            for j in range(len(query_words)):
                if j not in s:
                    temp.append(query_words[j])
            cmd = '.*'.join(temp) + '.*'
            respond, query_cmd = self.search_respond(cmd, source_hash)
            data.extend(respond)
            cmds.extend(query_cmd)
            idx += 1
        return data, cmds

    def search_respond(self, cmd, source_hash):
        query = {"query": {"regexp": {"method": cmd.lower()}}}
        scan_resp = helpers.scan(self.es, query, index=self.index_name, scroll="10m")
        respond = []
        query_cmd = []
        for hit in scan_resp:
            source = str(hit['_source']['source'])
            hash_val = hashlib.md5(source.encode('utf-8')).digest()
            if hash_val not in source_hash:
                source_hash.append(hash_val)
                respond.append(hit)
                query_cmd.append(cmd)
        return respond, query_cmd


if __name__ == '__main__':
    se = SearchEngine()

    # create ElasticSearch index
    se.create_index()

    # fill formatted data into indexed ElasticSearch
    se.fill_data('unzipdata/')
