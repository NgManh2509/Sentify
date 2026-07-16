
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class LastFMService:
    rootUrl = "http://ws.audioscrobbler.com/2.0"

    emotionMap = {
        "admiration": "j-pop",
        "amusement": "k-pop",
        "anger": "metal",
        "annoyance": "punk",
        "approval": "indie pop",
        "caring": "acoustic",
        "confusion": "experimental",
        "curiosity": "alternative",
        "desire": "rnb",
        "disappointment": "lofi",
        "disapproval": "hard rock",
        "disgust": "grunge",
        "embarrassment": "indie",
        "excitement": "dance",
        "fear": "dark ambient",
        "gratitude": "folk",
        "grief": "piano",
        "joy": "k-pop",
        "love": "romantic",
        "nervousness": "soundtrack",
        "optimism": "anime",
        "pride": "j-pop",
        "realization": "post-rock",
        "relief": "chillout",
        "remorse": "acoustic",
        "sadness": "sad",
        "surprise": "electronic",
        "neutral": "pop"
    }

    def __init__(self, apiKey: str):
        if not apiKey:
            raise ValueError("apiKey is required")
        self.apiKey = apiKey

    def getTrackByEmotion(self, emotion: str, limit: int = 5) -> list:
        tag = self.emotionMap.get(emotion.lower(), "pop")
        logger.info(f"Đang lấy nhạc cho tag {tag}")

        params = {
            "method": "tag.gettoptracks",
            "tag": tag,
            "api_key": self.apiKey,
            "limit": limit,
            "format": "json"
        }

        try:
            response = requests.get(self.rootUrl, params=params, timeout=10)
            if response.status_code != 200:
                logger.error(f"Last.fm API trả về lỗi: {response.status_code}")
                return []

            data = response.json()
            track = data.get("tracks", {}).get("track", [])
            return [{"name": t.get("name"), "artist": t.get("artist", {}).get("name")} for t in track]
        except Exception as e:
            logger.error(f"Lỗi kết nối Last.fm API: {e}")
            return []


