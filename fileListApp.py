import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import filedialog
import subprocess

from sourceSDK import SourceSDK
from texture import Texture
from _vpk import VPK

class FileListApp(tk.Tk):

    sdk : SourceSDK

    def __init__(self, sourceSDK):
        super().__init__()

        self.sdk = sourceSDK
        
        self.title("File List with Tkinter")
        self.geometry("800x600")

        self.current_folder = self.sdk.selected_folder
        self.firstfolder = self.sdk.selected_folder

        self.create_widgets()
        self.load_files(self.current_folder)

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg='white')
        self.scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.up_button = ttk.Button(self, text="Up", command=self.go_up)
        self.up_button.pack(pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

    def load_files(self, folder):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.current_folder = folder
        self.files = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f)) or f.endswith((".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga", ".wav", ".mp3"))]

        columns = 5  # Number of columns in the grid
        row = 0
        col = 0

        for file in self.files:
            file_path = os.path.join(self.current_folder, file)
            frame = ttk.Frame(self.scroll_frame, width=140, height=140, relief="solid", borderwidth=1)
            frame.grid_propagate(False)  # Prevent frame from resizing to fit contents
            frame.grid(row=row, column=col, padx=5, pady=5)

            label = ttk.Label(frame, text=file, wraplength=130, anchor="center")
            label.place(relx=0.5, rely=0.5, anchor='center')
            
            if os.path.isdir(file_path):
                label.bind("<Double-Button-1>", lambda e, path=file_path: self.load_files(path))
            else:
                label.bind("<Double-Button-1>", lambda e, path=file_path: self.open_file(path))

            col += 1
            if col >= columns:
                col = 0
                row += 1
        # Reset scrollbar position to the top
        self.canvas.yview_moveto(0.0)

    def go_up(self):
        parent_dir = os.path.dirname(self.current_folder)
        if parent_dir and self.current_folder != self.firstfolder:
            self.load_files(parent_dir)

    def open_file(self, path):

        file_name, file_extension = os.path.splitext(path)

        if file_extension == ".vtf":
            texture = Texture(self.sdk)
            texture.open_VTF(path)
        elif file_extension == ".mdl":
            command = f'"{self.sdk.bin_folder}/hlmv.exe" "{path}"'
            subprocess.Popen(command)
        elif file_extension == ".vmf":
            command = f'"{self.sdk.bin_folder}/hammer.exe" "{path}"'
            subprocess.Popen(command)
        elif file_extension == ".vcd":
            command = f'"{self.sdk.bin_folder}/hlfaceposer.exe" "{path}"'
            subprocess.Popen(command)
        elif file_extension == ".bsp":
            command = f'"{self.sdk.executable_game}" -game "{self.sdk.selected_folder}" -console -dev -w 1280 -h 720 -sw +sv_cheats 1 +map {file_name}'
            subprocess.Popen(command)
        elif file_extension == ".vpk":
            vpk = VPK(self.sdk)
            vpk.display_vpk_contents(path)
        elif file_extension == ".tga":
            texture = Texture(self.sdk)
            texture.display_tga_file(path)
        else:
            try:
                os.startfile(path)
            except OSError as e:
                print("Error: Failed to open file:", e)

if __name__ == "__main__":
    image_folder = filedialog.askdirectory(title="Select a Directory")
    app = FileListApp(image_folder)
    app.mainloop()
