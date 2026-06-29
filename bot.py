import re
import requests
import telebot

# =======================================================
# CẤU HÌNH THÔNG TIN BOT VÀ API
# =======================================================

# Điền Token Bot Telegram của bạn
BOT_TOKEN = "8937782880:AAE6Gsxh_SeCG5nkoEQHCHyfsnTWJ14SoiM"
bot = telebot.TeleBot(BOT_TOKEN)

RAPIDAPI_KEY = "525e0b9934msha396ecf14d009c9p1dcadajsn39105b0e7627"
RAPIDAPI_HOST = "tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com"


# =======================================================
# HÀM BÓC TÁCH ID VÀ GỌI API CHUẨN JSON THỰC TẾ
# =======================================================
def extract_video_id(url):
    """Sử dụng Regex để bóc chuỗi số ID từ link TikTok dài."""
    match = re.search(r"video/(\d+)", url)
    if match:
        return match.group(1)
    return None


def get_tiktok_video(video_id):
    """Gọi lên API chính xác theo định dạng Path Params dựa trên ảnh thực tế."""
    # Định dạng API bắt buộc điền ID thẳng vào URL (Path Parameter)
    url = f"https://{RAPIDAPI_HOST}/video/{video_id}"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            res_json = response.json()

            # Đi sâu vào đúng các tầng dữ liệu của JSON thực tế bạn gửi
            data_block = res_json.get("data", {})
            aweme_detail = data_block.get("aweme_detail", {})

            # 1. Lấy tiêu đề bài đăng (Trường 'desc')
            caption = aweme_detail.get(
                "desc", "Chúc bạn xem video vui vẻ! 🎬"
            )

            # 2. Đi vào object 'video' -> 'play_addr' -> 'url_list'
            video_block = aweme_detail.get("video", {})
            play_addr = video_block.get("play_addr", {})
            url_list = play_addr.get("url_list", [])

            # Lấy đường link video đầu tiên trong danh sách
            if url_list:
                video_url = url_list[0]
                return video_url, caption

    except Exception as e:
        print(f"[-] Lỗi kết nối API: {e}")

    return None, None


# =======================================================
# LOGIC ĐIỀU KHIỂN BOT TELEGRAM
# =======================================================


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    welcome_text = (
        "👋 Xin chào Nam! Tôi là Bot tải video TikTok.\n\n"
        "👉 Hãy gửi một đường link video TikTok bất kỳ (chuẩn máy tính), "
        "tôi sẽ xử lý và tải video về cho bạn!"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(
    func=lambda message: "tiktok.com" in message.text.lower()
    or message.text.startswith("http")
)
def handle_message(message):
    tiktok_url = message.text.strip()

    status_msg = bot.reply_to(
        message, "⏳ Đang bóc tách dữ liệu video, bạn chờ một chút nhé..."
    )

    # Bước 1: Trích xuất ID từ link người dùng gửi
    video_id = extract_video_id(tiktok_url)

    if not video_id:
        bot.edit_message_text(
            "❌ Link không đúng định dạng. Hiện tại hệ thống chỉ hỗ trợ link đầy đủ dạng máy tính (có chứa /video/ID).",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
        )
        return

    print(f"[+] Tìm thấy ID: {video_id}. Tiến hành gọi API...")

    # Bước 2: Gọi API lấy link tải trực tiếp
    video_link, caption = get_tiktok_video(video_id)

    # Bước 3: Gửi trả video cho User
    if video_link:
        try:
            bot.edit_message_text(
                "🚀 Tìm thấy video! Đang tải và gửi lên Telegram...",
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
            )

            bot.send_video(
                chat_id=message.chat.id, video=video_link, caption=caption
            )

            bot.delete_message(message.chat.id, status_msg.message_id)
            print("[+] Gửi video thành công!")

        except Exception as e:
            bot.edit_message_text(
                f"❌ Lỗi gửi file: {e}",
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
            )
    else:
        bot.edit_message_text(
            "💥 Không thể lấy được video từ API này. Vui lòng kiểm tra lại trạng thái gói cước trên RapidAPI.",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
        )


if __name__ == "__main__":
    print("[*] Telegram Bot đang lắng nghe tin nhắn...")
    bot.infinity_polling()