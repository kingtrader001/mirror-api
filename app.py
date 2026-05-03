# app.py mein ye naya route add karein
import requests

RAZORPAY_KEY_ID = "YOUR_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_KEY_SECRET"

@app.route('/get_razorpay_qr')
def get_razorpay_qr():
    amount = request.args.get('amount', '500')
    # Paisa paise mein hota hai (₹100 = 10000 paise)
    amount_in_paise = int(float(amount) * 100)

    url = "https://api.razorpay.com/v1/payment_links"
    payload = {
        "amount": amount_in_paise,
        "currency": "INR",
        "description": "Gaming Deposit",
        "upi_link": True # Direct UPI link generate karega
    }
    
    try:
        r = requests.post(url, json=payload, auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        res = r.json()
        # Razorpay ka short URL jo direct UPI QR dikhayega
        short_url = res.get('short_url')
        
        # QR Code generate karne ke liye hum Google Chart API use karenge short_url par
        qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={short_url}"
        
        return jsonify({"status": "success", "qr_url": qr_image_url})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
