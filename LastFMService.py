
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class LastFMService:
    rootUrl = "http://ws.audioscrobbler.com/2.0"

    emotionMap = {
        "admiration": {
            "high": ["epic", "symphonic metal", "Progressive metal"],
            "medium": ["j-pop", "indie rock", "classic rock"],
            "low": ["acoustic", "folk", "singer-songwriter"]
        },
        "amusement": {
            "high": ["happy", "fun", "upbeat"],
            "medium": ["pop", "k-pop", "j-pop"],
            "low": ["cute", "easy listening", "sweet"]
        },
        "anger": {
            "high": ["death metal", "thrash metal", "grindcore"],
            "medium": ["hard rock", "metalcore", "hardcore"],
            "low": ["alternative metal", "grunge", "blues rock"]
        },
        "annoyance": {
            "high": ["punk", "noise rock", "industrial metal"],
            "medium": ["garage rock", "post-punk", "industrial"],
            "low": ["minimal", "Lo-Fi", "downtempo"]
        },
        "approval": {
            "high": ["dance", "electro house", "k-pop"],
            "medium": ["indie pop", "rnb", "soul"],
            "low": ["Smooth Jazz", "lounge", "soft rock"]
        },
        "caring": {
            "high": ["beautiful", "orchestral", "contemporary classical"],
            "medium": ["acoustic", "piano", "Ballad"],
            "low": ["ambient", "chill", "easy listening"]
        },
        "confusion": {
            "high": ["mathcore", "breakcore", "Avant-Garde"],
            "medium": ["experimental", "psychedelic", "math rock"],
            "low": ["ambient", "drone", "dark ambient"]
        },
        "curiosity": {
            "high": ["trance", "synthwave", "psytrance"],
            "medium": ["Progressive rock", "post-rock", "Fusion"],
            "low": ["minimal techno", "idm", "glitch"]
        },
        "desire": {
            "high": ["sexy", "deep house", "latin"],
            "medium": ["rnb", "Neo-Soul", "synth pop"],
            "low": ["chillwave", "dream pop", "Mellow"]
        },
        "disappointment": {
            "high": ["doom metal", "screamo", "post-punk"],
            "medium": ["melancholy", "sad", "j-rock"],
            "low": ["melancholic", "blues", "dark folk"]
        },
        "disapproval": {
            "high": ["hard rock", "Gangsta Rap", "dark electro"],
            "medium": ["alternative", "alt metal", "indie rock"],
            "low": ["dark ambient", "slow", "acoustic"]
        },
        "disgust": {
            "high": ["death metal", "industrial noise", "Brutal Death Metal"],
            "medium": ["grunge", "Sludge", "darkwave"],
            "low": ["dark ambient", "drone", "noise"]
        },
        "embarrassment": {
            "high": ["breakcore", "fun", "pop punk"],
            "medium": ["indie pop", "shoegaze", "acoustic"],
            "low": ["Lo-Fi", "minimal", "ambient"]
        },
        "excitement": {
            "high": ["party", "dance", "EDM"],
            "medium": ["k-pop", "anime", "JPop"],
            "low": ["upbeat", "groovy", "House"]
        },
        "fear": {
            "high": ["horror punk", "black metal", "Soundtrack"],
            "medium": ["dark ambient", "darkwave", "industrial"],
            "low": ["drone", "dark", "atmospheric"]
        },
        "gratitude": {
            "high": ["epic", "orchestral", "gospel"],
            "medium": ["folk", "piano", "soul"],
            "low": ["acoustic", "chill", "ambient"]
        },
        "grief": {
            "high": ["depressive black metal", "doom metal", "screamo"],
            "medium": ["sad", "emotional", "melancholy"],
            "low": ["ambient", "drone", "slow"]
        },
        "joy": {
            "high": ["k-pop", "j-pop", "eurodance"],
            "medium": ["pop", "Kpop", "catchy"],
            "low": ["chill", "acoustic", "sweet"]
        },
        "love": {
            "high": ["epic", "romantic", "Love"],
            "medium": ["indie pop", "rnb", "love songs"],
            "low": ["acoustic", "piano", "Smooth Jazz"]
        },
        "nervousness": {
            "high": ["speed metal", "breakcore", "glitch"],
            "medium": ["Drum and bass", "industrial", "noise rock"],
            "low": ["minimal techno", "drone", "dark ambient"]
        },
        "optimism": {
            "high": ["anime", "power pop", "uplifting trance"],
            "medium": ["j-pop", "indie folk", "synthpop"],
            "low": ["acoustic", "chillwave", "classical"]
        },
        "pride": {
            "high": ["epic", "Heavy Metal", "classic rock"],
            "medium": ["hip hop", "rock", "british"],
            "low": ["folk", "acoustic", "indie"]
        },
        "realization": {
            "high": ["trance", "post-rock", "Progressive House"],
            "medium": ["tech house", "indie", "electronic"],
            "low": ["piano", "ambient", "minimalism"]
        },
        "relief": {
            "high": ["post-rock", "ambient", "chillout"],
            "medium": ["lounge", "rnb", "acoustic"],
            "low": ["atmospheric", "chill", "Lo-Fi"]
        },
        "remorse": {
            "high": ["doom metal", "screamo", "post-hardcore"],
            "medium": ["acoustic", "blues", "piano"],
            "low": ["Lo-Fi", "dark folk", "slow"]
        },
        "sadness": {
            "high": ["depressive black metal", "emo", "screamo"],
            "medium": ["melancholy", "sad", "j-rock"],
            "low": ["Lo-Fi", "chillout", "downtempo"]
        },
        "surprise": {
            "high": ["glitch", "dubstep", "breakcore"],
            "medium": ["hyperpop", "experimental", "idm"],
            "low": ["electronic", "jazz", "minimal"]
        },
        "neutral": {
            "high": ["pop", "House", "electronic"],
            "medium": ["easy listening", "background jazz", "chillout"],
            "low": ["ambient", "Lo-Fi", "minimal"]
        }
    }

    def __init__(self, apiKey: str):
        if not apiKey:
            raise ValueError("apiKey is required")
        self.apiKey = apiKey

    def _getTagByScore(self, emotion: str, score: float) -> str:
        import random
        tiers = self.emotionMap.get(emotion.lower())
        if not tiers:
            return "pop"
        if score >= 0.65:
            tier = "high"
        elif score >= 0.35:
            tier = "medium"
        else:
            tier = "low"
        return random.choice(tiers[tier])

    def _fetchByTag(self, tag: str, limit: int = 5) -> list:
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
                logger.warning(f"Last.fm trả lỗi {response.status_code} cho tag '{tag}'")
                return []
            data = response.json()
            tracks = data.get("tracks", {}).get("track", [])
            return [{"name": t.get("name"), "artist": t.get("artist", {}).get("name")} for t in tracks]
        except Exception as e:
            logger.error(f"Lỗi kết nối Last.fm API (tag={tag}): {e}")
            return []

    def getTrackByEmotion(self, emotion: str, score: float = 0.5, limit: int = 5) -> list:
        tag = self._getTagByScore(emotion, score)
        logger.info(f"Emotion '{emotion}' (score={score:.2f}) → tag '{tag}'")
        return self._fetchByTag(tag, limit=limit)

    def _getTagsByScore(self, emotion: str, score: float) -> list:
        """Trả về tất cả các tags trong tier tương ứng với score."""
        tiers = self.emotionMap.get(emotion.lower())
        if not tiers:
            return ["pop"]
        if score >= 0.65:
            tier = "high"
        elif score >= 0.35:
            tier = "medium"
        else:
            tier = "low"
        return list(tiers[tier])

    def getTrackByEmotions(self, emotions: list, limit: int = 5) -> list:
        import random

        if not emotions:
            return self._fetchByTag("pop", limit=limit)

        results = []
        seen = set()
        all_tags = []  # pool để random fill nếu chưa đủ limit

        # Bước 1: Với mỗi emotion, duyệt qua tất cả tags trong tier → mỗi tag lấy 1 bài
        for e in emotions:
            label = e["label"]
            score = e["score"]
            tags = self._getTagsByScore(label, score)
            all_tags.extend(tags)

            for tag in tags:
                logger.info(f"Emotion '{label}' (score={score:.2f}) → tag '{tag}' → lấy 1 bài")
                fetched = self._fetchByTag(tag, limit=3)  
                for track in fetched:
                    key = (track.get("name", "").lower(), track.get("artist", "").lower())
                    if key not in seen:
                        seen.add(key)
                        results.append(track)
                        break  # mỗi tag chỉ lấy 1 bài

        # Bước 2: Nếu chưa đủ limit → tiếp tục random từ pool all_tags
        random.shuffle(all_tags)
        tag_pool = list(all_tags)  # copy để vòng lặp
        pool_index = 0

        while len(results) < limit and tag_pool:
            tag = tag_pool[pool_index % len(tag_pool)]
            pool_index += 1

            fetched = self._fetchByTag(tag, limit=5)
            added = False
            for track in fetched:
                key = (track.get("name", "").lower(), track.get("artist", "").lower())
                if key not in seen:
                    seen.add(key)
                    results.append(track)
                    added = True
                    break

            # Nếu đã đi hết một vòng tag_pool mà không thêm được bài → dừng để tránh vòng vô hạn
            if pool_index >= len(tag_pool) and not added:
                break

        random.shuffle(results)
        return results[:limit]


