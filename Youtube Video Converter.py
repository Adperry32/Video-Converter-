import tkinter as tk
import subprocess
from tkinter import filedialog, messagebox
from pytube import YouTube
from moviepy.editor import VideoFileClip


# Function to handle the download and conversion process using pytube
def download_and_convert():
    # Get user inputs
    url = url_entry.get()
    format_choice = format_var.get()
    output_path = filedialog.askdirectory()

    if not url or not output_path:
        messagebox.showerror("Error", "Please provide a URL and select an output directory.")
        return

    try:
        # Download the video using pytube
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download(output_path=output_path)
        
        # Convert to MP3 if needed
        if format_choice == "MP3":
            audio_path = video_path.replace(".mp4", ".mp3")
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(audio_path)
            clip.close()
        
        # Show success message
        messagebox.showinfo("Success", f"File saved to {output_path}")
    except Exception as e:
        # On failure, fallback to yt-dlp
        messagebox.showerror("Error", f"pytube failed: {str(e)}\nSwitching to yt-dlp.")
        download_with_ytdlp(url, output_path, format_choice)


# Function to handle the download using yt-dlp
def download_with_ytdlp(url, output_path, format_choice):
    try:
        format_flag = "bestaudio" if format_choice == "MP3" else "bestvideo"
        subprocess.run(
            [
                "yt-dlp",
                "-f",
                format_flag,
                "--output",
                f"{output_path}/%(title)s.%(ext)s",
                url
            ],
            check=True
        )
        messagebox.showinfo("Success", "Download successful using yt-dlp!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"yt-dlp failed: {str(e)}")


# GUI Setup
root = tk.Tk()
root.title("YouTube Video to Audio Converter")
root.geometry("400x250")

# Input field for YouTube URL
tk.Label(root, text="YouTube URL:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Format selection buttons (MP4 or MP3)
format_var = tk.StringVar(value="MP4")  # Default format
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

mp4_button = tk.Radiobutton(button_frame, text="MP4", variable=format_var, value="MP4", font=("Arial", 10))
mp4_button.pack(side=tk.LEFT, padx=10)

mp3_button = tk.Radiobutton(button_frame, text="MP3", variable=format_var, value="MP3", font=("Arial", 10))
mp3_button.pack(side=tk.LEFT, padx=10)

# Download button
download_button = tk.Button(
    root, text="Download", command=download_and_convert, bg="blue", fg="white", font=("Arial", 12)
)
download_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
