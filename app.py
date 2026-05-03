from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
# Aapka fresh token yahan hai
MIRROR_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc3NzgwNTM4IiwibmJmIjoiMTc3Nzc4MDUzOCIsImV4cCI6IjE3Nzc3ODIzMzgiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzMvMjAyNiA5OjU1OjM4IEFNIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQWNjZXNzX1Rva2VuIiwiVXNlcklkIjoiNTc5MTkyMyIsIlVzZXJOYW1lIjoiOTE4NDM5MTgxMjY2IiwiVXNlclBob3RvIjoiMSIsIk5pY2tOYW1lIjoiTWVtYmVyTk5HQVFTVFgiLCJBbW91bnQiOiIwLjk4IiwiSW50ZWdyYWwiOiIwIiwiTG9naW5NYXJrIjoiSDUiLCJMb2dpblRpbWUiOiI1LzMvMjAyNiA5OjI1OjM4IEFNIiwiTG9naW5JUEFkZHJlc3MiOiIyNDA5OjQwZDI6MTI2YzoxMzY0Ojc0NGM6OTJkMjo4Yzg6ZTE5ZiIsIkRiTnVtYmVyIjoiMCIsIklzdmFsaWRhdG9yIjoiMCIsIktleUNvZGUiOiI1MCIsIlRva2VuVHlwZSI6IkFjY2Vzc19Ub2tlbiIsIlBob25lVHlwZSI6IjAiLCJVc2VyVHlwZSI6IjAiLCJVc2VyTmFtZTIiOiIiLCJpc3MiOiJqd3RJc3N1ZXIiLCJhdWQiOiJsb3R0ZXJ5VGlja2V0In0.h-lmj_omyTQs9c2V3U1dcCGQLOTmqHd0jLwNwZ04JNQ"

# Network tab se nikaala gaya domain
BASE_URL = "https://fortransferapi777.top/api/webapi"

@app.route('/get_mirror_upi', methods=['POST'])
def get_upi():
    try:
        user_amt = request.json.get('amount', '100')
        
        headers = {
            "Authorization": MIRROR_TOKEN,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
            "Origin": "https://www.rajastake1.com",
            "Referer": "https://www.rajastake1.com/"
        }
        
        # Game ke format ke hisaab se payload (image_5fc4ab.jpg ke mutabik)
        payload = {
            "amount": int(float(user_amt)),
            "payTypeId": 26000, # ArUpiPay ID
            "isFast": False
        }

        # Game server se recharge order generate karna
        r = requests.post(f"{BASE_URL}/GetPayUrl", json=payload, headers=headers)
        res = r.json()
        
        if res.get('code') == 0:
            return jsonify({
                "upi": res['data']['upiId'], # Game ka diya naya UPI
                "status": "success"
            })
        else:
            return jsonify({"upi": "7248331519@ibl", "status": "expired_token", "msg": res.get('msg')})
            
    except Exception as e:
        return jsonify({"upi": "7248331519@ibl", "status": "error"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
