import os
import yt_dlp as youtube_dl
import inquirer
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, DownloadColumn
from rich.console import Console
from rich import print

console = Console()

def download_video(url, resolution, save_path):
    try:
        # Configuration to select resolution and download the video
        ydl_opts = {
            'format': f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]',  # Select resolution
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Path to save the file
            'progress_hooks': [progress_hook],  # Calls the progress_hook function during download
        }
        
        # Download the video using yt-dlp
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
    except Exception as e:
        console.print(f"[red]An error occurred while trying to download the video: {str(e)}[/red]")

# Function to display progress using Rich
progress_bar = Progress(
    TextColumn("[cyan]{task.description}"),
    BarColumn(),
    DownloadColumn(),
    TextColumn("[bold blue]{task.percentage:>3.0f}%"),
    TimeRemainingColumn(),
)

def progress_hook(d):
    if d['status'] == 'downloading':
        filename = d['info_dict']['title']
        total_size = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        downloaded = d['downloaded_bytes']

        if not hasattr(progress_hook, "task_id"):
            progress_hook.task_id = progress_bar.add_task(
                f"[magenta]{filename}",
                total=total_size,
                start=True,
            )
        else:
            progress_bar.update(progress_hook.task_id, completed=downloaded)

    elif d['status'] == 'finished':
        filename = d['info_dict']['title']
        console.print(f"[green]Download completed: {filename}[/green]")

def main():
    # Ask for the video URL
    url = input("Enter the video URL: ")
    
    try:
        # Create the YouTube object using yt-dlp
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
        
        # Check if the 'formats' key exists and extract resolutions
        if not formats:
            console.print("[red]Unable to find formats for the video.[/red]")
            return
        
        # Filter valid resolutions
        resolutions = sorted(set([f['height'] for f in formats if f.get('height')]), reverse=True)
        
        if not resolutions:
            console.print("[red]No progressive resolutions found.[/red]")
            return
        
        # Create the resolution selection menu
        questions = [
            inquirer.List(
                'resolution',
                message="Choose the desired resolution",
                choices=resolutions,
            ),
        ]
        
        # Get the resolution selected by the user
        answers = inquirer.prompt(questions)
        resolution = answers['resolution']
        
        console.print(f"[cyan]Selected resolution: {resolution}p[/cyan]")
        
        # Path where the video will be saved
        save_path = "/sdcard/vc/ytd"
        
        # Create the directory if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # Start download with Rich progress bar
        with progress_bar:
            download_video(url, resolution, save_path)

    except Exception as e:
        console.print(f"[red]An error occurred while accessing the video: {str(e)}[/red]")

if __name__ == "__main__":
    main()
