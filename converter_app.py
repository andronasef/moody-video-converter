import customtkinter as ctk
from tkinter import filedialog, messagebox
import ffmpeg
import threading
import os
import sys

# --- UI Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class VideoConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Main Window Configuration ---
        self.title("Vertical Video Converter")
        self.geometry("800x600")
        self.minsize(700, 500)

        if os.path.exists("icon.ico"):
            self.iconbitmap("icon.ico")

        # --- App State Variables ---
        self.video_files = []
        self.file_widgets = []  # To track the UI widgets for each file

        # --- Main Layout (2 columns) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 1. Left Frame (Control Panel) ---
        self.control_frame = ctk.CTkFrame(self, width=250)
        self.control_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        self.control_frame.grid_propagate(False)

        app_title = ctk.CTkLabel(
            self.control_frame,
            text="Video Converter",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        app_title.pack(pady=(10, 20))

        self.select_files_button = ctk.CTkButton(
            self.control_frame, text="Select Videos", command=self.select_videos
        )
        self.select_files_button.pack(pady=10, padx=20, fill="x")

        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="Start Conversion",
            command=self.start_conversion_thread,
            state="disabled",
        )
        self.start_button.pack(pady=10, padx=20, fill="x", ipady=5)

        # Status Display Area
        status_title = ctk.CTkLabel(
            self.control_frame, text="Overall Status", font=ctk.CTkFont(size=14)
        )
        status_title.pack(pady=(20, 5), padx=20, anchor="w")

        self.status_label = ctk.CTkLabel(
            self.control_frame,
            text="Ready to select files...",
            text_color="gray",
            wraplength=220,
        )
        self.status_label.pack(pady=5, padx=20, anchor="w")

        self.progress_bar = ctk.CTkProgressBar(self.control_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10, padx=20, fill="x")

        # --- 2. Right Frame (File Queue) ---
        self.files_frame = ctk.CTkFrame(self)
        self.files_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        files_title = ctk.CTkLabel(
            self.files_frame,
            text="Video Queue",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        files_title.pack(pady=10, padx=20)

        self.scrollable_files_frame = ctk.CTkScrollableFrame(self.files_frame)
        self.scrollable_files_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def safe_ui_update(self, widget, **kwargs):
        """A thread-safe function to update UI elements."""
        self.after(0, lambda: widget.configure(**kwargs))

    def select_videos(self):
        """Opens a dialog to select videos and displays them in the queue."""
        self.video_files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video Files", "*.mp4 *.mov *.avi *.mkv"),
                ("All Files", "*.*"),
            ],
        )

        # Clear the old list from the UI
        for widget in self.file_widgets:
            widget.destroy()
        self.file_widgets.clear()

        if self.video_files:
            for file_path in self.video_files:
                file_name = os.path.basename(file_path)
                label = ctk.CTkLabel(
                    self.scrollable_files_frame, text=f"⏳ {file_name}"
                )
                label.pack(pady=5, padx=10, anchor="w")
                self.file_widgets.append(label)

            self.safe_ui_update(
                self.status_label,
                text=f"{len(self.video_files)} file(s) selected. Ready to start.",
                text_color="white",
            )
            self.start_button.configure(state="normal")
        else:
            self.safe_ui_update(
                self.status_label, text="No videos selected.", text_color="gray"
            )
            self.start_button.configure(state="disabled")

    def start_conversion_thread(self):
        """Starts the video processing in a separate thread to keep the UI responsive."""
        self.start_button.configure(state="disabled")
        self.select_files_button.configure(state="disabled")
        self.progress_bar.set(0)

        conversion_thread = threading.Thread(target=self.process_videos, daemon=True)
        conversion_thread.start()

    def process_videos(self):
        """The core function that processes all selected videos."""
        total_files = len(self.video_files)
        ffmpeg_executable = self.get_ffmpeg_path()

        for i, video_path in enumerate(self.video_files):
            file_name_full = os.path.basename(video_path)

            # Update UI to show current processing file
            self.safe_ui_update(
                self.status_label,
                text=f"Processing ({i+1}/{total_files}):\n{file_name_full}",
                text_color="cyan",
            )
            self.safe_ui_update(
                self.file_widgets[i], text=f"⚙️ {file_name_full}", text_color="cyan"
            )

            # --- Logic to create the new output filename and path ---
            directory = os.path.dirname(video_path)
            base_name, extension = os.path.splitext(file_name_full)
            output_filename = f"{base_name}Resized{extension}"
            output_path = os.path.join(directory, output_filename)

            try:
                # Get input stream
                input_stream = ffmpeg.input(video_path)
                
                # Apply video filters to video stream
                video = (
                    input_stream.video
                    .filter(
                        "scale", w=1080, h=1920, force_original_aspect_ratio="decrease"
                    )
                    .filter(
                        "pad",
                        w=1080,
                        h=1920,
                        x="(ow-iw)/2",
                        y="(oh-ih)/2",
                        color="black",
                    )
                )
                
                # Get audio stream
                audio = input_stream.audio
                
                # Map both video and audio to output
                (
                    ffmpeg.output(video, audio, output_path, vcodec="libx264", acodec="copy")
                    .run(cmd=ffmpeg_executable, overwrite_output=True, quiet=True)
                )
                # Update UI on success
                self.safe_ui_update(
                    self.file_widgets[i],
                    text=f"✅ {file_name_full}",
                    text_color="lightgreen",
                )

            except ffmpeg.Error as e:
                # Update UI on failure
                self.safe_ui_update(
                    self.file_widgets[i], text=f"❌ {file_name_full}", text_color="red"
                )
                print(
                    f"Error processing {file_name_full}: {e.stderr.decode()}"
                )  # For debugging

            # Update overall progress bar
            progress = (i + 1) / total_files
            self.safe_ui_update(self.progress_bar, set=progress)

        self.safe_ui_update(
            self.status_label,
            text="🎉 Conversion completed successfully!",
            text_color="lightgreen",
        )
        self.start_button.configure(state="normal")
        self.select_files_button.configure(state="normal")
        messagebox.showinfo(
            "Success", "All selected videos have been converted successfully!"
        )

    @staticmethod
    def get_ffmpeg_path():
        """Determines the path to ffmpeg.exe for both script and bundled .exe mode."""
        if getattr(sys, "frozen", False):
            # Running as a bundled executable
            return os.path.join(sys._MEIPASS, "ffmpeg.exe")
        else:
            # Running as a .py script
            return "ffmpeg"


if __name__ == "__main__":
    app = VideoConverterApp()
    app.mainloop()
