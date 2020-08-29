"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""
from flask import Flask
from customerAPI import customer_api

app = Flask(__name__)

app.register_blueprint(customer_api)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True, port=8080)