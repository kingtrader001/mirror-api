import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- CONFIGURATION ---
USER_PHONE = "918439181266" 
USER_PASSWORD = "72483382A"
BASE_URL = "https://fortransferapi777.top/api/webapi"

cached_token = None

def get_fresh_token():
    global cached_token
    login_url = f"{BASE_URL}/mlogin"
    # Game ke login payload ke hisaab se
    payload = {
        "account": USER_PHONE, 
        "password": USER_PASSWORD,
        "main_mark": "H5" # Standard for web login
    }
    
    try:
        r = requests.post(login_url, json=payload, timeout=10)
        res = r.json()
        if res.get('code') == 0:
            cached_token = "Bearer " + res['data']['token']
            print("Successfully fetched new token!")
            return cached_token
    except Exception as e:
        print(f"Login Error: {e}")
    return None

@app.route('/get_mirror_upi', methods=['POST'])
def get_upi():
    global cached_token
    user_amt = request.json.get('amount', '100')
    
    # 1. Agar token nahi hai toh login karo
    if not cached_token:
        get_fresh_token()

    def make_request(token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
            "Origin": "https://www.rajastake1.com"
        }
        payload = {
            "amount": int(float(user_amt)),
            "payTypeId": 26000,
            "isFast": False
        }
        return requests.post(f"{BASE_URL}/GetPayUrl", json=payload, headers=headers, timeout=10)

    try:
        # 2. Pehli koshish existing token ke sath
        r = make_request(cached_token)
        res = r.json()

        # 3. Agar token expire ho gaya (code 401 ya specific game error)
        if res.get('code') == 401 or res.get('msg') == "Unauthorized":
            print("Token expired, refreshing...")
            new_token = get_fresh_token()
            if new_token:
                r = make_request(new_token)
                res = r.json()

        if res.get('code') == 0:
            return jsonify({
                "upi": res['data']['upiId'], 
                "status": "success",
                "auto_refreshed": True
            })
        
        return jsonify({"upi": "7248331519@ibl", "status": "failed", "msg": res.get('msg')})

    except Exception as e:
        return jsonify({"upi": "7248331519@ibl", "status": "error", "details": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
