# TikTok & Facebook Video Downloader Bot - Telegram

Bot Telegram tải video TikTok và Facebook không logo với nhiều máy chủ xoay tua để đảm bảo độ ổn định cao.

## Tính năng

- Tải video TikTok không logo (5 máy chủ API xoay tua)
- Tải video Facebook (reels, video, story) - 5 máy chủ API
- Tải video YouTube (đang phát triển)
- Progress bar mượt mà từ 0-100%
- Hỗ trợ link điện thoại và máy tính
- Kiểm tra link hợp lệ tự động
- Giới hạn sử dụng theo user (tích hợp với bot thông báo)
- Kiểm tra blacklist từ bot thông báo

## Giới hạn sử dụng

**User đã có pass bot thông báo:**
- TikTok: 3 video/ngày
- Facebook: 2 video/ngày

**User lạ / Public mode:**
- TikTok: 1 video/ngày
- Facebook: 1 video/ngày

**Admin:** Không giới hạn

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

3. Chỉnh sửa `.env` với thông tin của bạn:
```
BOT_TOKEN=your_bot_token
RAPIDAPI_KEY=your_rapidapi_key
GITHUB_TOKEN=your_github_token
GIST_ID=your_gist_id
```

4. Chạy bot:
```bash
python bottiktok.py
```

## Deploy lên Render (Chạy 24/7 với Webhook)

### Bước 1: Chuẩn bị GitHub

1. Tạo repository mới trên GitHub
2. Upload toàn bộ file dự án (trừ file `.env` - KHÔNG push file này)
3. Đảm bảo các file sau đã được push:
   - `bottiktok.py`
   - `requirements.txt`
   - `Procfile`
   - `.gitignore`
   - `.env.example`

### Bước 2: Tạo Web Service trên Render

1. Đăng nhập vào [render.com](https://render.com)
2. Click **New +** → **Web Service**
3. Kết nối GitHub repository của bạn
4. Chọn repository TikTok bot

### Bước 3: Cấu hình Web Service

**Name:** Đặt tên cho service (ví dụ: `tiktok-facebook-bot`)

**Region:** Chọn region gần bạn nhất (Singapore hoặc Frankfurt)

**Branch:** `main` hoặc `master`

**Runtime:** Python 3

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn bottiktok:app
```

**Environment Variables (QUAN TRỌNG):**

Click vào "Advanced" → "Add Environment Variable" và thêm các biến sau:

| Variable | Value | Bắt buộc |
|----------|-------|----------|
| `BOT_TOKEN` | Token bot Telegram của bạn | ✅ Có |
| `RAPIDAPI_KEY` | RapidAPI key của bạn | ✅ Có |
| `GITHUB_TOKEN` | GitHub personal access token | ✅ Có |
| `GIST_ID` | ID của Gist chứa dữ liệu user | ✅ Có |
| `PORT` | `5000` | ✅ Có (Render tự thêm) |

**Lưu ý quan trọng:**
- `GITHUB_TOKEN` cần có quyền read gist
- `GIST_ID` là phần cuối URL gist: `https://gist.github.com/username/GIST_ID`
- Render sẽ tự động thêm biến `RENDER_EXTERNAL_URL`

**Instance Type:**
- **Free** (khuyên dùng cho test): Có thể sleep sau 15 phút không hoạt động
- **Starter ($7/tháng)**: Luôn active, performance tốt hơn

### Bước 4: Deploy

1. Click **Create Web Service** ở cuối trang
2. Render sẽ tự động build và deploy
3. Chờ 2-5 phút để deployment hoàn tất
4. Bot sẽ tự động set webhook và chạy 24/7 trên Render

### Bước 5: Kiểm tra và Verify

1. Vào tab **Logs** trên Render để xem log của bot
2. Tìm dòng: `[*] Bot Telegram Tải TikTok 5 Máy Chủ Xoay Tua Đang Hoạt Động...`
3. Tìm dòng: `[*] Setting webhook: https://your-app.onrender.com/webhook`
4. Test bot trên Telegram với lệnh `/start`
5. Bot nên phản hồi với thông tin giới hạn

### Bước 6: Keep-alive (nếu dùng Free tier)

Free tier sẽ sleep sau 15 phút không có request. Để giữ bot luôn active:

**Cách 1: Dùng UptimeRobot (miễn phí)**
1. Đăng ký [uptimerobot.com](https://uptimerobot.com)
2. Tạo new monitor
3. Type: HTTPS
4. URL: `https://your-app.onrender.com/health`
5. Interval: 5 minutes
6. Save

**Cách 2: Dùng paid tier ($7/tháng)**
- Upgrade lên Starter tier trong Render dashboard
- Bot sẽ luôn active 24/7

## Lưu ý quan trọng

### Webhook vs Polling
- **Render**: Bot tự động dùng webhook (tiết kiệm tài nguyên, phản hồi nhanh)
- **Local**: Bot dùng polling (tiện cho dev)
- Bot tự động chuyển mode dựa trên biến `RENDER_EXTERNAL_URL`

### Environment Variables
- KHÔNG bao giờ push file `.env` lên GitHub
- Luôn dùng Environment Variables trên Render cho sensitive data
- Token và API key được bảo mật trên Render

### Giới hạn Free tier
- Sleep sau 15 phút không hoạt động
- Cần ~30s để wake up khi có request mới
- 750 giờ/tháng (đủ cho 1 service chạy 24/7)
- RAM: 512MB, CPU: 0.1 vCPU

### Tích hợp với bot thông báo
- Bot TikTok đọc danh sách user có quyền từ Gist của bot thông báo
- Gist được sync tự động khi có thay đổi trong bot thông báo
- Files cần có trong Gist:
  - `notification_allowed_users.json` (danh sách user có pass)
  - `notification_public_mode.json` (trạng thái public mode)
  - `notification_public_users.json` (danh sách user public)
  - `notification_blocklist.json` (danh sách user bị block)

## Troubleshooting

### Bot không phản hồi

**Kiểm tra:**
1. Vào tab **Logs** trên Render
2. Tìm lỗi trong log (dòng có `[-]` hoặc `Error`)
3. Đảm bảo Environment Variables được cấu hình đúng
4. Kiểm tra xem bot có đang sleep không (free tier)

**Common errors:**
- `[-] Thiếu GITHUB_TOKEN hoặc GIST_ID`: Thêm biến môi trường
- `[-] Lỗi tải Gist: 401`: GitHub token không có quyền read gist
- `[-] Lỗi khi tải video`: RapidAPI key hết hạn hoặc quota

### Lỗi deployment

**Build failed:**
1. Kiểm tra file `Procfile`: `web: gunicorn bottiktok:app`
2. Đảm bảo `requirements.txt` có đầy đủ dependencies
3. Xem log build để biết lỗi cụ thể

**Deployment failed:**
1. Kiểm tra Start Command: `gunicorn bottiktok:app`
2. Đảm bảo file `bottiktok.py` tồn tại
3. Kiểm tra syntax error trong code Python

### Webhook không hoạt động

**Symptoms:**
- Bot không nhận message
- Logs không hiển thị request

**Fix:**
1. Kiểm tra biến `RENDER_EXTERNAL_URL` có được thêm tự động không
2. Manual set webhook: vào Telegram BotFather → `/setwebhook`
3. URL: `https://your-app.onrender.com/webhook`

### Giới hạn không hoạt động

**Symptoms:**
- User vẫn tải vượt giới hạn
- Giới hạn hiển thị sai

**Fix:**
1. Kiểm tra Gist có được sync không
2. Đảm bảo các file JSON trong Gist đúng format
3. Restart service trên Render

## Cập nhật code

Khi thay đổi code:

1. Commit và push lên GitHub
2. Render sẽ tự động detect và redeploy
3. Chờ 2-5 phút để deployment hoàn tất
4. Kiểm tra tab **Events** để xem progress

## License

MIT
