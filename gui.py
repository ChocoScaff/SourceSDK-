import tkinter as tk
import srctools
import os
import subprocess
from tkinter import filedialog

def find_gameinfo_folder(start_dir):
    # Recursively search through directories
    selected_folder = filedialog.askdirectory()
    return selected_folder

def build_map():
    # Function to handle "Build Map" button click
    
    compile_map_path = os.path.join(selected_folder, "compile_map.bat")
    subprocess.call([compile_map_path], shell=True)
        

def build_texture():

    compile_texture_path = os.path.join(selected_folder, "compile_texture.bat")
    subprocess.call([compile_texture_path], shell=True)





# Start searching from the root directory (e.g., "C:\")
current_directory = os.getcwd()
print(current_directory)

selected_folder = find_gameinfo_folder(current_directory)

# Create the main window
root = tk.Tk()
root.title("Source SDK")

lbl_result = tk.Label(root, text="", wraplength=300)
lbl_result.pack()

# Create "Open Folder" button
#btn_open_folder = tk.Button(root, text="Open Folder", command=find_gameinfo_folder(current_directory))
#btn_open_folder.pack(pady=10)

# Create "Build Map" button
btn_build_map = tk.Button(root, text="Build Map", command=build_map)
btn_build_map.pack()

# Create "Build Texture" button
btn_build_texture = tk.Button(root, text="Build Texture", command=build_texture)
btn_build_texture.pack()



# Start the GUI event loop
root.mainloop()
