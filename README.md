# TikTok Video Downloader Bot - Telegram

Bot Telegram tải video TikTok không logo với 5 máy chủ xoay tua để đảm bảo độ ổn định cao.

## Tính năng

- Tải video TikTok không logo
- 5 máy chủ API xoay tua tự động
- Progress bar mượt mà từ 0-100%
- Hỗ trợ link điện thoại và máy tính
- Kiểm tra link hợp lệ tự động

## Cấu trúc dự án

```
.
├── bottiktok.py          # File chính của bot
├── requirements.txt      # Dependencies Python
├── Procfile             # Cấu hình Render
├── .env.example         # Mẫu biến môi trường
├── .gitignore           # File bỏ qua khi git
└── README.md            # Hướng dẫn
```

## Cài đặt local

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

3. Chạy bot:
```bash
python bottiktok.py
```

## Deploy lên Render (Chạy 24/7 với Webhook)

### Bước 1: Chuẩn bị GitHub

1. Tạo repository mới trên GitHub
2. Upload toàn bộ file dự án (trừ file `.env` nếu có)
3. Đảm bảo các file sau đã được push:
   - `bottiktok.py`
   - `requirements.txt`
   - `Procfile`
   - `.gitignore`

### Bước 2: Tạo Web Service trên Render

1. Đăng nhập vào [render.com](https://render.com)
2. Click **New +** → **Web Service**
3. Kết nối GitHub repository của bạn
4. Chọn repository TikTok bot

### Bước 3: Cấu hình Web Service

**Build & Deploy:**
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn bottiktok:app`

**Environment Variables:**
Thêm các biến môi trường sau:
- `BOT_TOKEN`: Token bot Telegram của bạn
- `RAPIDAPI_KEY`: RapidAPI key của bạn
- `GITHUB_TOKEN`: GitHub token (để đọc Gist)
- `GIST_ID`: ID của Gist chứa danh sách user
- `RENDER_EXTERNAL_URL`: URL của Render service (Render tự động thêm)

**Instance Type:**
- Chọn **Free** (hoặc paid nếu cần performance cao hơn)

### Bước 4: Deploy

1. Click **Create Web Service**
2. Render sẽ tự động build và deploy
3. Chờ vài phút để deployment hoàn tất
4. Bot sẽ tự động set webhook và chạy 24/7 trên Render

### Bước 5: Kiểm tra

1. Vào tab **Logs** trên Render để xem log của bot
2. Test bot trên Telegram
3. Bot sẽ phản hồi như khi chạy local
4. Webhook sẽ tự động được cấu hình khi deploy

## Lưu ý quan trọng

- **Webhook mode**: Bot sử dụng webhook khi deploy lên Render, giúp tiết kiệm tài nguyên và phản hồi nhanh hơn
- **Free tier** trên Render sẽ sleep sau 15 phút không hoạt động và cần ~30s để wake up
- Để bot luôn active, có thể:
  - Sử dụng paid tier ($7/tháng)
  - Hoặc dùng service keep-alive (uptimerobot.com) để ping định kỳ endpoint `/health`
- Token và API key được lưu trong Environment Variables trên Render, không cần file `.env`
- Bot tự động chuyển giữa webhook (Render) và polling (local) dựa trên biến môi trường `RENDER_EXTERNAL_URL`

## Troubleshooting

**Bot không phản hồi:**
- Kiểm tra Logs trên Render
- Đảm bảo Environment Variables được cấu hình đúng
- Kiểm tra xem bot có đang sleep không (free tier)

**Lỗi deployment:**
- Kiểm tra file `Procfile` có đúng không
- Đảm bảo `requirements.txt` có đầy đủ dependencies
- Xem log build để biết lỗi cụ thể

## License

MIT
