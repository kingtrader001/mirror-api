import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Aapka fresh token yahan set kar diya hai
MANUAL_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc3Nzg1NTcxIiwibmJmIjoiMTc3Nzc4NTU3MSIsImV4cCI6IjE3Nzc3ODczNzEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzMvMjAyNiAxMToxOTozMSBBTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjU3OTE5MjMiLCJVc2VyTmFtZSI6IjkxODQzOTE4MTI2NiIsIlVzZXJQaG90byI6IjEiLCJOaWNrTmFtZSI6Ik1lbWJlck5OR0FRU1RYIiwiQW1vdW50IjoiMC45OCIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiNS8zLzIwMjYgMTA6NDk6MzEgQU0iLCJMb2dpbklQQWRkcmVzcyI6IjE1Mi41OS44Ny43OSIsIkRiTnVtYmVyIjoiMCIsIklzdmFsaWRhdG9yIjoiMCIsIktleUNvZGUiOiI1NSIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjAiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.NB61FaxGMuYU3nGcQrKlR2XlbXFOK1ZnhT4QDAP6NYY"

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
        if r.status_code == 200 and r.text:
            res = r.json()
            if res.get('code') == 0:
                cached_token = "Bearer " + res['data']['token']
                return cached_token
    except Exception as e:
        print(f"AUTO-LOGIN FAILED: {e}")
    return cached_token # Login fail hone par manual token use karega

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
        # Agar token expire dikhaye toh auto-refresh try karo
        if r.status_code == 401 or (r.text and r.json().get('code') == 401):
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
