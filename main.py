from flask import Flask, jsonify
import os
import json

DIR = os.getcwd()

app = Flask(__name__)


@app.route("/info")
def get_mirroring_info():
    data = json.load(open(f"{DIR}/mirror_list.json"))
    return jsonify(data)


app.run(host="0.0.0.0", port=8181)
