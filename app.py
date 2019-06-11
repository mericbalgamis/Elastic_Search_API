#!/usr/local/bin/python3
from flask import Flask, jsonify, request

app = Flask(__name__)



@app.route('/result', methods=['GET'])
def send_result():
    return jsonify({'result': 'This is result JSON'})


@app.route('/query', methods=['POST'])
def get_query():
    return jsonify({'msg': 'This is a Test'})


if __name__ == '__main__':
    app.run(debug=True)
