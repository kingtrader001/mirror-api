import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- YOUR UPDATED DETAILS ---
USER_PHONE = "8439181266"
USER_PASSWORD = "8439181266SK"
BASE_URL = "https://fortransferapi777.top/api/webapi"

@app.route('/')
def home():
    return "Mirror Server Live - Login Ready", 200

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
        # Naye password ke saath login request
        r = requests.post(f"{BASE_URL}/mlogin", json=payload, headers=headers, timeout=15)
        res = r.json()
        
        if r.status_code == 200 and res.get('code') == 0:
            return jsonify({
                "token": res['data']['token'],
                "userId": res['data']['userId'],
                "status": "success"
            })
        else:
            return jsonify({
                "status": "failed", 
                "msg": res.get('msg', 'Login failed'),
                "code": res.get('code')
            }), 401
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
