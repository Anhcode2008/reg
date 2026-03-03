# ================= IMPORT =================
import os
import sys
import time
import json
import random
import requests
from time import sleep

# ================= CLEAR =================
os.system("cls" if os.name == "nt" else "clear")

# ================= UI =================
dau = "\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> "

banner = """
\033[1;34m╔═══════════╗
\033[1;36m║▇◤▔▔▔▔▔▔▔◥▇║
\033[1;36m║▇▏◥▇◣┊◢▇◤▕▇║
\033[1;36m║▇▏▃▆▅▎▅▆▃▕▇║
\033[1;36m║▇▏╱▔▕▎▔▔╲▕▇║
\033[1;36m║▇◣◣▃▅▎▅▃◢◢▇║
\033[1;36m║▇▇◣◥▅▅▅◤◢▇▇║
\033[1;36m║▇▇▇◣╲▇╱◢▇▇▇║
\033[1;36m║▇▇▇▇◣▇◢▇▇▇▇║
\033[1;34m╚═══════════╝
\033[1;31m────────────────────────────────────────────
\033[1;33mREG PAGE PRO5 | ADMIN: ANHCODE
\033[1;31m────────────────────────────────────────────
"""
print(banner)

# ================= LOAD COOKIE =================
try:
    with open("cookie.txt", "r", encoding="utf-8") as f:
        cookies = [i.strip() for i in f if i.strip()]
    if not cookies:
        print("❌ cookie.txt rỗng")
        sys.exit()
except:
    print("❌ Không tìm thấy cookie.txt")
    sys.exit()

# ================= DELAY =================
DL = 500

def delay(t):
    for i in range(t, 0, -1):
        for c in ["31","32","33","35","36"]:
            print(f"{dau}\033[1;{c}m🍉 Đang Delay Reg Pro5 🍉 > {i} < Giây\033[0m", end="\r")
            sleep(0.2)
    print()

# ================= CLASS REG =================
class reg_pro5():
    def __init__(self,cookies, name) -> None:
        self.cookies = cookies
        self.id_acc = self.cookies.split('c_user=')[1].split(';')[0]
        headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi',
            'cookie': self.cookies,
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'viewport-width': '1366',
        }
        url_profile = requests.get('https://www.facebook.com/me', headers=headers).url
        profile = requests.get(url_profile, headers=headers).text
        try:
            self.fb_dtsg = profile.split('{"name":"fb_dtsg","value":"')[1].split('"},')[0]
        except:
            self.fb_dtsg = profile.split(',"f":"')[1].split('","l":null}')[0]
    def Reg(self):
        
        headers = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            # Requests sorts cookies= alphabetically
            'cookie': self.cookies,
            'origin': 'https://www.facebook.com',
            'referer': 'https://www.facebook.com/pages/creation?ref_type=launch_point',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'viewport-width': '979',
            'x-fb-friendly-name': 'AdditionalProfilePlusCreationMutation',
            'x-fb-lsd': 'ZM7FAk6cuRcUp3imwqvHTY',
        }

        data = {
            'av': self.id_acc,
            '__user': self.id_acc,
            '__a': '1',
            '__dyn': '7AzHxq1mxu1syUbFuC0BVU98nwgU29zEdEc8co5S3O2S7o11Ue8hw6vwb-q7oc81xoswIwuo886C11xmfz81sbzoaEnxO0Bo7O2l2Utwwwi831wiEjwZwlo5qfK6E7e58jwGzE8FU5e7oqBwJK2W5olwuEjUlDw-wUws9ovUaU3qxWm2Sq2-azo2NwkQ0z8c84K2e3u362-2B0oobo',
            '__csr': 'gP4ZAN2d-hbbRmLObkZO8LvRcXWVvth9d9GGXKSiLCqqr9qEzGTozAXiCgyBhbHrRG8VkQm8GFAfy94bJ7xeufz8jK8yGVVEgx-7oiwxypqCwgF88rzKV8y2O4ocUak4UpDxu3x1K4opAUrwGx63J0Lw-wa90eG18wkE7y14w4hw6Bw2-o069W00CSE0PW06aU02Z3wjU6i0btw3TE1wE5u',
            '__req': 't',
            '__hs': '19296.HYP:comet_pkg.2.1.0.2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1006496476',
            '__s': '1gapab:y4xv3f:2hb4os',
            '__hsi': '7160573037096492689',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': '25404',
            'lsd': 'ZM7FAk6cuRcUp3imwqvHTY',
            '__aaid': '800444344545377',
            '__spin_r': '1006496476',
            '__spin_b': 'trunk',
            '__spin_t': '1667200829',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
            'variables': '{"input":{"bio":"","categories":["181475575221097"],"creation_source":"comet","name":"'+name+'","page_referrer":"launch_point","actor_id":"'+self.id_acc+'","client_mutation_id":"1"}}',
            'server_timestamps': 'true',
            'doc_id': '5903223909690825',
        }
        
        response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data)     
        try:
            return response.json()
        except:
                return response.text
# ================= MAIN LOOP =================
dem = 0

arrayho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Vũ", "Phan", "Trương", "Bùi", "Đặng", "Đỗ", "Ngô", "Hồ", "Dương", "Đinh"]
arraylot = ["Công", "Đức", "Duy", "Gia", "Anh", "Hồng", "Đinh", "Quốc", "Quỳnh","Vĩnh"]
arrayten = ["Hưng","Anh", "Văn", "Tuấn", "Hoàng", "Quốc", "Năm", "Giang", "Khang", "Dương", "Phúc", "Thiên", "Hùng", "Kiệt", "Châu", "Quỳnh", "huệ", "Tuấn", "Khánh", "Trân", "Yên", "Lợi", "Danh", "Vinh", "Nhi", "Nhí", "Quốc", "Anh", "Danh", "Hân", "Giang","Phán"]

while True:
    if not cookies:
        print("❌ HẾT COOKIE – DỪNG TOOL")
        break

    ck = random.choice(cookies)
    name = f"{random.choice(arrayho)} {random.choice(arraylot)} {random.choice(arrayten)}"
    dem += 1

    try:
        kq = reg_pro5(ck, name).Reg()
        print(dau, dem, kq)
    except Exception:
        print(dau, dem, "❌ COOKIE DIE / BLOCK")
        cookies.remove(ck)

    delay(DL)
