import json
import tkinter as tk
from tkinter import ttk, filedialog
import sys
import os
from main import main as download_main

class TikTokDownloaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Data Downloader")
        self.root.geometry("500x550")

        # Create and pack a main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Metadata file selection
        ttk.Label(main_frame, text="TikTok Data File:").pack(anchor=tk.W)

        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.metadata_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.metadata_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=(5, 0))

        # Download directory selection
        ttk.Label(main_frame, text="Save Location:").pack(anchor=tk.W)

        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        self.download_path = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.download_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side=tk.LEFT, padx=(5, 0))

        # Video type selection
        ttk.Label(main_frame, text="Download:").pack(anchor=tk.W)
        self.video_type = tk.StringVar(value="favorites")

        type_frame = ttk.Frame(main_frame)
        type_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Radiobutton(type_frame, text="Favorite Videos", value="favorites",
                        variable=self.video_type).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(type_frame, text="My Videos", value="my-videos",
                        variable=self.video_type).pack(side=tk.LEFT)

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Download Progress", padding="5")
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        # Overall progress
        ttk.Label(progress_frame, text="Overall:").pack(anchor=tk.W)
        self.overall_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.overall_progress.pack(fill=tk.X, pady=(0, 5))

        # Current video progress
        ttk.Label(progress_frame, text="Current Video:").pack(anchor=tk.W)
        self.video_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.video_progress.pack(fill=tk.X)

        # Status display
        self.status = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status, wraplength=450).pack(fill=tk.X)

        # Download button
        self.download_btn = ttk.Button(main_frame, text="Start Download", command=self.start_download)
        self.download_btn.pack(pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select TikTok data file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.metadata_path.set(filename)

    def browse_directory(self):
        directory = filedialog.askdirectory(title="Select download location")
        if directory:
            self.download_path.set(directory)

    def update_progress(self, video_num, total_videos, video_progress, message):
        """Update both progress bars and status message"""
        # Update overall progress (video_num out of total_videos)
        overall_percent = (video_num + video_progress) * 100 / total_videos
        self.overall_progress['value'] = overall_percent

        # Update current video progress
        self.video_progress['value'] = video_progress * 100

        # Update status message
        self.status.set(message)

        # Force GUI update
        self.root.update()

    def start_download(self):
        if not self.metadata_path.get() or not self.download_path.get():
            self.status.set("Please select both a data file and download location.")
            return

        self.download_btn.state(['disabled'])
        self.status.set("Starting download...")
        self.overall_progress['value'] = 0
        self.video_progress['value'] = 0

        try:
            # Call main() with our progress callback
            download_main(
                self.metadata_path.get(),
                self.download_path.get(),
                self.video_type.get(),
                self.update_progress
            )
            self.status.set("Download complete!")

        except Exception as e:
            self.status.set(f"Error: {str(e)}")
        finally:
            self.download_btn.state(['!disabled'])


def main():
    root = tk.Tk()
    app = TikTokDownloaderUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
