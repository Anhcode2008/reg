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
class reg_pro5:
    def __init__(self, cookie, name):
        self.cookie = cookie
        self.name = name

        # lấy uid
        if "c_user=" not in cookie:
            raise Exception("COOKIE_DIE")

        self.uid = cookie.split("c_user=")[1].split(";")[0]

        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0"
        }

        r = requests.get("https://www.facebook.com/me", headers=headers, timeout=15)
        html = r.text

        # lấy fb_dtsg an toàn
        self.fb_dtsg = None
        if "fb_dtsg" in html:
            try:
                self.fb_dtsg = html.split('{"name":"fb_dtsg","value":"')[1].split('"')[0]
            except:
                try:
                    self.fb_dtsg = html.split(',"f":"')[1].split('"')[0]
                except:
                    pass

        if not self.fb_dtsg:
            raise Exception("COOKIE_DIE")

    def Reg(self):
        data = {
            "av": self.uid,
            "fb_dtsg": self.fb_dtsg,
            "variables": json.dumps({
                "input": {
                    "name": self.name,
                    "actor_id": self.uid
                }
            }),
            "doc_id": "5903223909690825"
        }

        res = requests.post(
            "https://www.facebook.com/api/graphql/",
            headers={"cookie": self.cookie, "user-agent": "Mozilla/5.0"},
            data=data,
            timeout=15
        )

        try:
            return res.json()
        except:
            return res.text

# ================= MAIN LOOP =================
dem = 0

arrayho = ["Nguyễn","Trần","Lê","Phạm","Hoàng","Huỳnh","Võ","Vũ","Phan"]
arraylot = ["Công","Đức","Gia","Anh","Quốc","Văn","Hữu"]
arrayten = ["Hưng","Tuấn","Hoàng","Phúc","Khang","Dương","Kiệt","Vinh","An"]

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
