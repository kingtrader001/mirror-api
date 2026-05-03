import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

# 1. Pehle Flask app define karo (Sabse upar hona chahiye)
app = Flask(__name__)
CORS(app)

# 2. Configuration
USER_PHONE = "918439181266"
USER_PASSWORD = "72483382A"
BASE_URL = "https://fortransferapi777.top/api/webapi"

# 3. Routes (Ab 'app' define ho chuka hai, toh error nahi aayega)
@app.route('/')
def home():
    return "Mirror Server Active", 200

@app.route('/get_session_mirror')
def get_session_mirror():
    payload = {
        "account": USER_PHONE,
        "password": USER_PASSWORD,
        "main_mark": "H5"
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B)"
    }
    try:
        r = requests.post(f"{BASE_URL}/mlogin", json=payload, headers=headers, timeout=15)
        if r.status_code == 200:
            res = r.json()
            if res.get('code') == 0:
                return jsonify({
                    "token": res['data']['token'],
                    "userId": res['data']['userId'],
                    "status": "success"
                })
        return jsonify({"status": "failed", "error": "Login invalid"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
