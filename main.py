from flask import Flask, request, jsonify
import os
import requests

app = Flask(_name_)

BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

@app.route("/")
def home():
    return "Bot está rodando!"

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "source_channel": SOURCE_CHANNEL,
        "target_channel": TARGET_CHANNEL
    })

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
