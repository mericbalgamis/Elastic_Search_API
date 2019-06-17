#!/usr/local/bin/python3
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
import json
from flask_restful.utils.cors import crossdomain

from read_json import startElasticSearch, searchByIndex

content = ""
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#
# @app.route('/result', methods=['GET'])
# def send_result():
#     return jsonify({'result': 'This is result JSON'})
#

@app.route('/query', methods=['GET','POST'])
@cross_origin()
def get_query():
    content = request.get_json()
    print(json.dumps(content,indent=2))
    es = startElasticSearch()
    result = es.search("restaurant", content)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
