import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- RAZORPAY LIVE KEYS ---
RZP_KEY_ID = "rzp_live_SkuRu7LTmk0HiI"
RZP_KEY_SECRET = "rYENwRKOHw0tBkJ56C4w3UqT"

@app.route('/')
def home():
    return "Razorpay Mirror Server: Live and Running", 200

@app.route('/get_razorpay_qr')
def get_razorpay_qr():
    try:
        amount_val = request.args.get('amount', '500')
        amount_paise = int(float(amount_val) * 100)

        url = "https://api.razorpay.com/v1/payment_links"
        payload = {
            "amount": amount_paise,
            "currency": "INR",
            "accept_partial": False,
            "description": "Wallet Deposit",
            "customer": {
                "name": "App User",
                "email": "user.support@gmail.com",
                "contact": "8439181266"  # Valid number for validation
            },
            "notify": {"sms": False, "email": False},
            "reminder_enable": False,
            "upi_link": True 
        }

        response = requests.post(url, json=payload, auth=(RZP_KEY_ID, RZP_KEY_SECRET), timeout=15)
        res_data = response.json()

        if response.status_code == 200 or response.status_code == 201:
            short_url = res_data.get('short_url')
            qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={short_url}"
            
            return jsonify({
                "status": "success",
                "qr_url": qr_image_url,
                "payment_id": res_data.get('id')
            })
        else:
            return jsonify({"status": "failed", "error": res_data}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
