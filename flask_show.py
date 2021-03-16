from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print('ip:', ip)
    return render_template('index.html')


@app.route('/search/<query>', methods=['POST', 'GET'])
def search(query):
    print(query)
    import parsing
    query_parse = parsing.parse(query)
    print(1)
    from indexing import SearchEngine
    se = SearchEngine()
    data, cmds = se.fuzzy_search(query_parse, top_k=10)
    import reranking
    results = reranking.reranking(query_parse, data, cmds)
    print(3)
    print(results)
    # return render_template('search.html',results=results)
    return jsonify({"result": results})


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
