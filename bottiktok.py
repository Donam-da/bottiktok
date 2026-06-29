import re
import requests
import telebot
import threading
import time
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# =======================================================
# CẤU HÌNH THÔNG TIN BOT VÀ TOKEN CHUNG
# =======================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN không được tìm thấy trong biến môi trường!")
bot = telebot.TeleBot(BOT_TOKEN)

# Key tài khoản RapidAPI dùng chung của bạn
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY không được tìm thấy trong biến môi trường!")

# Biến toàn cầu để kiểm soát progress bar
progress_running = False


def progress_bar(chat_id, message_id):
    """Chạy progress bar từ 0% đến 100% từng số một"""
    global progress_running
    for i in range(101):
        if not progress_running:
            break
        try:
            bot.edit_message_text(f"Process: {i}%", chat_id=chat_id, message_id=message_id)
            time.sleep(0.05)  # Delay nhỏ để tạo hiệu ứng mượt
        except Exception:
            break


# =======================================================
# LÕI CÁC HÀM GỌI API (4 MÁY CHỦ XOAY TUA)
# =======================================================

def call_api_1_scrapper(tiktok_url):
    """Máy chủ 1: TikTok Scrapper (Yêu cầu trích xuất ID)"""
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
    """Máy chủ 3: Tiktok API (Đọc từ trường 'play' lớp ngoài cùng)"""
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
            video_url = res_json.get('play') 
            if video_url:
                print("[+] API 3 bóc link thành công!")
                return video_url, "Video tải từ Máy chủ dự phòng 3 💎"
    except Exception as e:
        print(f"[-] API 3 gặp sự cố: {e}")
    return None, None


def call_api_4_no_watermark2(tiktok_url):
    """Máy chủ 4 (MỚI): Tiktok Video No Watermark (Đọc từ data.hdplay hoặc data.play)"""
    host = "tiktok-video-no-watermark2.p.rapidapi.com"
    url = f"https://{host}/"
    
    # Cấu hình tham số hd=1 giống như trên playground bạn test thành công
    querystring = {"url": tiktok_url, "hd": "1"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            data_block = res_json.get('data', {})
            
            # Ưu tiên bản HD chất lượng cao không logo theo cấu trúc hệ thống
            video_url = data_block.get('hdplay') or data_block.get('play')
            caption = data_block.get('title') or "Video tải từ Máy chủ dự phòng 4 🔥"
            
            if video_url:
                print("[+] API 4 bóc link không logo thành công!")
                return video_url, caption
    except Exception as e:
        print(f"[-] API 4 gặp sự cố: {e}")
    return None, None


def call_api_5_7scorp(tiktok_url):
    """Máy chủ 5: TikTok Downloader by 7scorp (Gói Free 400 req/tháng)"""
    host = "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
    
    # Endpoint số 2 chính xác của bạn
    url = f"https://{host}/vid/index" 
    
    querystring = {"url": tiktok_url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": host
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            
            # Bóc tách chuẩn theo Response body trên ảnh của bạn
            video_url = res_json.get('video')
            caption = res_json.get('title') or "Video tải từ Máy chủ dự phòng 5 ✨"
            
            if video_url:
                print("[+] API 5 (7scorp) bóc link thành công!")
                return video_url, caption
    except Exception as e:
        print(f"[-] API 5 gặp sự cố: {e}")
    return None, None


# =======================================================
# LOGIC ĐIỀU KHIỂN CHÍNH CỦA BOT TELEGRAM
# =======================================================

def is_valid_tiktok_url(url):
    """Kiểm tra xem link có phải là TikTok hợp lệ không"""
    tiktok_patterns = [
        r'https?://(www\.)?tiktok\.com/@[\w\.-]+/video/\d+',
        r'https?://(www\.)?tiktok\.com/t/[\w-]+',
        r'https?://(vm|vt)\.tiktok\.com/[\w-]+',
        r'https?://(www\.)?tiktok\.com/[\w\.-]+/video/\d+'
    ]
    for pattern in tiktok_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Xin chào Nam! Hệ thống tải TikTok Siêu Cấp đã sẵn sàng.\n\n"
                          "👉 Gửi link video vào đây bot sẽ gửi bạn lại video không logo!")


@bot.message_handler(func=lambda message: message.text.startswith('http'))
def handle_message(message):
    raw_url = message.text.strip()
    
    # Kiểm tra link có phải TikTok hợp lệ không
    if not is_valid_tiktok_url(raw_url):
        error_message = (
            "❌ Link không hợp lệ! Vui lòng nhập lại link TikTok đúng.\n\n"
            "📱 **Mẫu link trên điện thoại:**\n"
            "• https://vm.tiktok.com/ZM6abc123/\n"
            "• https://vt.tiktok.com/ZM6abc123/\n\n"
            "💻 **Mẫu link trên máy tính:**\n"
            "• https://www.tiktok.com/@username/video/1234567890\n"
            "• https://tiktok.com/@username/video/1234567890\n\n"
            "👉 Hãy copy link từ TikTok và gửi lại cho bot!"
        )
        bot.reply_to(message, error_message)
        return
    
    status_msg = bot.reply_to(message, "Process: 0%")
    
    # Bắt đầu chạy progress bar trong thread riêng biệt
    global progress_running
    progress_running = True
    progress_thread = threading.Thread(target=progress_bar, args=(message.chat.id, status_msg.message_id))
    progress_thread.start()

    # Giải mã nhanh nếu là link rút gọn trên điện thoại (vt.tiktok hoặc vm.tiktok)
    if "vt.tiktok.com" in raw_url or "vm.tiktok.com" in raw_url:
        try:
            response = requests.head(raw_url, allow_redirects=True, timeout=6)
            raw_url = response.url
        except Exception:
            pass

    # DANH SÁCH MẠNG LƯỚI 5 MÁY CHỦ THEO THỨ TỰ XOAY TUA
    api_servers = [
        {"name": "Máy chủ Chính (API 1)", "func": call_api_1_scrapper},
        {"name": "Máy chủ Dự phòng 2 (API 2)", "func": call_api_2_social_media},
        {"name": "Máy chủ Dự phòng 3 (API 3)", "func": call_api_3_tiktok_api23},
        {"name": "Máy chủ Không Logo (API 4)", "func": call_api_4_no_watermark2},
        {"name": "Máy chủ 7scorp (API 5)", "func": call_api_5_7scorp}
    ]

    video_link, caption = None, None

    # Vòng lặp duyệt tự động qua từng máy chủ gánh lỗi cho nhau
    for index, server in enumerate(api_servers):
        print(f"[*] Đang thử thách qua: {server['name']}...")

        # Thực thi gọi hàm bóc tách link video
        video_link, caption = server["func"](raw_url)

        # Nếu lấy được link thành công, dừng ngay và không thử API khác
        if video_link:
            print(f"[+] Thành công tại {server['name']}.")
            break
        
        # Nếu API này fail, tiếp tục thử API tiếp theo
        print(f"[-] {server['name']} thất bại, chuyển sang máy chủ tiếp theo...")

    # TIẾN HÀNH GỬI TRẢ FILE VIDEO SẠCH CHO USER
    # Dừng progress bar
    progress_running = False
    
    if video_link:
        try:
            bot.edit_message_text("Process: 100%", chat_id=message.chat.id, message_id=status_msg.message_id)
            bot.send_video(chat_id=message.chat.id, video=video_link, caption=caption if caption else "🎬")
            bot.delete_message(message.chat.id, status_msg.message_id)
            print("[+] Đã gửi thành công video!")
        except Exception as e:
            bot.edit_message_text(f"❌ Lỗi khi tải video lên Telegram: {e}", chat_id=message.chat.id, message_id=status_msg.message_id)
    else:
        bot.edit_message_text("💥 Toàn bộ hệ thống 5 máy chủ đều không phản hồi link này hoặc cụm tài khoản đã cạn kiệt quota tháng. Hãy thử lại sau!", 
                              chat_id=message.chat.id, message_id=status_msg.message_id)


if __name__ == "__main__":
    print("[*] Bot Telegram Tải TikTok 5 Máy Chủ Xoay Tua Đang Hoạt Động...")
    bot.infinity_polling()