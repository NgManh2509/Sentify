from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from TranslateModel import translateToEng
from EmotionDetect import detect
from LastFMService import LastFMService
from SpotifyService import SpotifyService
from MusicService import MusicService

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

musicSV = None
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
        mainEmotion = labels[0] if labels else "neutral"

        songs = musicSV.getRecommendation(mainEmotion, limit=5)
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

