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
        """创建名为{self.index_name}的索引，指定body为{body}"""
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
        """删除索引"""
        self.es.indices.delete(index_name)

    def fill_data(self, path_formatted_repos):
        """将unzipdata下的10个pkl文件反序列化为对象，
        并用bulk方法批量处理，加载到elasticsearch中"""
        for i in range(10):
            print(str(i) + '-9')
            body = util.load_pkl(
                path_formatted_repos + 'body' + str(i) + '.pkl')
            helpers.bulk(self.es, body, )
            print('success')

    def fuzzy_search(self, query_parse, top_k):
        """
        调用elasticsearch搜索引擎去搜索top_k个查询词

        :param query_parse: 解析后的查询词，具体来说，列表的第一个元素是处理后的查询词列表，第二个元素是排序后的下标，下标指示其在第一个元素中的位置
        :param top_k: 要求返回多少条结果
        :return: 一个元组，第一个元素是elasticsearch返回的结果列表，第二个元素是查询内容列表，两者一一对应
        """
        query = query_parse
        query_words = list(query[0])
        query_sorts = list(query[1])

        #.表示匹配除换行符\n之外的任何单字符，*表示零次或多次。
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
        """
        用cmd执行elasticsearch，去重后返回源代码

        :param cmd: 正则匹配串
        :param source_hash:保存搜索到代码串的hash值列表
        :return:{respond}是去重后的源代码列表，{query_cmd}是查询的正则串列表，两者一一对应
        """
        query = {"query": {"regexp": {"method": cmd.lower()}}}
        #用正则表达式执行查询
        scan_resp = helpers.scan(self.es, query, index=self.index_name,
                                 scroll="10m")
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

    # se.delete_index(se.index_name)
