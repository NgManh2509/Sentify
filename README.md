# 🎵 Sentify — Emotion-Based Music Recommender

> Nhập cảm xúc bằng tiếng Việt → Hệ thống phân tích → Gợi ý nhạc phù hợp tâm trạng

Sentify là ứng dụng web kết hợp **NLP** và **Machine Learning** để phát hiện cảm xúc từ văn bản tiếng Việt, sau đó đề xuất bài hát phù hợp thông qua **Last.fm**, **Spotify** và **YouTube**.

---

## ✨ Tính năng

- 🌐 **Hỗ trợ tiếng Việt**: Dịch tự động sang tiếng Anh trước khi phân tích (bao gồm xử lý từ lóng)
- 🧠 **Phát hiện đa cảm xúc**: Sử dụng mô hình `monologg/bert-base-cased-goemotions-original` hỗ trợ 28 nhãn cảm xúc
- 🎵 **Gợi ý nhạc thông minh**: Kết hợp Last.fm (tìm kiếm theo tag nhạc) + Spotify (metadata, ảnh bìa, link nghe)
- ▶️ **Tải nhạc từ YouTube**: Tải file MP3 chất lượng cao qua YouTube API + yt-dlp
- 🔄 **Session tracking**: Không lặp lại bài hát đã gợi ý trong cùng phiên (TTL: 1 giờ)
- 💬 **Giao diện chat**: UI hiện đại dạng chat, hiển thị kết quả trực quan

---

## 🏗️ Kiến trúc hệ thống

```
Sentify/
│
├── Backend (Python / FastAPI)
│   ├── main.py                 # CLI demo – chạy độc lập không cần frontend
│   ├── Controller.py           # FastAPI app, định nghĩa API endpoints
│   ├── TranslateModel.py       # Dịch Việt → Anh (facebook/nllb-200-1.3B)
│   ├── EmotionDetect.py        # Phát hiện cảm xúc (BERT GoEmotions)
│   ├── LastFMService.py        # Tìm bài hát theo tag cảm xúc qua Last.fm API
│   ├── SpotifyService.py       # Lấy metadata + ảnh bìa từ Spotify API
│   ├── MusicService.py         # Orchestrate LastFM + Spotify
│   ├── YoutubeService.py       # Tìm & tải nhạc MP3 từ YouTube
│   ├── model.py                # Kiến trúc BertForMultiLabelClassification
│   └── multilabel_pipeline.py  # Pipeline multi-label inference
│
└── Frontend/ (React + Vite + TailwindCSS)
    └── Sentify/
        └── src/
            ├── App.jsx
            ├── components/
            │   ├── SideBar.jsx
            │   ├── DisplayComponents/
            │   │   ├── MainChat.jsx
            │   │   └── Instruction.jsx
            │   └── ResponseComponents/
            │       └── ModelResponse.jsx
            └── services/
                └── api.js
```

---

## ⚙️ Yêu cầu hệ thống

| Thành phần | Phiên bản |
|---|---|
| Python | ≥ 3.10 |
| Node.js | ≥ 18.x |
| FFmpeg | Bất kỳ (cần cho yt-dlp tải MP3) |
| GPU (tuỳ chọn) | CUDA – tăng tốc inference |

---

## 🚀 Hướng dẫn cài đặt & Chạy

### 1. Clone repository

```bash
git clone https://github.com/NgManh2509/Sentify.git
cd Sentify
```

### 2. Cấu hình API Keys

Tạo file `.env` tại thư mục gốc (ngang hàng với `Controller.py`):

```env
# Spotify Developer – https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Last.fm API – https://www.last.fm/api/account/create
LASTFM_API_KEY=your_lastfm_api_key
LASTFM_SHARED_SECRET=your_lastfm_shared_secret

# YouTube Data API v3 – https://console.cloud.google.com/
YOUTUBE_API_KEY=your_youtube_api_key
```

> ⚠️ **Lưu ý bảo mật**: Không commit file `.env` lên git. File này đã được thêm vào `.gitignore`.

---

### 3. Cài đặt & Chạy Backend

```bash
# Tạo và kích hoạt môi trường ảo
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Cài đặt dependencies
pip install fastapi uvicorn python-dotenv requests spotipy transformers torch yt-dlp
```

> 💡 **GPU acceleration**: Nếu có GPU NVIDIA, cài PyTorch với CUDA:
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cu121
> ```

**Khởi động server Backend:**

```bash
uvicorn Controller:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: `http://localhost:8000`

Swagger UI (API docs): `http://localhost:8000/docs`

> ⏳ **Lần đầu chạy**: Hệ thống sẽ tự động tải các model AI (NLLB ~5GB + BERT ~400MB). Hãy đảm bảo kết nối internet ổn định.

---

### 4. Cài đặt & Chạy Frontend

```bash
cd Frontend/Sentify

# Cài đặt dependencies
npm install

# Chạy dev server
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:5173`

---

### 5. Cài đặt FFmpeg (cho tính năng tải nhạc)

**Windows:**
```powershell
# Dùng winget
winget install FFmpeg

# Hoặc tải tại: https://ffmpeg.org/download.html
# Sau đó thêm vào PATH hệ thống
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

---

## 🖥️ Chạy nhanh (CLI Demo)

Nếu chỉ muốn kiểm tra tính năng phát hiện cảm xúc mà không cần frontend:

```bash
# Kích hoạt venv trước
python main.py
```

Kết quả mẫu:

```
==================================================
  Sentify — Phát hiện cảm xúc từ tiếng Việt
==================================================
Nhập văn bản tiếng Việt (Enter trống để thoát)

🇻🇳 Nhập > Hôm nay tôi rất vui vì được gặp bạn bè
🇬🇧 Dịch    : Today I am very happy to meet my friends
💬 Cảm xúc  :
   😄  joy             87.32%  █████████████████
   🥰  caring          45.10%  █████████
   🌟  optimism        32.45%  ██████
```

---

## 🌐 Hướng dẫn sử dụng giao diện Web

### Bước 1: Nhập cảm xúc

Trong ô chat, nhập văn bản mô tả cảm xúc của bạn **bằng tiếng Việt** (hoặc tiếng Anh), rồi nhấn **Enter** hoặc nút gửi.

```
Ví dụ:
• "Tôi đang rất buồn và cô đơn"
• "Hôm nay thật tuyệt vời, mọi thứ đều suôn sẻ!"
• "Cảm giác lo lắng trước kỳ thi"
• "Đang cần nhạc để tập trung làm việc"
```

### Bước 2: Xem kết quả phân tích

Hệ thống trả về:
- 🇬🇧 **Văn bản đã dịch** sang tiếng Anh
- 📊 **Top 3 cảm xúc** phát hiện được kèm điểm số
- 🎵 **5 bài hát gợi ý** phù hợp với tâm trạng (kèm ảnh bìa, tên nghệ sĩ)

### Bước 3: Nghe & Tải nhạc

- Nhấn **▶ Play on Spotify** để mở bài hát trực tiếp trên Spotify
- Nhấn **⬇ Download MP3** để tải file nhạc về máy qua YouTube

### Gửi tiếp

Bạn có thể gửi thêm tin nhắn mới bất cứ lúc nào. Hệ thống tự động **tránh lặp lại bài hát đã gợi ý** trong cùng phiên làm việc.

---

## 🔌 API Endpoints

### `POST /api/analyze`

Phân tích cảm xúc và gợi ý nhạc.

**Request body:**
```json
{
  "text": "Tôi đang rất vui hôm nay",
  "session_id": "user-abc-123"
}
```

**Response:**
```json
{
  "status": "success",
  "original_text": "Tôi đang rất vui hôm nay",
  "translated_text": "I am very happy today",
  "emotions_detected": {
    "labels": ["joy", "optimism", "excitement"],
    "scores": [0.91, 0.54, 0.38]
  },
  "main_emotion": "joy",
  "recommendations": [
    {
      "id": "2374M0fQpwd7hxTFJa67Z2",
      "name": "Happy",
      "artists": "Pharrell Williams",
      "cover_image": "https://i.scdn.co/image/...",
      "spotify_url": "https://open.spotify.com/track/..."
    }
  ]
}
```

> 💡 **session_id** *(tuỳ chọn)*: Chuỗi định danh phiên bất kỳ. Nếu truyền vào, hệ thống không lặp lại bài đã gợi ý trong phiên đó (hết hạn sau 1 giờ không hoạt động).

---

### `GET /api/download`

Tìm kiếm và tải file MP3 từ YouTube.

**Query params:**
```
GET /api/download?song_name=Happy&artist_name=Pharrell+Williams
```

**Response:** File nhị phân MP3 (`audio/mpeg`)

---

## 🎭 Danh sách cảm xúc hỗ trợ (28 nhãn GoEmotions)

| Cảm xúc | Emoji | Cảm xúc | Emoji |
|---|---|---|---|
| admiration | 🤩 | nervousness | 😰 |
| amusement | 😄 | optimism | 🌟 |
| anger | 😡 | pride | 🦁 |
| annoyance | 😤 | realization | 💡 |
| approval | 👍 | relief | 😮‍💨 |
| caring | 🥰 | remorse | 😔 |
| confusion | 😕 | sadness | 😢 |
| curiosity | 🤔 | surprise | 😲 |
| desire | 😍 | neutral | 😐 |
| disappointment | 😞 | joy | 😄 |
| disapproval | 👎 | love | ❤️ |
| disgust | 🤢 | grief | 😭 |
| embarrassment | 😳 | fear | 😨 |
| excitement | 🤩 | gratitude | 🙏 |

---

## 🛠️ Công nghệ sử dụng

### Backend

| Thư viện | Mục đích |
|---|---|
| `FastAPI` | Web framework, REST API |
| `uvicorn` | ASGI server |
| `transformers` | Tải và chạy model BERT, NLLB |
| `torch` | Deep learning inference |
| `spotipy` | Spotify Web API client |
| `yt-dlp` | Tải audio từ YouTube |
| `python-dotenv` | Quản lý biến môi trường |
| `requests` | HTTP client cho Last.fm API |

### Frontend

| Thư viện | Mục đích |
|---|---|
| `React 19` | UI framework |
| `Vite` | Build tool & dev server |
| `TailwindCSS v4` | Utility-first CSS framework |
| `lucide-react` | Icon library |
| `react-icons` | Icon library bổ sung |

### AI Models

| Model | Nhiệm vụ | Kích thước |
|---|---|---|
| `facebook/nllb-200-1.3B` | Dịch Việt → Anh | ~5 GB |
| `monologg/bert-base-cased-goemotions-original` | Phân tích cảm xúc đa nhãn | ~400 MB |

---

## 🐛 Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|---|---|---|
| `Service chưa được khởi tạo` | API keys sai hoặc thiếu | Kiểm tra lại file `.env` |
| Tải model chậm / thất bại | Mạng yếu hoặc hết dung lượng | Cần ~6GB ổ đĩa, kết nối internet ổn định |
| Lỗi tải nhạc (Download) | FFmpeg chưa cài hoặc YouTube key hết hạn mức | Cài FFmpeg, kiểm tra quota YouTube API |
| Frontend không kết nối Backend | Backend chưa chạy | Đảm bảo Backend chạy tại `http://localhost:8000` |
| CORS error | Cấu hình CORS | Backend đã cấu hình `allow_origins=["*"]`, kiểm tra port |

---

## 📄 License

MIT License — feel free to use and modify.

---

<div align="center">
  Made with ❤️ by <strong>NgManh2509</strong>
</div>
