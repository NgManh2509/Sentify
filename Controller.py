
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import time
from dotenv import load_dotenv

from TranslateModel import translateToEng
from EmotionDetect import detect
from LastFMService import LastFMService
from SpotifyService import SpotifyService
from MusicService import MusicService
from YoutubeService import router as youtube_router

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(youtube_router)

musicSV = None

# ─── Session history store ────────────────────────────────────────────────────
# { session_id: {"seen": set("name|artist"), "last_active": float(timestamp)} }
_session_store: dict = {}
_SESSION_TTL = 3600  # giây – session hết hạn sau 1 giờ không hoạt động

def _get_session_seen(session_id: str) -> set:
    """Trả về set các bài đã đề xuất cho session này."""
    now = time.time()
    # Dọn session hết hạn
    expired = [sid for sid, data in _session_store.items() if now - data["last_active"] > _SESSION_TTL]
    for sid in expired:
        del _session_store[sid]

    if session_id not in _session_store:
        _session_store[session_id] = {"seen": set(), "last_active": now}
    else:
        _session_store[session_id]["last_active"] = now
    return _session_store[session_id]["seen"]

def _update_session_seen(session_id: str, tracks: list):
    """Thêm các bài vừa đề xuất vào history của session."""
    seen = _get_session_seen(session_id)
    for t in tracks:
        key = f"{t.get('name','').lower()}|{t.get('artists','').lower()}"
        seen.add(key)
try:
    lastFM = LastFMService(apiKey=os.getenv("LASTFM_API_KEY"))
    spotify = SpotifyService(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    )
    musicSV = MusicService(lastfm=lastFM, spotify=spotify)
except Exception as e:
    print(f"Lỗi khởi tạo service {e}")

class TextInput(BaseModel):
    text: str
    session_id: str | None = None

@app.post("/api/analyze")
async def analyze_and_recommend(input_text: TextInput):
    if musicSV is None:
        raise HTTPException(status_code=503, detail="Service chưa được khởi tạo, kiểm tra lại API key")
    if not input_text.text.strip():
        raise HTTPException(status_code=400, detail="Văn bản không được để trống")
    try:
        translatedText = translateToEng(input_text.text)
        emotionRes = detect(translatedText)
        labels = emotionRes.get("labels", [])
        scores = emotionRes.get("scores", [])

        # Lấy top-3 emotion theo score giảm dần
        top_emotions = sorted(
            [{"label": l, "score": s} for l, s in zip(labels, scores)],
            key=lambda x: -x["score"]
        )[:3]

        mainEmotion = top_emotions[0]["label"] if top_emotions else "neutral"

        session_id = input_text.session_id
        already_seen: set = _get_session_seen(session_id) if session_id else set()
        candidates = musicSV.getRecommendationByEmotions(top_emotions, limit=15)
        songs = []
        seen_names: set = set() 
        for t in candidates:
            name_key = t.get('name', '').lower()
            session_key = f"{name_key}|{t.get('artists','').lower()}"
            if session_key not in already_seen and name_key not in seen_names:
                songs.append(t)
                seen_names.add(name_key)
            if len(songs) >= 5:
                break

        # Cập nhật history session
        if session_id:
            _update_session_seen(session_id, songs)

        return {
            "status": "success",
            "original_text": input_text.text,
            "translated_text": translatedText,
            "emotions_detected": emotionRes,
            "main_emotion": mainEmotion,
            "recommendations": songs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

