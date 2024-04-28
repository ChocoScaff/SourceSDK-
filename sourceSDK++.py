import tkinter as tk
import srctools
import os
import subprocess
from tkinter import filedialog

def parse_gameinfo_txt(file_path):
    #gameinfo_path = os.path.join(folder_path, "gameinfo.txt")
    print(file_path)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Example of parsing logic, modify as needed
                if "game" in line:
                    game_name = line.split('"')[1]
                    print("game", game_name)
                elif "FileSystem" in line:
                    # Example of parsing FileSystem section, modify as needed
                    # Assuming the next line contains the paths
                    next_line = next(file)
                    paths = next_line.strip().split('"')[1::2]
                    print("Paths:", paths)

def find_executable_game(folder_path):
    parent_folder = os.path.dirname(folder_path)
    executables = []
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith('.exe'):
                executables.append(os.path.join(root, file))
    #print(executables)
    return executables[0]

def find_game_name(folder_path):
    game_name = os.path.basename(folder_path)
    return game_name

def find_gameinfo_folder(start_dir):
    # Recursively search through directories
    selected_folder = filedialog.askdirectory()
    gameinfo_path = os.path.join(selected_folder, "gameinfo.txt")
    if os.path.isfile(gameinfo_path):
        path = os.path.join(os.getcwd(), "scripts/vproject.bat")
        subprocess.call([path, selected_folder], shell=True)
    else:
        print("gameinfo.txt not found in selected folder.")
        exit()
    return selected_folder

def build_map():  
    path = os.path.join(os.getcwd(), "scripts/compile_map.bat")
    subprocess.call([path, selected_folder,game_name], shell=True)
        
def build_texture():
    path = os.path.join(os.getcwd(), "scripts/compile_texture.bat")
    subprocess.call([path,selected_folder,game_name], shell=True)

def build_model():
    path = os.path.join(os.getcwd(), "scripts/compile_model.bat")
    subprocess.call([path,selected_folder,game_name], shell=True)

def build_caption():
    path = os.path.join(os.getcwd(), "scripts/compile_caption.bat")
    subprocess.call([path,selected_folder,game_name], shell=True)

def open_hammer():
    path = os.path.join(os.getcwd(), "scripts/hammer.bat")
    subprocess.call([path,selected_folder], shell=True)

def open_hammer_plus_plus():
    path = os.path.join(os.getcwd(), "scripts/hammer++.bat")
    subprocess.call([path,selected_folder], shell=True)

def open_hlmv():
    path = os.path.join(os.getcwd(), "scripts/hlmv.bat")
    subprocess.call([path,selected_folder], shell=True)

def open_qc_eyes():
    path = os.path.join(os.getcwd(), "scripts/qc_eyes.bat")
    subprocess.call([path,selected_folder], shell=True)

def open_hlfaceposer():
    path = os.path.join(os.getcwd(), "scripts/hlfaceposer.bat")
    subprocess.call([path,selected_folder], shell=True)

def particle():
    path = os.path.join(os.getcwd(), "scripts/particle.bat")
    subprocess.call([path,game_name,executable_game], shell=True)

def Launch_dev():
    path = os.path.join(os.getcwd(), "scripts/launch_dev.bat")
    subprocess.call([path,game_name,executable_game], shell=True)

def Launch():
    path = os.path.join(os.getcwd(), "scripts/launch.bat")
    subprocess.call([path,game_name,executable_game], shell=True)

# Start searching from the root directory (e.g., "C:\")
current_directory = os.getcwd()
print("current directory : " + current_directory)

selected_folder = find_gameinfo_folder(current_directory)
print("selected directory : " + selected_folder)

executable_game = find_executable_game(selected_folder)
print("executable game : " + executable_game)

game_name = find_game_name(selected_folder)
print("game name : " + game_name)

# Create the main window
root = tk.Tk()
root.title("Source SDK")

lbl_result = tk.Label(root, text="", wraplength=300)
lbl_result.pack()

# Create "Open Folder" button
#btn_open_folder = tk.Button(root, text="Open Folder", command=find_gameinfo_folder(current_directory))
#btn_open_folder.pack(pady=10)

# Create "Build Map" button
btn_build_map = tk.Button(root, text="Build Maps", command=build_map)
btn_build_map.pack()

# Create "Build Texture" button
btn_build_texture = tk.Button(root, text="Build Textures", command=build_texture)
btn_build_texture.pack()

btn_build_model = tk.Button(root, text="Build Models", command=build_model)
btn_build_model.pack()

btn_build_caption = tk.Button(root, text="Build Captions", command=build_caption)
btn_build_caption.pack()

btn_hammer = tk.Button(root, text="hammer", command=open_hammer)
btn_hammer.pack()

btn_open_hammer_plus_plus = tk.Button(root, text="hammer++", command=open_hammer_plus_plus)
btn_open_hammer_plus_plus.pack()

btn_hlmv = tk.Button(root, text="hlmv", command=open_hlmv)
btn_hlmv.pack()

btn_hlmv = tk.Button(root, text="qc_eyes", command=open_qc_eyes)
btn_hlmv.pack()

btn_hlfaceposer = tk.Button(root, text="hlfaceposer", command=open_hlfaceposer)
btn_hlfaceposer.pack()

btn_particle = tk.Button(root, text="Particle", command=particle)
btn_particle.pack()

btn_Launch_dev = tk.Button(root, text="Launch Dev", command=Launch_dev)
btn_Launch_dev.pack()

btn_Launch = tk.Button(root, text="Launch", command=Launch)
btn_Launch.pack()

# Start the GUI event loop
root.mainloop()
