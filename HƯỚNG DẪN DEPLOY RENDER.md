# HƯỚNG DẪN DEPLOY BOT TIKTOK LÊN RENDER 24/7

## Tổng quan
Bot TikTok của bạn sẽ chạy 24/7 trên Render với webhook, giúp tiết kiệm tài nguyên và phản hồi nhanh hơn.

---

## BƯỚC 1: CHUẨN BỊ CODE

### 1.1 Đảm bảo file cấu hình đã sẵn sàng
Các file cần thiết trong dự án:
- ✅ `bottiktok.py` - Code chính của bot (đã có webhook support)
- ✅ `requirements.txt` - Dependencies Python
- ✅ `Procfile` - Cấu hình Render
- ✅ `.gitignore` - Bỏ qua file nhạy cảm

### 1.2 Kiểm tra nội dung file

**requirements.txt:**
```
pyTelegramBotAPI==4.14.0
requests==2.31.0
python-dotenv==1.0.0
flask==3.0.0
gunicorn==21.2.0
```

**Procfile:**
```
web: gunicorn bottiktok:app
```

---

## BƯỚC 2: PUSH CODE LÊN GITHUB

### 2.1 Nếu chưa có GitHub repo
```bash
git init
git add .
git commit -m "Initial commit - TikTok bot with webhook support"
git branch -M main
git remote add origin https://github.com/Donam-da/bottiktok.git
git push -u origin main
```

### 2.2 Nếu đã có repo
```bash
git add .
git commit -m "Update webhook support for Render"
git push
```

---

## BƯỚC 3: TẠO WEB SERVICE TRÊN RENDER

### 3.1 Đăng nhập Render
- Truy cập: https://render.com
- Đăng nhập bằng GitHub

### 3.2 Tạo Web Service mới
1. Click **New +** → **Web Service**
2. Click **Connect** → Chọn repo `bottiktok`
3. Click **Connect** để kết nối

---

## BƯỚC 4: CẤU HÌNH WEB SERVICE

### 4.1 Name & Region
- **Name**: bottiktok (hoặc tên bạn muốn)
- **Region**: Singapore (nếu có) hoặc gần Việt Nam nhất

### 4.2 Build & Deploy
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn bottiktok:app`

### 4.3 Environment Variables (QUAN TRỌNG)
Click **Advanced** → **Add Environment Variable**

Thêm các biến sau:

| Biến | Giá trị | Mô tả |
|------|---------|-------|
| `BOT_TOKEN` | `8937782880:AAE6Gsxh_SeCG5nkoEQHCHyfsnTWJ14SoiM` | Token bot Telegram |
| `RAPIDAPI_KEY` | `525e0b9934msha396ecf14d009c9p1dcadajsn39105b0e7627` | RapidAPI key |
| `GITHUB_TOKEN` | `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` | GitHub token |
| `GIST_ID` | `815baee38593f02c389f56e3798d1f40` | ID Gist chứa danh sách user |

*Lưu ý: `RENDER_EXTERNAL_URL` sẽ được Render tự động thêm, không cần thêm thủ công*

### 4.4 Instance Type
- **Free** (miễn phí) - Bot sẽ sleep sau 15 phút không hoạt động
- **Starter ($7/tháng)** - Bot luôn active, không sleep

---

## BƯỚC 5: DEPLOY

1. Click **Create Web Service**
2. Render sẽ tự động:
   - Clone code từ GitHub
   - Cài đặt Python và dependencies
   - Khởi động gunicorn
   - Set webhook cho Telegram

3. Chờ 3-5 phút để deploy hoàn tất
4. Khi thấy "Your service is live 🎉" là xong

---

## BƯỚC 6: KIỂM TRA BOT

### 6.1 Kiểm tra trên Render
- Vào tab **Logs** để xem log của bot
- Nên thấy: `[*] Đang chạy trên Render: https://...`
- Nên thấy: `[*] Setting webhook: https://.../webhook`

### 6.2 Test trên Telegram
1. Mở bot trên Telegram
2. Gửi link TikTok hoặc Facebook
3. Bot nên phản hồi bình thường

---

## BƯỚC 7: GIỮ BOT AWAKE 24/7 (QUAN TRỌNG)

### 7.1 Nếu dùng Free Tier
Render sẽ sleep sau 15 phút không hoạt động. Để giữ bot awake:

**Cách 1: Dùng Uptimerobot**
1. Truy cập: https://uptimerobot.com
2. Đăng ký tài khoản miễn phí
3. Click **Add New Monitor**
4. **Monitor Type**: HTTP(s)
5. **URL**: `https://bottiktok-1-jaue.onrender.com/health`
6. **Monitoring Interval**: 5 minutes
7. Click **Create Monitor**

**Cách 2: Dùng paid tier**
- Nâng cấp lên Starter ($7/tháng) trên Render
- Bot sẽ luôn active, không cần uptimerobot

### 7.2 Nếu dùng Paid Tier
Không cần làm gì thêm, bot sẽ chạy 24/7 tự động.

---

## CẬP NHẬT CODE SAU KHI DEPLOY

Khi bạn thay đổi code:

1. Commit và push lên GitHub:
```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

2. Render sẽ tự động deploy lại
3. Chờ vài phút để deployment hoàn tất

---

## TROUBLESHOOTING

### Bot không phản hồi
- Kiểm tra **Logs** trên Render
- Đảm bảo Environment Variables đúng
- Kiểm tra webhook đã được set chưa
- Test endpoint `/health` trên browser

### Deployment thất bại
- Kiểm tra `Procfile` có đúng không
- Đảm bảo `requirements.txt` đầy đủ
- Xem log build để biết lỗi cụ thể

### Bot sleep (Free tier)
- Kiểm tra Uptimerobot đang hoạt động
- Hoặc nâng cấp lên paid tier

---

## LỢI ÍCH CỦA WEBHOOK

- ✅ Tiết kiệm tài nguyên (không cần polling liên tục)
- ✅ Phản hồi nhanh hơn
- ✅ Phù hợp cho môi trường cloud như Render
- ✅ Tự động chuyển giữa webhook (Render) và polling (local)

---

## URL CỦA BẠN

- **Render Service**: https://bottiktok-1-jaue.onrender.com
- **Health Check**: https://bottiktok-1-jaue.onrender.com/health
- **Webhook**: https://bottiktok-1-jaue.onrender.com/webhook

---

## XONG!

Bot của bạn giờ sẽ chạy 24/7 trên Render với webhook. 🎉
