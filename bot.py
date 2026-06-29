import re
import requests
import telebot

# =======================================================
# CẤU HÌNH THÔNG TIN BOT VÀ CÁC API KEYS
# =======================================================

BOT_TOKEN = "8937782880:AAE6Gsxh_SeCG5nkoEQHCHyfsnTWJ14SoiM"
bot = telebot.TeleBot(BOT_TOKEN)

# Key dùng chung của tài khoản RapidAPI của bạn
RAPIDAPI_KEY = "525e0b9934msha396ecf14d009c9p1dcadajsn39105b0e7627"


# =======================================================
# MÁY CHỦ 1: TikTok Scrapper (Con cũ đang chạy ngon)
# =======================================================
def extract_video_id(url):
    """Bóc chuỗi số ID từ link dài để cấp cho API 1."""
    match = re.search(r"video/(\d+)", url)
    return match.group(1) if match else None


def call_api_1_scrapper(video_id):
    host = "tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com"
    url = f"https://{host}/video/{video_id}"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host,
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200:
            res_json = response.json()
            data_block = res_json.get("data", {})
            aweme_detail = data_block.get("aweme_detail", {})

            caption = aweme_detail.get("desc", "")
            url_list = aweme_detail.get("video", {}).get("play_addr", {}).get(
                "url_list", []
            )

            if url_list:
                return url_list[0], caption
    except Exception as e:
        print(f"[-] API 1 (Scrapper) gặp sự cố: {e}")
    return None, None


# =======================================================
# MÁY CHỦ 2 (MỚI THÊM): Social Media Video Downloader
# =======================================================
def call_api_2_social_media(tiktok_url):
    """Gọi con API mới tích hợp, truyền thẳng nguyên link gốc."""
    host = "social-media-video-downloader.p.rapidapi.com"
    url = f"https://{host}/tiktok/v3/post/details"

    querystring = {"url": tiktok_url}
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": host}

    try:
        response = requests.get(
            url, headers=headers, params=querystring, timeout=12
        )
        if response.status_code == 200:
            res_json = response.json()

            # Bóc tách chuẩn cấu trúc JSON tầng lớp trong ảnh image_5ccd84.png của bạn
            contents = res_json.get("contents", [])
            if contents:
                first_content = contents[0]
                videos = first_content.get("videos", [])
                if videos:
                    # Lấy phần tử video đầu tiên (thường là bản 540p hoặc HD)
                    video_url = videos[0].get("url")
                    caption = "Video tải từ máy chủ dự phòng 🚀"
                    return video_url, caption
    except Exception as e:
        print(f"[-] API 2 (Social Media) gặp sự cố: {e}")
    return None, None


# =======================================================
# LOGIC ĐIỀU KHIỂN BOT TELEGRAM
# =======================================================


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Xin chào Nam! Tôi là Bot tải video TikTok phiên bản nâng cấp có máy chủ dự phòng xoay tua.\n\n"
        "👉 Hãy gửi link video TikTok vào đây, tôi sẽ lo phần còn lại!",
    )


@bot.message_handler(
    func=lambda message: "tiktok.com" in message.text.lower()
    or message.text.startswith("http")
)
def handle_message(message):
    raw_url = message.text.strip()
    status_msg = bot.reply_to(
        message, "⏳ Đang bóc tách dữ liệu video, bạn chờ một chút nhé..."
    )

    # Tự động giải mã nếu người dùng gửi link rút gọn trên điện thoại
    if "vt.tiktok.com" in raw_url or "vm.tiktok.com" in raw_url:
        try:
            response = requests.head(raw_url, allow_redirects=True, timeout=8)
            raw_url = response.url
        except Exception:
            pass

    video_link, caption = None, None

    # ──── [BƯỚC 1]: THỬ CHẠY MÁY CHỦ 1 ────
    video_id = extract_video_id(raw_url)
    if video_id:
        print(f"[+] Thử tải qua API 1 (ID: {video_id})...")
        video_link, caption = call_api_1_scrapper(video_id)

    # ──── [BƯỚC 2]: XOAY TUA SANG MÁY CHỦ 2 NẾU MÁY CHỦ 1 LỖI ────
    if not video_link:
        print("[-] API 1 thất bại! Tự động xoay tua sang API 2...")
        bot.edit_message_text(
            "⚡ Máy chủ chính bận, đang chuyển sang máy chủ dự phòng...",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
        )
        video_link, caption = call_api_2_social_media(raw_url)

    # ──── [BƯỚC 3]: GỬI TRẢ KẾT QUẢ CHO USER ────
    if video_link:
        try:
            bot.edit_message_text(
                "🚀 Đang gửi video lên Telegram...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
            )
            bot.send_video(
                chat_id=message.chat.id,
                video=video_link,
                caption=caption if caption else "🎬",
            )
            bot.delete_message(message.chat.id, status_msg.message_id)
            print("[+] Hoàn tất gửi video thành công!")
        except Exception as e:
            bot.edit_message_text(
                f"❌ Lỗi gửi file lên Telegram: {e}",
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
            )
    else:
        bot.edit_message_text(
            "💥 Tất cả máy chủ (chính và dự phòng) đều không phản hồi link này. Vui lòng kiểm tra lại link hoặc thử lại sau!",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
        )


if __name__ == "__main__":
    print("[*] Telegram Bot ĐA MÁY CHỦ đang hoạt động...")
    bot.infinity_polling()