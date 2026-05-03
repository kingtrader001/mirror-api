import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Agar automation fail ho, toh ye token kaam karega
# Ek baar fresh token yahan paste kar dein
MANUAL_TOKEN = "Bearer YOUR_FRESH_TOKEN_HERE"

USER_PHONE = os.environ.get('USER_PHONE', '918439181266')
USER_PASSWORD = os.environ.get('USER_PASSWORD', '72483382A')
BASE_URL = "https://fortransferapi777.top/api/webapi"

cached_token = MANUAL_TOKEN

def login_and_get_token():
    global cached_token
    login_url = f"{BASE_URL}/mlogin"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B)",
        "Origin": "https://www.rajastake1.com"
    }
    payload = {"account": USER_PHONE, "password": USER_PASSWORD, "main_mark": "H5"}

    try:
        r = requests.post(login_url, json=payload, headers=headers, timeout=10)
        # Check if response is actually JSON
        if r.status_code == 200 and r.text:
            res = r.json()
            if res.get('code') == 0:
                cached_token = "Bearer " + res['data']['token']
                print("AUTO-LOGIN SUCCESSFUL")
                return cached_token
        print(f"AUTO-LOGIN FAILED: Status {r.status_code}")
    except Exception as e:
        print(f"AUTO-LOGIN EXCEPTION: {e}")
    return cached_token # Return existing if new fails

@app.route('/')
def home():
    return "MIRROR SERVER IS LIVE", 200

@app.route('/get_mirror_upi', methods=['POST'])
def get_upi():
    global cached_token
    user_amt = request.json.get('amount', '100')

    def fetch_upi(token_to_use):
        headers = {
            "Authorization": token_to_use,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B)",
            "Origin": "https://www.rajastake1.com"
        }
        payload = {"amount": int(float(user_amt)), "payTypeId": 26000, "isFast": False}
        return requests.post(f"{BASE_URL}/GetPayUrl", json=payload, headers=headers, timeout=10)

    try:
        r = fetch_upi(cached_token)
        # Agar token expire dikhaye toh refresh try karo
        if r.status_code == 401 or (r.text and r.json().get('code') == 401):
            print("Token expired, trying auto-refresh...")
            cached_token = login_and_get_token()
            r = fetch_upi(cached_token)

        res = r.json()
        if res.get('code') == 0:
            return jsonify({"upi": res['data']['upiId'], "status": "success"})
        
        return jsonify({"upi": "7248331519@ibl", "status": "failed", "msg": res.get('msg')})
    except:
        return jsonify({"upi": "7248331519@ibl", "status": "error"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
