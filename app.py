#!/usr/local/bin/python3
import json

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from read_json import startElasticSearch

content = ""
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#
# @app.route('/result', methods=['GET'])
# def send_result():
#     return jsonify({'result': queryBuilder'This is result JSON'})
#

@app.route('/query', methods=['GET','POST'])
@cross_origin()
def get_query():
    content = request.get_json()
    print(json.dumps(content,indent=2))
    es = startElasticSearch()
    #result = es.search("mr", content)
    return jsonify({'name':'meric'})


if __name__ == '__main__':
    app.run(debug=True)
