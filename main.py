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
# ================= CLASS REG =================
class reg_pro5:
    def __init__(self, cookie, name):
        self.cookie = cookie
        self.name = name

        # check cookie
        if "c_user=" not in cookie:
            raise Exception("COOKIE_DIE")

        self.uid = cookie.split("c_user=")[1].split(";")[0]

        self.session = requests.Session()
        self.session.headers.update({
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "accept-language": "vi-VN,vi;q=0.9",
        })

        # lấy fb_dtsg
        self.fb_dtsg = self._get_fb_dtsg()
        if not self.fb_dtsg:
            raise Exception("COOKIE_DIE")

    # ================= LẤY FB_DTSG AN TOÀN =================
    def _get_fb_dtsg(self):
        try:
            r = self.session.get("https://www.facebook.com/me", timeout=15)
            html = r.text

            # cách 1
            if 'fb_dtsg' in html:
                try:
                    return html.split('{"name":"fb_dtsg","value":"')[1].split('"')[0]
                except:
                    pass

            # cách 2 (fallback)
            if ',"f":"' in html:
                try:
                    return html.split(',"f":"')[1].split('"')[0]
                except:
                    pass

        except:
            return None

        return None

    # ================= REG PAGE PRO5 =================
    def Reg(self):
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "origin": "https://www.facebook.com",
            "referer": "https://www.facebook.com/pages/creation?ref_type=launch_point",
            "x-fb-friendly-name": "AdditionalProfilePlusCreationMutation",
        }

        data = {
            "av": self.uid,
            "__user": self.uid,
            "fb_dtsg": self.fb_dtsg,
            "jazoest": "25404",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AdditionalProfilePlusCreationMutation",
            "variables": json.dumps({
                "input": {
                    "bio": "",
                    "categories": ["181475575221097"],
                    "creation_source": "comet",
                    "name": self.name,
                    "page_referrer": "launch_point",
                    "actor_id": self.uid,
                    "client_mutation_id": "1"
                }
            }),
            "server_timestamps": "true",
            "doc_id": "5903223909690825"
        }

        try:
            res = self.session.post(
                "https://www.facebook.com/api/graphql/",
                headers=headers,
                data=data,
                timeout=15
            )

            try:
                return res.json()
            except:
                return res.text

        except Exception as e:
            return {"status": "error", "msg": str(e)}
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
