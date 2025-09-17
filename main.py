from flask import Flask, request, jsonify
import os
import requests

app = Flask(_name_)

BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
SOURCE_CHANNEL = str(os.getenv("SOURCE_CHANNEL", "")).strip()  # ex: -1002810508717
TARGET_CHANNEL = str(os.getenv("TARGET_CHANNEL", "")).strip()  # ex: -1003099015408

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# rota simples pra testar
@app.route("/")
def home():
    return "Bot está rodando!"

# rota de saúde
@app.route("/health")
def health():
    return jsonify({
        "ok": True,
        "source_channel": SOURCE_CHANNEL,
        "target_channel": TARGET_CHANNEL
    })

# Webhook que recebe as atualizações do Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    # Mensagens de canal (channel_post) e mensagens normais (message)
    update = data.get("channel_post") or data.get("message")
    if not update:
        return jsonify({"ok": False, "desc": "Sem message/channel_post"}), 200

    chat = update.get("chat", {})
    chat_id = str(chat.get("id", ""))

    # Só processa se vier do canal de ORIGEM
    if chat_id != str(SOURCE_CHANNEL):
        return jsonify({"ok": True, "desc": "ignorado: outro chat"}), 200

    # Texto puro
    text = update.get("text")
    # Legenda de mídia (caso o canal poste foto+legenda)
    caption = update.get("caption")

    content = caption if caption else text
    if content:
        send_message(TARGET_CHANNEL, content)

    return jsonify({"ok": True}), 200

def send_message(chat_id: str, text: str):
    try:
        url = f"{TELEGRAM_API}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": True
        }
        requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print(f"[send_message] erro: {e}")

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
