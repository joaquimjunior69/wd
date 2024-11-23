import os
import yt_dlp as youtube_dl
import inquirer

def download_video(url, resolution, save_path):
    try:
        # Configuração para escolher a resolução e baixar o vídeo
        ydl_opts = {
            'format': f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]',  # Escolher resolução
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Caminho para salvar o arquivo
        }
        
        # Baixar o vídeo usando yt-dlp
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print(f"Vídeo baixado com sucesso em {resolution}p!")
    
    except Exception as e:
        print(f"Ocorreu um erro ao tentar baixar o vídeo: {str(e)}")

def main():
    # Solicita a URL do vídeo
    url = input("Insira o URL do vídeo: ")
    
    try:
        # Cria o objeto YouTube usando yt-dlp
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
        
        # Verifica se existe a chave 'formats' e extrai as resoluções
        if not formats:
            print("Não foi possível encontrar formatos para o vídeo.")
            return
        
        # Filtra as resoluções válidas
        resolutions = sorted(set([f['height'] for f in formats if f.get('height')]), reverse=True)
        
        if not resolutions:
            print("Nenhuma resolução progressiva encontrada.")
            return
        
        # Cria o menu de seleção de resoluções
        questions = [
            inquirer.List(
                'resolution',
                message="Escolha a resolução desejada",
                choices=resolutions,
            ),
        ]
        
        # Obtém a resolução escolhida pelo usuário
        answers = inquirer.prompt(questions)
        resolution = answers['resolution']
        
        print(f"Resolução selecionada: {resolution}p")
        
        # Caminho onde o vídeo será salvo
        save_path = "/sdcard/vc/ytd"
        
        # Cria o diretório, caso não exista
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        download_video(url, resolution, save_path)

    except Exception as e:
        print(f"Ocorreu um erro ao acessar o vídeo: {str(e)}")

if __name__ == "__main__":
    main()

