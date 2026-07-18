import yt_dlp
import os
import requests
import shutil
import tempfile
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

def cleanup_temp_dir(temp_dir: str):
    shutil.rmtree(temp_dir, ignore_errors=True)

def getAudio(url: str):
    tmp_dir = tempfile.mkdtemp(prefix="yt_dlp_audio_")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'ignoreerrors': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        downloadedFiles = os.listdir(tmp_dir)
        if not downloadedFiles:
            raise Exception("Không tìm thấy file sau khi tải.")

        filePath = os.path.join(tmp_dir, downloadedFiles[0])
        return tmp_dir, filePath

    except Exception as e:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise e

@router.get("/api/download")
async def download_file(song_name: str, artist_name: str, background_tasks: BackgroundTasks):
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="Thiếu YOUTUBE_API_KEY trong biến môi trường")

    search_query = f"{song_name} {artist_name}"
    yt_search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": 1,
        "q": search_query,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(yt_search_url, params=params)
    data = response.json()
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Lỗi khi gọi YouTube API")

    items = data.get("items", [])
    if not items:
        raise HTTPException(status_code=404, detail="Không tìm thấy video trên YouTube")

    video_id = items[0]["id"]["videoId"]
    yt_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        temp_dir, filePath = getAudio(yt_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tải nhạc: {str(e)}")

    background_tasks.add_task(cleanup_temp_dir, temp_dir)
    safe_filename = f"{song_name} - {artist_name}.mp3".replace("/", "_").replace("\\", "_")
    return FileResponse(
        path=filePath,
        filename=safe_filename,
        media_type='audio/mpeg'
    )
