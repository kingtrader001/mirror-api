import os
import requests
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RZP_KEY_ID = "rzp_live_SkuRu7LTmk0HiI"
RZP_KEY_SECRET = "rYENwRKOHw0tBkJ56C4w3UqT"

# Spam se bachne ke liye global timer
last_call_time = 0

@app.route('/get_razorpay_qr')
def get_razorpay_qr():
    global last_call_time
    current_time = time.time()
    
    # 10 second se pehle naya link nahi banega
    if current_time - last_call_time < 10:
        return jsonify({"status": "error", "message": "Too fast"}), 429
    
    amount_val = request.args.get('amount')
    if not amount_val or amount_val == "null":
        return jsonify({"status": "error", "message": "No amount"}), 400

    last_call_time = current_time
    amount_paise = int(float(amount_val) * 100)

    try:
        url = "https://api.razorpay.com/v1/payment_links"
        payload = {
            "amount": amount_paise,
            "currency": "INR",
            "description": "Wallet Recharge",
            "customer": {"name": "User", "contact": "8439181266", "email": "user.support@gmail.com"},
            "upi_link": True 
        }
        r = requests.post(url, json=payload, auth=(RZP_KEY_ID, RZP_KEY_SECRET))
        data = r.json()
        
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={data['short_url']}"
        return jsonify({"status": "success", "qr_url": qr_url})
    except:
        return jsonify({"status": "error"}), 500
