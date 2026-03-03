import telebot
import requests
import time
import threading
import subprocess
import json
import os
import psutil
import hashlib
import random
from datetime import datetime, timedelta, date
from urllib.parse import quote
from io import BytesIO
from telebot import types

# ================== CONFIG ==================
TOKEN = "8669252640:AAEVsAQeu916TMt88OoVKAfxD8kYKYEEMdY"
bot = telebot.TeleBot(TOKEN)

# ---- MB BANK ----
MB_ACCOUNT = "0329270154"
MB_NAME = "KIEU VAN NHAT ANH"
MB_PREFIX = "anhcode"
MB_CHECK_DELAY = 30
API_MB_HISTORY = "https://api.anhcode.io.vn/historyapimbbankv2/99372ffb7b040a3b4dfa2a934810775b"

# ---- API BUFF TIKTOK (không gửi key) ----
API_BUFF = "https://anhcode.io.vn/api/bot.php"

# ---- CONFIG KEY (từ PHP của bạn) ----
YEUMONEY_TOKEN = "56e38d42f495932dba2473dbb05a8a66974cd4db289dc9529985fbf75a4983f3"
LINK4M_API = "674701e4b29cad72ca685685"
KEY_FILE = "keyanhcode.txt"
KEY_HOURS = 12
COOLDOWN = 0

# ---- LIMIT ----
NORMAL_MIN = 5000
VIP_MIN = 20000
MAX_NORMAL = 5
MAX_VIP = 10
EXPIRE_DAYS = 10
DAILY_BUFF_TT_FREE = 1
DAILY_BUFF_TT_BASIC = 5
DAILY_BUFF_TT_VIP = 10

# ================== RAM ==================
user_state = {}
active_spam_processes = {}
checked_trans = set()

# ================== HÀM GET KEY & CHECK KEY ==================
def get_key(username):
    now = datetime.now()
    current_time = now.timestamp()

    if not os.path.exists(KEY_FILE):
        open(KEY_FILE, 'w').close()

    with open(KEY_FILE, 'r') as f:
        lines = f.read().splitlines()

    new_data = []
    user_has_key = False
    old_link = ""

    for line in lines:
        parts = line.split("|")
        if len(parts) < 5:
            continue
        key, user, create_time, expire_time, saved_link = parts
        try:
            expire_ts = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S").timestamp()
        except:
            continue
        if expire_ts < current_time:
            continue
        if user == username:
            try:
                create_ts = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S").timestamp()
            except:
                create_ts = 0
            if (current_time - create_ts) < COOLDOWN:
                return {"status": "error", "message": f"Tạo key quá nhanh, chờ {COOLDOWN} giây!"}
            user_has_key = True
            old_link = saved_link
        new_data.append(line)

    if user_has_key:
        return {"status": "success", "link_get_key": old_link}

    random_str = hashlib.md5(str(random.random()).encode()).hexdigest()[:6]
    key = username + random_str

    domain = "http://anhcode.io.vn"  # THAY DOMAIN THẬT CỦA BẠN
    link_goc = f"{domain}/key/{key}"

    api1 = f"https://yeumoney.com/QL_api.php?token={YEUMONEY_TOKEN}&format=json&url={quote(link_goc)}"
    try:
        res1 = requests.get(api1, timeout=10).json()
        if res1.get("status") != "success":
            return {"status": "error", "message": "Lỗi YeuMoney"}
        link_yeumoney = res1["shortenedUrl"]
    except Exception as e:
        return {"status": "error", "message": f"Lỗi YeuMoney: {str(e)}"}

    api2 = f"https://link4m.co/api-shorten/v2?api={LINK4M_API}&url={quote(link_yeumoney)}"
    try:
        res2 = requests.get(api2, timeout=10).json()
        if "shortenedUrl" not in res2:
            return {"status": "error", "message": "Lỗi Link4m"}
        link_cuoi = res2["shortenedUrl"]
    except Exception as e:
        return {"status": "error", "message": f"Lỗi Link4m: {str(e)}"}

    create_time = now.strftime("%Y-%m-%d %H:%M:%S")
    expire_time = (now + timedelta(hours=KEY_HOURS)).strftime("%Y-%m-%d %H:%M:%S")

    new_data.append(f"{key}|{username}|{create_time}|{expire_time}|{link_cuoi}")
    with open(KEY_FILE, 'w') as f:
        f.write("\n".join(new_data) + "\n")

    return {"status": "success", "link_get_key": link_cuoi}

def check_key(username, input_key):
    if not os.path.exists(KEY_FILE):
        return {"status": "error", "message": "Chưa có key nào"}

    with open(KEY_FILE, 'r') as f:
        lines = f.read().splitlines()

    now_ts = datetime.now().timestamp()

    for line in lines:
        parts = line.split("|")
        if len(parts) < 5:
            continue
        key, user, create_time, expire_time, saved_link = parts
        if key != input_key:
            continue
        try:
            expire_ts = datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S").timestamp()
        except:
            continue
        if expire_ts < now_ts:
            return {"status": "error", "message": "Key đã hết hạn"}
        if user != username:
            return {"status": "error", "message": "Key không thuộc về bạn"}
        return {"status": "success", "message": "Key hợp lệ", "expire_time": expire_time}

    return {"status": "error", "message": "Key không tồn tại"}

# ================== BUFF TIKTOK HISTORY ==================
def load_buff_tiktok_history():
    if os.path.exists("buff_tiktok_history.json"):
        with open("buff_tiktok_history.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_buff_tiktok_history(data):
    with open("buff_tiktok_history.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_today_buff_tiktok(uid):
    history = load_buff_tiktok_history()
    today = str(date.today())
    return history.get(str(uid), {}).get(today, 0)

def increment_buff_tiktok(uid):
    history = load_buff_tiktok_history()
    today = str(date.today())
    uid_str = str(uid)
    if uid_str not in history:
        history[uid_str] = {}
    history[uid_str][today] = history[uid_str].get(today, 0) + 1
    save_buff_tiktok_history(history)

# ================== USERS JSON ==================
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def get_user(uid):
    users = load_users()
    key = str(uid)
    if key not in users:
        users[key] = {"balance": 0, "total": 0, "last_recharge": 0, "level": "none", "history": []}
        save_users(users)
    user = users[key]
    if check_expire(user):
        save_users(users)
    return user

def update_user(uid, amount, tid):
    users = load_users()
    key = str(uid)
    user = users.get(key, {"balance": 0, "total": 0, "last_recharge": 0, "level": "none", "history": []})
    now = time.time()
    user['balance'] += amount
    user['total'] += amount
    user['last_recharge'] = now
    user['history'].append({"tid": tid, "amount": amount, "time": now})
    if user['total'] >= VIP_MIN:
        user['level'] = "vip"
    elif user['total'] >= NORMAL_MIN:
        user['level'] = "basic"
    else:
        user['level'] = "none"
    users[key] = user
    save_users(users)

def check_expire(user):
    if user['last_recharge'] == 0:
        expired = True
    else:
        expired = (time.time() - user['last_recharge']) > (EXPIRE_DAYS * 86400)
    if expired:
        user['level'] = "none"
        user['balance'] = 0
        return True
    return False

def is_valid_recharge(user):
    return user['last_recharge'] != 0 and (time.time() - user['last_recharge']) <= (EXPIRE_DAYS * 86400)

# ================== MENUS SIÊU XỊN ==================
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("💎 NẠP VIP"),
        types.KeyboardButton("🔥 CHECK BANK")
    )
    markup.add(
        types.KeyboardButton("📞 SPAM CALL"),
        types.KeyboardButton("❤️ BUFF TIKTOK")
    )
    markup.add(
        types.KeyboardButton("🔑 LẤY KEY"),
        types.KeyboardButton("👑 THÔNG TIN VIP")
    )
    markup.add(types.KeyboardButton("📖 HƯỚNG DẪN PRO"))
    return markup

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(m):
    text = (
        "🌟✨ **CHÀO MỪNG BOSS ĐẾN BOT SIÊU VIP PRO MAX 2026** ✨🌟\n\n"
        "💎 Spam Call Cực Mạnh - Buff Tim TikTok Siêu Xịn\n"
        "🔑 Lấy key siêu nhanh: /getkey hoặc nút 🔑 LẤY KEY\n"
        "✅ Check key: /check <key>\n"
        "❤️ Buff TikTok thoải mái theo level\n\n"
        "🚀 Chọn chức năng siêu sang bên dưới nhé boss! 🚀"
    )
    bot.reply_to(m, text, parse_mode="Markdown", reply_markup=main_menu())

# ================== HƯỚNG DẪN PRO ==================
@bot.message_handler(commands=["huongdan", "help"])
@bot.message_handler(func=lambda m: m.text == "📖 HƯỚNG DẪN PRO")
def huongdan(m):
    text = (
        "🔥 **HƯỚNG DẪN SIÊU VIP PRO MAX** 🔥\n"
        "═════════════════════════════════════\n\n"
        "💎 **NẠP TIỀN** → '💎 NẠP VIP' hoặc /bank\n\n"
        "📞 **SPAM CALL** → '📞 SPAM CALL'\n\n"
        "❤️ **BUFF TIKTOK** → '❤️ BUFF TIKTOK' + link\n\n"
        "🔑 **LẤY KEY** → /getkey hoặc nút 🔑 LẤY KEY\n"
        "   Mở link → copy key → paste chat → /check <key>\n\n"
        "👑 **THÔNG TIN** → Xem level, số dư\n\n"
        "⏳ Hạn sử dụng: 10 ngày từ nạp cuối"
    )
    bot.reply_to(m, text, parse_mode="Markdown", reply_markup=main_menu())

# ================== /getkey ==================
@bot.message_handler(commands=["getkey"])
@bot.message_handler(func=lambda m: m.text == "🔑 LẤY KEY")
def getkey_handler(m):
    uid = str(m.from_user.id)
    chat_id = m.chat.id

    loading = bot.send_message(chat_id, "🔑 **ĐANG TẠO KEY VIP CHO BOSS...** ✨")
    time.sleep(1.2)
    bot.edit_message_text("🌐 **KẾT NỐI HỆ THỐNG KEY SIÊU TỐC** 🌐", chat_id, loading.message_id)
    time.sleep(1.2)
    bot.edit_message_text("⚡ **ĐANG RÚT GỌN LINK VIP** ⚡", chat_id, loading.message_id)

    result = get_key(uid)

    if result["status"] == "success":
        link = result.get("link_get_key", "")
        bot.edit_message_text(
            f"🌟 **LINK LẤY KEY VIP CỦA BOSS** 🌟\n"
            f"{link}\n\n"
            f"1. Mở link trên\n"
            f"2. Copy KEY → paste vào chat bot\n"
            f"3. Gõ /check <key> để kiểm tra & kích hoạt\n"
            f"💎 Boss làm theo là buff TikTok thoải mái ngay!",
            chat_id, loading.message_id
        )
    else:
        bot.edit_message_text(f"❌ Lỗi: {result.get('message', 'Không rõ')}\nThử lại /getkey nhé boss!", chat_id, loading.message_id)

# ================== /check <key> ==================
@bot.message_handler(commands=["check"])
def check_key_handler(m):
    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(m, "❌ Cú pháp: `/check <key>`\nVí dụ: /check 7808122787efa464")
        return

    input_key = args[1].strip()
    uid = str(m.from_user.id)

    loading = bot.send_message(m.chat.id, "✅ **ĐANG CHECK KEY VIP...** 🔍")
    time.sleep(1.2)
    bot.edit_message_text("🔥 **KIỂM TRA KEY TRONG HỆ THỐNG...** 🔥", m.chat.id, loading.message_id)

    result = check_key(uid, input_key)

    if result["status"] == "success":
        bot.edit_message_text(
            f"🌟 **KEY HỢP LỆ - ĐÃ KÍCH HOẠT VIP!** 🌟\n"
            f"Key: `{input_key}`\n"
            f"Thuộc về boss ✓\n"
            f"Hết hạn: {result.get('expire_time', 'N/A')}\n\n"
            "🔥 Buff TikTok thoải mái ngay bây giờ! 💎",
            m.chat.id, loading.message_id, parse_mode="Markdown"
        )
    else:
        bot.edit_message_text(f"❌ {result.get('message', 'Key không hợp lệ')}\nLấy key mới bằng /getkey nhé boss!", m.chat.id, loading.message_id)

# ================== BUFF TIKTOK ==================
@bot.message_handler(commands=["bufftiktok"])
@bot.message_handler(func=lambda m: m.text == "❤️ BUFF TIKTOK")
def buff_tiktok_handler(m):
    if m.text == "❤️ BUFF TIKTOK":
        bot.reply_to(m, "✨ Gửi link video TikTok cần buff tim nhé!\nVí dụ: /bufftiktok https://www.tiktok.com/@user/video/123456789")
        return

    args = m.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(m, "❌ Gõ: `/bufftiktok <link>`", parse_mode="Markdown")
        return

    link = args[1].strip()
    if "tiktok.com" not in link:
        bot.reply_to(m, "❌ Link phải là video TikTok")
        return

    uid = m.from_user.id
    user = get_user(uid)
    level = user['level']

    daily_max = DAILY_BUFF_TT_VIP if level == "vip" else DAILY_BUFF_TT_BASIC if level == "basic" else DAILY_BUFF_TT_FREE
    today_count = get_today_buff_tiktok(uid)

    if today_count >= daily_max:
        bot.reply_to(m, f"💔 **Hết lượt buff hôm nay** ({today_count}/{daily_max})\nNgày mai quay lại nhé boss VIP!")
        return

    loading = bot.send_message(m.chat.id, "🔍")
    time.sleep(1.5)
    bot.edit_message_text("⚡ **KẾT NỐI SERVER BUFF VIP PRO** ⚡", m.chat.id, loading.message_id)
    time.sleep(1.2)
    bot.edit_message_text("🌟 **TIM ĐANG TĂNG VÈO VÈO...** 🌟", m.chat.id, loading.message_id)
    time.sleep(1.2)
    bot.edit_message_text("💎 **HOÀN TẤT BUFF - CHECK NGAY!** 💎", m.chat.id, loading.message_id)

    try:
        r = requests.get(API_BUFF, params={"buff": link}, timeout=30).json()
        if r.get("status") == "success":
            increment_buff_tiktok(uid)
            order_id = r.get("trang_thai", "N/A")
            success_text = (
                "🌟 **BUFF TIM TIKTOK THÀNH CÔNG SIÊU XỊN** 🌟\n"
                "═════════════════════════════════════\n"
                f"🎥 **Link video**: {link}\n"
                f"❤️ **Hôm nay**: {today_count + 1}/{daily_max}\n\n"
                "🔥 Tim tăng vèo vèo! Boss giàu like rồi 💎"
            )
            bot.edit_message_text(success_text, m.chat.id, loading.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text(f"❌ Buff fail: {r.get('message', 'Lỗi API')}", m.chat.id, loading.message_id)
    except Exception as e:
        bot.edit_message_text(f"⚠️ Lỗi kết nối: {str(e)}", m.chat.id, loading.message_id)

from urllib.parse import quote  # <-- quote là hàm, dùng trực tiếp
import threading
from datetime import datetime
import requests  # cần cho API_MB_HISTORY

            # Giả sử các global đã define ở đầu file:
            # user_state = {}               # dict lưu trạng thái user
            # checked_trans = set()         # set mã GD đã check
            # API_MB_HISTORY = "your_api_endpoint_here"  # ví dụ: "https://api.example.com/mb/history"
            # MB_CHECK_DELAY = 30           # giây delay check
            # update_user(uid, amount, tid) # hàm cập nhật VIP cho user
            # main_menu()                   # hàm trả về ReplyKeyboardMarkup chính

            # ================== NẠP VIP (tạo QR + lưu state) ==================
@bot.message_handler(func=lambda m: m.text in ["💎 NẠP VIP", "💳 Nạp Tiền"] or m.text.startswith("/bank"))
def nap_bank(m):
                chat_id = m.chat.id
                uid = m.from_user.id
                state_key = (chat_id, uid)

                # Rút gọn nội dung CK: b + 6 chữ số cuối uid (an toàn <= 7-8 ký tự)
                noidung = f"botcall{uid % 999999}"

                account_name = "KIEU VAN NHAT ANH"  # hoặc MB_NAME global

                # Tạo URL QR
                qr_url = (
                    f"https://img.vietqr.io/image/mbbank-0329270154-qr_only.jpg"
                    f"?accountName={quote(account_name)}"
                    f"&addInfo={quote(noidung)}"
                )

                # Lưu state chờ check
                user_state[state_key] = {
                    "type": "bank_wait",
                    "content": noidung,  # dùng để match description giao dịch
                    "timestamp": datetime.now().timestamp(),
                    "amount_expected": None  # nếu sau này muốn check amount cụ thể
                }

                # Inline keyboard HỢP LỆ (callback_data)
                markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                markup.add(
                    telebot.types.InlineKeyboardButton("🔄 Check ngay", callback_data=f"checkbank_{chat_id}_{uid}"),
                    telebot.types.InlineKeyboardButton("❌ Huỷ", callback_data=f"cancel_{chat_id}_{uid}")
                )

                try:
                    bot.send_photo(
                        chat_id,
                        photo=qr_url,
                        caption=(
                            f"💎 **NẠP VIP THỦ CÔNG**\n\n"
                            f"• Ngân hàng: MBBank\n"
                            f"• Số TK: `0329270154`\n"
                            f"• Chủ TK: {account_name}\n"
                            f"• Nội dung CK: <code>{noidung}</code>\n\n"
                            f"1. Quét QR hoặc chuyển khoản thủ công.\n"
                            f"2. Đảm bảo nội dung CK **chính xác** (copy-paste).\n"
                            f"3. Sau chuyển xong → nhấn **Check ngay** hoặc dùng /checkbank.\n"
                            f"Hệ thống tự động phát hiện & cộng VIP (thường 30-60s)."
                        ),
                        parse_mode="HTML",
                        reply_markup=markup
                    )
                except Exception as e:
                    bot.reply_to(m, f"❌ Lỗi tạo QR: {str(e)}\nThử lại sau hoặc liên hệ admin!")
                    print(f"QR send error: {e}")
                    user_state.pop(state_key, None)  # dọn state nếu lỗi

            # ================== CALLBACK QUERY (Check & Cancel) ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith(("cancel_", "checkbank_")))
def handle_inline(call):
                try:
                    parts = call.data.split("_")
                    if len(parts) != 3:
                        bot.answer_callback_query(call.id, "Dữ liệu không hợp lệ!", show_alert=True)
                        return

                    action, chat_id_str, uid_str = parts
                    chat_id = int(chat_id_str)
                    uid = int(uid_str)
                    state_key = (chat_id, uid)

                    if call.from_user.id != uid:
                        bot.answer_callback_query(call.id, "⛔ Không phải yêu cầu của bạn!", show_alert=True)
                        return

                    if state_key not in user_state:
                        bot.answer_callback_query(call.id, "Yêu cầu đã hết hạn hoặc huỷ!", show_alert=True)
                        return

                    state = user_state[state_key]

                    if action == "cancel":
                        user_state.pop(state_key, None)
                        bot.edit_message_caption(
                            caption="✅ **ĐÃ HUỶ YÊU CẦU NẠP VIP** thành công!",
                            chat_id=chat_id,
                            message_id=call.message.message_id,
                            reply_markup=None,
                            parse_mode="Markdown"
                        )
                        bot.answer_callback_query(call.id, "Huỷ OK!")

                    elif action == "checkbank":
                        if state.get("type") != "bank_wait":
                            bot.answer_callback_query(call.id, "Yêu cầu đã xử lý hoặc hết hạn!", show_alert=True)
                            return

                        bot.answer_callback_query(call.id, "Đang check...")

                        loading_msg = bot.send_message(
                            chat_id,
                            "🔄 **ĐANG KIỂM TRA GIAO DỊCH BANK...**\nChờ ~30 giây nhé boss! 🚀",
                            parse_mode="Markdown"
                        )

                        threading.Timer(
                            MB_CHECK_DELAY,
                            lambda: check_bank_after_delay(state_key, chat_id, loading_msg.message_id)
                        ).start()

                except Exception as e:
                    bot.answer_callback_query(call.id, f"Lỗi: {str(e)}", show_alert=True)
                    print(f"Callback error: {e}")

            # ================== CHECK BANK TỪ MENU / LỆNH ==================
@bot.message_handler(func=lambda m: m.text in ["🔥 CHECK BANK", "/checkbank"])
def checkbank(m):
                chat_id = m.chat.id
                uid = m.from_user.id
                state_key = (chat_id, uid)

                if state_key not in user_state or user_state[state_key].get("type") != "bank_wait":
                    bot.reply_to(m, "⚠️ Không có yêu cầu nạp đang chờ.\nDùng 💎 NẠP VIP để tạo mới!")
                    return

                loading_msg = bot.reply_to(
                    m,
                    "🔄 **ĐANG CHECK GIAO DỊCH VIP...**\nChờ chút nhé! 💎",
                    parse_mode="Markdown"
                )

                threading.Timer(
                    MB_CHECK_DELAY,
                    lambda: check_bank_after_delay(state_key, chat_id, loading_msg.message_id)
                ).start()

            # ================== HÀM CHECK CHUNG ==================
def check_bank_after_delay(state_key, chat_id, msg_id):
                if state_key not in user_state:
                    try:
                        bot.edit_message_text("⚠️ Yêu cầu đã hết hạn.", chat_id, msg_id, parse_mode="Markdown")
                    except:
                        pass
                    return

                state = user_state.get(state_key, {})
                if state.get("type") != "bank_wait":
                    try:
                        bot.edit_message_text("⚠️ Yêu cầu đã xử lý.", chat_id, msg_id, parse_mode="Markdown")
                    except:
                        pass
                    return

                try:
                    resp = requests.get(API_MB_HISTORY, timeout=40)
                    resp.raise_for_status()
                    data = resp.json()

                    found = False
                    content_lower = state["content"].lower()

                    for tx in data.get("transactions", []):
                        if tx.get("type") != "IN":
                            continue
                        tid = tx.get("transactionID")
                        if not tid or tid in checked_trans:
                            continue
                        amount = int(tx.get("amount", 0))
                        desc = (tx.get("description") or "").lower()

                        if content_lower in desc:
                            checked_trans.add(tid)
                            user_state.pop(state_key, None)

                            uid = state_key[1]
                            update_user(uid, amount, tid)

                            success_text = (
                                "🎉 **NẠP VIP THÀNH CÔNG!** 🎉\n"
                                "═══════════════════════\n"
                                f"💰 Số tiền: +{amount:,} VNĐ\n"
                                f"🧾 Mã GD: `{tid}`\n"
                                f"⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                                "🔥 Boss lên VIP rồi – Buff thoải mái nhé!"
                            )
                            bot.edit_message_text(success_text, chat_id, msg_id, parse_mode="Markdown")
                            found = True
                            break

                    if not found:
                        bot.edit_message_text(
                            "❌ **Chưa thấy GD phù hợp.**\n"
                            "→ Kiểm tra nội dung CK có đúng không.\n"
                            "→ Chờ thêm 1-2 phút rồi /checkbank lại.\n"
                            "→ Hoặc thử chuyển khoản mới.",
                            chat_id, msg_id, parse_mode="Markdown"
                        )

                except requests.RequestException as e:
                    bot.edit_message_text(f"⚠️ Lỗi kết nối API: {str(e)}", chat_id, msg_id, parse_mode="Markdown")
                except Exception as e:
                    bot.edit_message_text(f"⚠️ Lỗi check: {str(e)}", chat_id, msg_id, parse_mode="Markdown")
                    print(f"Check error: {e}")
                finally:
                    user_state.pop(state_key, None)  # luôn dọn state
# ================== THÔNG TIN VIP ==================
@bot.message_handler(commands=["thongtin"])
@bot.message_handler(func=lambda m: m.text == "👑 THÔNG TIN VIP")
def thongtin(m):
    uid = m.from_user.id
    user = get_user(uid)
    level_emoji = {"vip": "💎 VIP PRO MAX", "basic": "🌟 BASIC VIP", "none": "🔒 FREE"}.get(user['level'], "❓")
    last_time = "Chưa nạp" if user['last_recharge'] == 0 else datetime.fromtimestamp(user['last_recharge']).strftime("%d/%m/%Y %H:%M")
    text = (
        "👑 **THÔNG TIN TÀI KHOẢN VIP PRO 2026** 👑\n"
        "═════════════════════════════════════\n"
        f"🆔 **ID**: <code>{uid}</code>\n"
        f"💰 **Số dư**: {user['balance']:,} VNĐ\n"
        f"🏆 **Tổng nạp**: {user['total']:,} VNĐ\n"
        f"🌟 **Gói**: {level_emoji}\n"
        f"⏳ **Nạp gần nhất**: {last_time}\n\n"
    )
    bot.reply_to(m, text, parse_mode="HTML", reply_markup=main_menu())

# ================== HỦY SPAM ==================
@bot.message_handler(commands=["huycall"])
def huycall(m):
    chat_id = m.chat.id
    uid = m.from_user.id
    key = (chat_id, uid)
    if key not in active_spam_processes:
        bot.reply_to(m, "⚠️ Không có lệnh spam call nào đang chạy.")
        return
    proc = active_spam_processes.get(key)
    if not proc or not psutil.pid_exists(proc.pid):
        if key in active_spam_processes:
            del active_spam_processes[key]
        bot.reply_to(m, "✅ Không còn process spam nào đang chạy.")
        return
    try:
        parent = psutil.Process(proc.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        del active_spam_processes[key]
        bot.reply_to(m, "🛑 **ĐÃ DỪNG TOÀN BỘ SPAM CALL THÀNH CÔNG!**\nBoss yên tâm nhé! 🔥")
    except Exception as e:
        bot.reply_to(m, f"⚠️ Lỗi dừng: {str(e)}\nThử lại hoặc restart bot.")

# ================== SPAM CALL THƯỜNG ==================
@bot.message_handler(commands=["spamcall"])
def spamcall(m):
    args = m.text.split()
    if len(args) != 3:
        bot.reply_to(m, "❌ **Cú pháp**: `/spamcall 09xxxxxxxx 5`", parse_mode="Markdown")
        return

    phone = args[1]
    try:
        times = int(args[2])
    except:
        bot.reply_to(m, "❌ Số lần phải là số nguyên!")
        return

    if not phone.isdigit() or len(phone) != 10:
        bot.reply_to(m, "❌ SĐT phải đúng 10 số (bắt đầu 09/03/...)")
        return

    uid = m.from_user.id
    user = get_user(uid)
    if not is_valid_recharge(user):
        bot.reply_to(m, "⏰ **Gói đã hết hạn** → Nạp lại để spam tiếp!")
        return
    if user['level'] not in ["basic", "vip"]:
        bot.reply_to(m, "🔒 Cần nạp ít nhất **5.000đ** để dùng spam thường")
        return

    search_msg = bot.send_message(m.chat.id, "🔍")
    time.sleep(1.8)
    try:
        bot.delete_message(m.chat.id, search_msg.message_id)
    except:
        pass

    status_msg = bot.send_message(
        m.chat.id,
        "╭───────────────✦✧✦───────────────╮\n"
        " 🚀 **KHỞI ĐỘNG SPAM CALL THƯỜNG** \n"
        "╰───────────────✦✧✦───────────────╯",
        parse_mode="Markdown"
    )
    time.sleep(1.4)
    bot.edit_message_text(
        "╭───────────────✦✧✦───────────────╮\n"
        " 📡 **KẾT NỐI SERVER VIP** \n"
        "╰───────────────✦✧✦───────────────╯",
        m.chat.id, status_msg.message_id
    )
    time.sleep(1.3)

    proc = subprocess.Popen(["python", "spamcall.py", phone, str(times)])
    active_spam_processes[(m.chat.id, m.from_user.id)] = proc

    result = (
        "╔════════════════════════════════════════╗\n"
        "║ 📞 **SPAM CALL THƯỜNG - ĐANG CHẠY** ║\n"
        "╠════════════════════════════════════════╣\n"
        f"║ 📱 **SĐT**: `{phone}` ║\n"
        f"║ 🔄 **Số lần**: {times} ║\n"
        "║ 💎 **Gói**: BASIC ║\n"
        "║ ⚡ **Trạng thái**: Gọi rầm rộ... ║\n"
        "╚════════════════════════════════════════╝\n\n"
        "• Dừng khẩn: /huycall"
    )
    bot.edit_message_text(result, m.chat.id, status_msg.message_id, parse_mode="Markdown")

# ================== SPAM CALL VIP ==================
@bot.message_handler(commands=["spamcallvip"])
def spamcallvip(m):
    args = m.text.split()
    if len(args) != 3:
        bot.reply_to(m, "❌ **Cú pháp**: `/spamcallvip 09xxxxxxxx 10`", parse_mode="Markdown")
        return

    phone = args[1]
    try:
        times = int(args[2])
    except:
        bot.reply_to(m, "❌ Số lần phải là số nguyên!")
        return

    if not phone.isdigit() or len(phone) != 10:
        bot.reply_to(m, "❌ SĐT phải đúng 10 số")
        return

    uid = m.from_user.id
    user = get_user(uid)
    if not is_valid_recharge(user):
        bot.reply_to(m, "⏰ **Gói VIP hết hạn** → Nạp lại ngay!")
        return
    if user['level'] != "vip":
        bot.reply_to(m, "💎 **Chỉ VIP mới dùng được**\n→ Nạp ≥ 20.000đ để mở khóa")
        return

    search_msg = bot.send_message(m.chat.id, "🔍")
    time.sleep(1.8)
    try:
        bot.delete_message(m.chat.id, search_msg.message_id)
    except:
        pass

    status_msg = bot.send_message(
        m.chat.id,
        "╭───────────────✦✧✦───────────────╮\n"
        " 🔥 **KÍCH HOẠT VIP MODE PRO** \n"
        "╰───────────────✦✧✦───────────────╯",
        parse_mode="Markdown"
    )
    time.sleep(1.5)
    bot.edit_message_text(
        "╭───────────────✦✧✦───────────────╮\n"
        " ⚡ **VIP SERVER ĐANG XỬ LÝ** \n"
        "╰───────────────✦✧✦───────────────╯",
        m.chat.id, status_msg.message_id
    )
    time.sleep(1.4)

    proc = subprocess.Popen(["python", "spamcall.py", phone, str(times)])
    active_spam_processes[(m.chat.id, m.from_user.id)] = proc

    result = (
        "╔════════════════════════════════════════╗\n"
        "║ 🔥 **VIP SPAM CALL PRO - ĐANG CHẠY** ║\n"
        "╠════════════════════════════════════════╣\n"
        f"║ 📱 **SĐT**: `{phone}` ║\n"
        f"║ 🔄 **Số lần**: {times} ║\n"
        "║ 💎 **Gói**: VIP PRO ║\n"
        "║ ⚡ **Trạng thái**: Gọi siêu tốc... ║\n"
        "╚════════════════════════════════════════╝\n\n"
        "• Dừng khẩn: /huycall"
    )
    bot.edit_message_text(result, m.chat.id, status_msg.message_id, parse_mode="Markdown")

# ================== RUN ==================
if __name__ == "__main__":
    print("🌟 BOT SIÊU VIP PRO MAX - FULL GIAO DIỆN ĐẸP XỊN 🌟")
    bot.infinity_polling(timeout=15, long_polling_timeout=5)