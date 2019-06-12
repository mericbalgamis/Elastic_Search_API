#!/usr/local/bin/python3
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

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
    print(request.is_json)
    content = request.get_json()
    return jsonify({"message" : "successful"})


if __name__ == '__main__':
    app.run(debug=True)
