@app.route('/get_session_mirror')
def get_session_mirror():
    # Aapki details
    payload = {"account": "918439181266", "password": "72483382A", "main_mark": "H5"}
    try:
        r = requests.post("https://fortransferapi777.top/api/webapi/mlogin", json=payload, timeout=10)
        res = r.json()
        if res.get('code') == 0:
            return jsonify({
                "token": res['data']['token'],
                "userId": res['data']['userId'],
                "status": "success"
            })
    except: pass
    return jsonify({"status": "error"})
