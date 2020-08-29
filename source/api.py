#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from model.database import Database

app = Flask(__name__)

# 
@app.route('/get/password', methods=['GET'])
def get_context():


# 
@app.route('/u', methods=['POST'])
def upload_context():
 

if __name__ == "__main__":
    app.run(debug=True, port=8080)