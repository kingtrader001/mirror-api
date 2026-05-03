import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- APKA FRESH SESSION DATA ---
# Token Expiry: 12:47:54 PM
MY_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzc3NzkwODc0IiwibmJmIjoiMTc3Nzc5MDg3NCIsImV4cCI6IjE3Nzc3OTI2NzQiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiI1LzMvMjAyNiAxMjo0Nzo1NCBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjU3OTE5MjMiLCJVc2VyTmFtZSI6IjkxODQzOTE4MTI2NiIsIlVzZXJQaG90byI6IjEiLCJOaWNrTmFtZSI6Ik1lbWJlck5OR0FRU1RYIiwiQW1vdW50IjoiMC45OCIsIkludGVncmFsIjoiMCIsIkxvZ2luTWFyayI6Ikg1IiwiTG9naW5UaW1lIjoiNS8zLzIwMjYgMTI6MTc6NTQgUE0iLCJMb2dpbklQQWRkcmVzcyI6IjI0MDk6NDBkMjoxMjZjOjEzNjQ6NzQ0Yzo5MmQyOjhjODplMTlmIiwiRGJOdW1iZXIiOiIwIiwiSXN2YWxpZGF0b3IiOiIwIiwiS2V5Q29kZSI6IjU3IiwiVG9rZW5UeXBlIjoiQWNjZXNzX1Rva2VuIiwiUGhvbmVUeXBlIjoiMCIsIlVzZXJUeXBlIjoiMCIsIlVzZXJOYW1lMiI6IiIsImlzcyI6Imp3dElzc3VlciIsImF1ZCI6ImxvdHRlcnlUaWNrZXQifQ.QHmjPpYVnv33Z4tVCGIIup772c3aXkAePWdaWXGF1H4"
MY_USER_ID = "5791923"

@app.route('/')
def home():
    return "Mirror Server: Stable Mode Active (No-Login)", 200

@app.route('/get_session_mirror')
def get_session_mirror():
    # Bina kisi delay ke turant aapka session bhejega
    return jsonify({
        "token": MY_TOKEN,
        "userId": MY_USER_ID,
        "status": "success"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
