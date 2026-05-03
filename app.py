import time

# --- AAPKI DETAILS ---
USER_PHONE = "918439181266" # User Summary se liya gaya
USER_PASSWORD = "72483382A" 

cached_token = None

def get_fresh_token():
    global cached_token
    login_url = "https://fortransferapi777.top/api/webapi/mlogin" # Login endpoint
    payload = {"account": USER_PHONE, "password": USER_PASSWORD}
    
    try:
        r = requests.post(login_url, json=payload)
        res = r.json()
        if res.get('code') == 0:
            # Token format: Bearer + data
            cached_token = "Bearer " + res['data']['token']
            return cached_token
    except:
        return None

@app.route('/get_mirror_upi', methods=['POST'])
def get_upi():
    global cached_token
    if not cached_token:
        get_fresh_token()
    
    # ... baki logic wahi rahega ...
    # Agar request 401 (Unauthorized) de, toh get_fresh_token() dobara call karein
