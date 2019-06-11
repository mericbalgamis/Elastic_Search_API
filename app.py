#!/usr/local/bin/python3
from flask import Flask, jsonify, request

app = Flask(__name__)



@app.route('/result', methods=['GET'])
def send_result():
    return jsonify({'result': 'This is result JSON'})


@app.route('/query', methods=['POST'])
def get_query():
    print(request.is_json)
    content = request.get_json()
    return jsonify(content)


if __name__ == '__main__':
    app.run(debug=True)
