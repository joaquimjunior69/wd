import yt_dlp

def download_video(url, resolution):
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
        'outtmpl': '/sdcard/vlc/ytd/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Digite a URL do YouTube: ")
    resolution = input("Digite a resolução desejada (ex: 720): ")
    download_video(url, resolution)
