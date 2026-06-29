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

## Deploy lên Render (Chạy 24/7)

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
- **Start Command**: `python bottiktok.py`

**Environment Variables:**
Thêm các biến môi trường sau:
- `BOT_TOKEN`: Token bot Telegram của bạn (8937782880:AAE6Gsxh_SeCG5nkoEQHCHyfsnTWJ14SoiM)
- `RAPIDAPI_KEY`: RapidAPI key của bạn (525e0b9934msha396ecf14d009c9p1dcadajsn39105b0e7627)

**Instance Type:**
- Chọn **Free** (hoặc paid nếu cần performance cao hơn)

### Bước 4: Deploy

1. Click **Create Web Service**
2. Render sẽ tự động build và deploy
3. Chờ vài phút để deployment hoàn tất
4. Bot sẽ chạy 24/7 trên Render

### Bước 5: Kiểm tra

1. Vào tab **Logs** trên Render để xem log của bot
2. Test bot trên Telegram
3. Bot sẽ phản hồi như khi chạy local

## Lưu ý quan trọng

- **Free tier** trên Render sẽ sleep sau 15 phút không hoạt động và cần ~30s để wake up
- Để bot luôn active, có thể:
  - Sử dụng paid tier ($7/tháng)
  - Hoặc dùng service keep-alive (uptimerobot.com) để ping định kỳ
- Token và API key được lưu trong Environment Variables trên Render, không cần file `.env`

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
