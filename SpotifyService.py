import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging

logger = logging.getLogger(__name__)

class SpotifyService:
    def __init__(self, client_id: str, client_secret: str):
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret are required")

        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id = client_id,
            client_secret = client_secret
        ))

    def searchTrackMetaData(self, track_name: str, artist_name: str) -> dict:
        query = f"track:{track_name} artist:{artist_name}"
        try:
            res = self.sp.search(q=query, limit=1, type='track')
            items = res.get("tracks", {}).get("items", [])

            if not items:
                logger.warning(f"Không tìm thấy trên Spotify: '{track_name}' - '{artist_name}'")
                return None

            track = items[0]
            artists_list = [artist["name"] for artist in track.get("artists", [])]
            images = track.get("album", {}).get("images", [])

            return {
                "id": track.get("id"),
                "name": track.get("name"),
                "artists": ", ".join(artists_list),
                "cover_image": images[0]["url"] if images else None,
                "spotify_url": track.get("external_urls", {}).get("spotify")
            }
        except Exception as e:
            logger.error(f"Lỗi tìm kiếm Spotify API: {e}")
            return None