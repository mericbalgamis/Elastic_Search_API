#!/usr/local/bin/python3
import json, os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from read_json import startElasticSearch

path_to_CSV_output = "./csv_outputs"
content = ""
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#
# @app.route('/result', methods=['GET'])
# def send_result():
#     return jsonify({'result': queryBuilder'This is result JSON'})
#

def convert_to_CSV():
    os.system("python3.6 json_to_csv.py node ./response.json "+path_to_CSV_output+"/csv_output.csv")
    os.remove("./response.json")

def write_JSON(response):
    with open('response.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    convert_to_CSV()

@app.route('/query', methods=['GET','POST'])
@cross_origin()
def get_query():
    content = request.get_json()
    print(json.dumps(content,indent=2))
    es = startElasticSearch(sys.argv[1])
    result = es.search("mr", content)
    edited_JSON = result['hits']['hits']
    edited_JSON = "{\"node\":"+json.dumps(edited_JSON) + "}"
    write_JSON(json.loads(edited_JSON))
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
