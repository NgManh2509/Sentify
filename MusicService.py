import os
import random
import logging
from dotenv import load_dotenv

from LastFMService import LastFMService
from SpotifyService import SpotifyService

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MusicService:
    def __init__(self, lastfm: LastFMService, spotify: SpotifyService):
        self.lastfm = lastfm
        self.spotify = spotify

    def getRecommendation(self, emotion: str, score: float = 0.5, limit: int = 5) -> list:
        """Lấy gợi ý từ một emotion đơn lẻ (backward-compatible)."""
        candidateTrack = self.lastfm.getTrackByEmotion(emotion, score=score, limit=limit * 3)

        if not candidateTrack:
            return []

        random.shuffle(candidateTrack)
        finalRec = []
        for track in candidateTrack:
            if len(finalRec) >= limit:
                break
            spotifyTrack = self.spotify.searchTrackMetaData(track["name"], track["artist"])
            if spotifyTrack:
                finalRec.append(spotifyTrack)
        return finalRec

    def getRecommendationByEmotions(self, emotions: list, limit: int = 5) -> list:
        candidateTrack = self.lastfm.getTrackByEmotions(emotions, limit=limit * 3)

        if not candidateTrack:
            return []

        finalRec = []
        for track in candidateTrack:
            if len(finalRec) >= limit:
                break
            spotifyTrack = self.spotify.searchTrackMetaData(track["name"], track["artist"])
            if spotifyTrack:
                finalRec.append(spotifyTrack)
        return finalRec


if __name__ == "__main__":
    load_dotenv()
    lastfm_svc = LastFMService(apiKey=os.getenv("LASTFM_API_KEY"))
    spotify_svc = SpotifyService(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
    music_svc = MusicService(lastfm=lastfm_svc, spotify=spotify_svc)
    songs = music_svc.getRecommendation("joy", limit=5)

    for idx, song in enumerate(songs, 1):
        print(f"{idx}. {song['name']} - {song['artists']}")
        print(f"   Iframe ID: {song['id']}")
