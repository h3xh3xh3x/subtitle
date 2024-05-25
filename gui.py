import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from main import main_process

class SubtitleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subtitle Generator")
        self.is_running = False

        self.file_label = tk.Label(root, text="Video File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10)
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        self.file_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.file_button.grid(row=0, column=2, padx=10, pady=10)

        self.video_lang_label = tk.Label(root, text="Video Language:")
        self.video_lang_label.grid(row=1, column=0, padx=10, pady=10)
        self.video_lang_var = tk.StringVar(value="eng")
        self.video_lang_menu = tk.OptionMenu(root, self.video_lang_var, "eng", "spa", "fre", "ger", "chi", "jpn")
        self.video_lang_menu.grid(row=1, column=1, padx=10, pady=10)

        self.sub_lang_label = tk.Label(root, text="Subtitle Language:")
        self.sub_lang_label.grid(row=2, column=0, padx=10, pady=10)
        self.sub_lang_var = tk.StringVar(value="eng")
        self.sub_lang_menu = tk.OptionMenu(root, self.sub_lang_var, "eng", "spa", "fre", "ger", "chi", "jpn")
        self.sub_lang_menu.grid(row=2, column=1, padx=10, pady=10)

        self.output_path_label = tk.Label(root, text="Output Path:")
        self.output_path_label.grid(row=3, column=0, padx=10, pady=10)
        self.output_path_entry = tk.Entry(root, width=50)
        self.output_path_entry.grid(row=3, column=1, padx=10, pady=10)
        self.output_path_button = tk.Button(root, text="Browse", command=self.browse_output_path)
        self.output_path_button.grid(row=3, column=2, padx=10, pady=10)

        self.subsync_var = tk.BooleanVar()
        self.subsync_check = tk.Checkbutton(root, text="Run subsync", variable=self.subsync_var)
        self.subsync_check.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.keep_intermediate_var = tk.BooleanVar()
        self.keep_intermediate_check = tk.Checkbutton(root, text="Keep intermediate files", variable=self.keep_intermediate_var)
        self.keep_intermediate_check.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_processing)
        self.start_button.grid(row=6, column=0, columnspan=1, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_processing)
        self.stop_button.grid(row=6, column=1, columnspan=1, padx=10, pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.progress_label = tk.Label(root, text="Processing, please wait...")
        self.progress_bar = ttk.Progressbar(root, mode='indeterminate')

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_output_path(self):
        output_path = filedialog.askdirectory()
        if output_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, output_path)

    def start_processing(self):
        if self.is_running:
            return
        video_file = self.file_entry.get()
        video_lang = self.video_lang_var.get()
        sub_lang = self.sub_lang_var.get()
        output_path = self.output_path_entry.get()
        run_subsync = self.subsync_var.get()
        keep_intermediate = self.keep_intermediate_var.get()
        if not os.path.isfile(video_file):
            messagebox.showerror("Error", "Please select a valid video file.")
            return
        if not os.path.isdir(output_path):
            messagebox.showerror("Error", "Please select a valid output directory.")
            return
        self.progress_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        self.progress_bar.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        self.progress_bar.start()
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.run_main_process, args=(video_file, run_subsync, keep_intermediate, video_lang, sub_lang, output_path)).start()

    def stop_processing(self):
        self.is_running = False
        self.progress_bar.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_label.grid_remove()
        self.progress_bar.grid_remove()
        messagebox.showinfo("Info", "Processing stopped.")

    def run_main_process(self, video_file, run_subsync, keep_intermediate, video_lang, sub_lang, output_path):
        try:
            main_process(video_file, run_subsync, keep_intermediate, video_lang, sub_lang, output_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.is_running = False
            self.progress_bar.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress_label.grid_remove()
            self.progress_bar.grid_remove()

def run_gui():
    root = tk.Tk()
    app = SubtitleApp(root)
    root.mainloop()
