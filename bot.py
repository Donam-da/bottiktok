import re
import requests
import telebot

# =======================================================
# CẤU HÌNH THÔNG TIN BOT VÀ TOKEN CHUNG
# =======================================================
BOT_TOKEN = "8937782880:AAE6Gsxh_SeCG5nkoEQHCHyfsnTWJ14SoiM"
bot = telebot.TeleBot(BOT_TOKEN)

# Key tài khoản RapidAPI dùng chung của bạn
RAPIDAPI_KEY = "525e0b9934msha396ecf14d009c9p1dcadajsn39105b0e7627"


# =======================================================
# LÕI CÁC HÀM GỌI API (MỖI HÀM LÀ 1 MÁY CHỦ DỰ PHÒNG)
# =======================================================

def call_api_1_scrapper(tiktok_url):
    """Máy chủ 1: TikTok Scrapper (Yêu cầu trích xuất ID)"""
    # Trích xuất ID từ link dài
    match = re.search(r"video/(\d+)", tiktok_url)
    video_id = match.group(1) if match else None
    if not video_id:
        return None, None
        
    host = "tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com"
    url = f"https://{host}/video/{video_id}"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            data_block = res_json.get('data', {})
            aweme_detail = data_block.get('aweme_detail', {})
            caption = aweme_detail.get('desc', '')
            url_list = aweme_detail.get('video', {}).get('play_addr', {}).get('url_list', [])
            if url_list:
                print("[+] API 1 bóc link thành công!")
                return url_list[0], caption
    except Exception as e:
        print(f"[-] API 1 gặp sự cố: {e}")
    return None, None


def call_api_2_social_media(tiktok_url):
    """Máy chủ 2: Social Media Video Downloader (Truyền thẳng link)"""
    host = "social-media-video-downloader.p.rapidapi.com"
    url = f"https://{host}/tiktok/v3/post/details"
    querystring = {"url": tiktok_url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            contents = res_json.get('contents', [])
            if contents:
                videos = contents[0].get('videos', [])
                if videos:
                    video_url = videos[0].get('url')
                    print("[+] API 2 bóc link thành công!")
                    return video_url, "Video tải từ Máy chủ dự phòng 2 🚀"
    except Exception as e:
        print(f"[-] API 2 gặp sự cố: {e}")
    return None, None


def call_api_3_tiktok_api23(tiktok_url):
    """Máy chủ 3 (MỚI): Tiktok API (Đọc từ trường 'play' lớp ngoài cùng)"""
    host = "tiktok-api23.p.rapidapi.com"
    url = f"https://{host}/api/download/video"
    querystring = {"url": tiktok_url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            # Bóc chuẩn theo ảnh image_5d39ca.png của bạn
            video_url = res_json.get('play') 
            if video_url:
                print("[+] API 3 bóc link thành công!")
                return video_url, "Video tải từ Máy chủ dự phòng 3 💎"
    except Exception as e:
        print(f"[-] API 3 gặp sự cố: {e}")
    return None, None


# =======================================================
# LOGIC ĐIỀU KHIỂN CHÍNH CỦA BOT TELEGRAM
# =======================================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Xin chào Nam! Hệ thống tải TikTok Đa Máy Chủ (3 Lõi Xoay Tua) đã sẵn sàng.\n\n"
                          "👉 Chỉ cần gửi link video vào đây, Bot sẽ tự động tìm máy chủ chạy tốt nhất để tải!")


@bot.message_handler(func=lambda message: "tiktok.com" in message.text.lower() or message.text.startswith('http'))
def handle_message(message):
    raw_url = message.text.strip()
    status_msg = bot.reply_to(message, "⏳ Đang kết nối máy chủ phân tích dữ liệu...")

    # Giải mã nhanh nếu là link rút gọn trên điện thoại
    if "vt.tiktok.com" in raw_url or "vm.tiktok.com" in raw_url:
        try:
            response = requests.head(raw_url, allow_redirects=True, timeout=6)
            raw_url = response.url
        except Exception:
            pass

    # DANH SÁCH CÁC MÁY CHỦ SẼ ĐƯỢC DUYỆT QUA
    api_servers = [
        {"name": "Máy chủ Chính (API 1)", "func": call_api_1_scrapper},
        {"name": "Máy chủ Dự phòng 2 (API 2)", "func": call_api_2_social_media},
        {"name": "Máy chủ Dự phòng 3 (API 3)", "func": call_api_3_tiktok_api23}
    ]

    video_link, caption = None, None

    # Vòng lặp duyệt tự động qua từng máy chủ
    for index, server in enumerate(api_servers):
        print(f"[*] Đang thử thách qua: {server['name']}...")
        
        # Nếu đang ở server thứ 2 hoặc 3, cập nhật trạng thái trên Telegram cho người dùng biết
        if index > 0:
            try:
                bot.edit_message_text(f"⚡ Máy chủ trước bận, đang chuyển tiếp sang {server['name']}...", 
                                      chat_id=message.chat.id, message_id=status_msg.message_id)
            except Exception:
                pass

        # Gọi hàm API tương ứng
        video_link, caption = server["func"](raw_url)

        # Nếu lấy được link thành công thì dừng vòng lặp (break) ngay lập tức
        if video_link:
            print(f"[+] Thành công tại {server['name']}. Tiến hành gửi file...")
            break

    # GỬI FILE VIDEO VỀ CHO USER
    if video_link:
        try:
            bot.edit_message_text("🚀 Đang gửi file video không logo về Telegram...", chat_id=message.chat.id, message_id=status_msg.message_id)
            bot.send_video(chat_id=message.chat.id, video=video_link, caption=caption if caption else "🎬")
            bot.delete_message(message.chat.id, status_msg.message_id)
            print("[+] Đã gửi thành công video!")
        except Exception as e:
            bot.edit_message_text(f"❌ Lỗi khi tải video lên Telegram: {e}", chat_id=message.chat.id, message_id=status_msg.message_id)
    else:
        bot.edit_message_text("💥 Toàn bộ hệ thống 3 máy chủ đều không bóc được link này hoặc đã hết quota tháng. Vui lòng thử lại sau!", 
                              chat_id=message.chat.id, message_id=status_msg.message_id)


if __name__ == "__main__":
    print("[*] Bot Telegram Tải TikTok 3 Máy Chủ Xoay Tua Đang Chạy...")
    bot.infinity_polling()