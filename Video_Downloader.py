import yt_dlp

def baixar_video(url):
    ydl_opts = {
        'format': 'best', # Melhor qualidade
        'outtmpl': '%(title)s.%(ext)s' # Nome arquivo
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Sucesso.")
    except Exception as e:
        print(f"Erro: {e}")

# Uso
baixar_video('URL_DO_VIDEO_AQUI')