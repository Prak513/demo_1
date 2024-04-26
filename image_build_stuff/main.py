from flask import Flask, jsonify, redirect
import os


app = Flask(__name__)

CURRENT_MIRRORING_LIST = os.getenv("CURRENT_MIRRORING_LIST")


@app.route("/info")
def get_mirroring_info():
    return jsonify({"current_running_mirroring": CURRENT_MIRRORING_LIST})


@app.route("/")
def redirects():
    return redirect("/info")


app.run(host="0.0.0.0", port=8181)
