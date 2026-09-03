import os
from googleapiclient.discovery import build
import yt_dlp

pendrive = "D:\\"

if os.path.exists(pendrive):
    print(f"✅ Pendrive acessado com sucesso: {pendrive}")
else:
    print(f"❌ Não foi possível acessar: {pendrive}")

# ── Configurações ──────────────────────────────────────────
YOUTUBE_API_KEY = "AIzaSyCCZrdoOjcCk8YqA81swG0k2bcwrPODjGY" 
PLAYLIST_ID = "PLBTf6uglIBM6_hnTpe219u0cRgzoxhKke"
DESTINO = "D:\\"

# ── Busca vídeos da playlist ───────────────────────────────
def buscar_videos_playlist(playlist_id):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            videos.append({
                "titulo": item["snippet"]["title"],
                "videoId": item["snippet"]["resourceId"]["videoId"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

# ── Download com yt-dlp ────────────────────────────────────
def baixar_musicas(videos, destino):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for video in videos:
            url = f"https://www.youtube.com/watch?v={video['videoId']}"
            print(f"⬇️  Baixando: {video['titulo']}")
            ydl.download([url])

# ── Execução ───────────────────────────────────────────────
print(f"\n🔍 Buscando vídeos da playlist...")
videos = buscar_videos_playlist(PLAYLIST_ID)
print(f"✅ {len(videos)} vídeos encontrados\n")

baixar_musicas(videos, DESTINO)
print("\n✅ Download concluído!")