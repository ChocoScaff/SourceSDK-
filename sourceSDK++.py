import re
import string
import tkinter as tk
from turtle import st
from numpy import source
import srctools
import os
import subprocess
from tkinter import filedialog
import sys
import shutil

class SourceSDK():
    selected_folder : string
    bin_folder : string
    executable_game : string
    game_name : string
    first_init : bool
    def __init__(self):
        self.first_init = False


class Terminal(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tag_configure("stdout", foreground="black")
        self.tag_configure("stderr", foreground="red")

    def write(self, message):
        self.insert(tk.END, message)
        self.see(tk.END)

    def flush(self):
        pass

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

def bin_folder(folder_path):
    parent_folder = os.path.dirname(folder_path)
    bin_folder = parent_folder + "/bin"
    return bin_folder

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

def find_gameinfo_folder():
    # Recursively search through directories
    selected_folder = filedialog.askdirectory()
    
    gameinfo_path = os.path.join(selected_folder, "gameinfo.txt")

    if os.path.isfile(gameinfo_path):
        path = os.path.join(os.getcwd(), "scripts/vproject.bat")
        subprocess.call([path, selected_folder], shell=True)
        return selected_folder
    else:
        print("gameinfo.txt not found in selected folder.")
        return -1

def build_all_map():  
    path = os.path.join(os.getcwd(), "scripts/compile_map.bat")
    subprocess.call([path, sdk.selected_folder,sdk.game_name], shell=True)

def build_map():  

    mapsrc_directory = os.path.join(sdk.selected_folder, "mapsrc")
    map_directory = os.path.join(sdk.selected_folder, "maps")

    filenameVMF = filedialog.askopenfile(title="Select .vmf file", filetypes=[("VMF files", "*.vmf")])

    print("file =", filenameVMF.name)
    # Execute vbsp.exe

    fileBSP = filenameVMF.name
    #file_directory = os.path.dirname(fileBSP)
    fileBSP = os.path.splitext(os.path.basename(fileBSP))[0]

    # Create the new .bsp file path
    fileBSP = fileBSP + ".bsp"
    print("bsp =", fileBSP)


    print(sdk.bin_folder)

    vbsp = (sdk.bin_folder + "/vbsp.exe")
    command = ('"' + vbsp + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + filenameVMF.name + '"')
    print(command)
    #Execute the command in cmd
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

    vvis = (sdk.bin_folder + "/vvis.exe")
    command = ('"' + vvis + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

    vrad = (sdk.bin_folder + "/vrad.exe")
    command = ('"' + vrad + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

    try:
        os.makedirs(map_directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder: {e}")

    # Move bsp file to maps directory
    directoryBSP = mapsrc_directory + "/" + fileBSP
    shutil.move(directoryBSP, map_directory)
        
def build_all_texture():
    path = os.path.join(os.getcwd(), "scripts/compile_texture.bat")
    subprocess.call([path,sdk.selected_folder,sdk.game_name], shell=True)

def build_texture():
    filenameTGA = filedialog.askopenfile(title="Select .tga file", filetypes=[("TGA files", "*.tga")])
    vtex = (sdk.bin_folder + "/vtex.exe")
    command = ('"' + vtex + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + filenameTGA.name + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_model():
    filenameQC = filedialog.askopenfile(title="Select .qc file", filetypes=[("QC files", "*.qc")])
    vtex = (sdk.bin_folder + "/studiomdl.exe")
    command = ('"' + vtex + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + filenameQC.name + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_all_model():
    path = os.path.join(os.getcwd(), "scripts/compile_model.bat")
    subprocess.call([path,sdk.selected_folder,sdk.game_name], shell=True)

def build_caption():
    filenameTXT = filedialog.askopenfile(title="Select .txt file", filetypes=[("TXT files", "closecaption*.txt")])
    vtex = (sdk.bin_folder + "/captioncompiler.exe")
    command = ('"' + vtex + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + filenameTXT.name + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_all_caption():
    path = os.path.join(os.getcwd(), "scripts/compile_caption.bat")
    subprocess.call([path,sdk.selected_folder,sdk.game_name], shell=True)

def open_hammer():
    subprocess.Popen([sdk.bin_folder + "/hammer.exe"])

def open_hammer_plus_plus():
    subprocess.Popen([sdk.bin_folder + "/hammerplusplus.exe"])

def open_hlmv():
    subprocess.Popen([sdk.bin_folder + "/hlmv.exe"])

def open_qc_eyes():
    subprocess.Popen([sdk.bin_folder + "/qc_eyes.exe"])

def open_hlfaceposer():
    subprocess.Popen([sdk.bin_folder + "/hlfaceposer.exe"])

def particle():
    path = os.path.join(os.getcwd(), "scripts/particle.bat")
    subprocess.call([path,sdk.game_name,sdk.executable_game], shell=True)

def Launch_dev():
    path = os.path.join(os.getcwd(), "scripts/launch_dev.bat")
    subprocess.call([path,sdk.game_name,sdk.executable_game], shell=True)

def Launch():
    path = os.path.join(os.getcwd(), "scripts/launch.bat")
    subprocess.call([path,sdk.game_name,sdk.executable_game], shell=True)


def Init():
    print("Wait...")
    sdk.selected_folder = find_gameinfo_folder()
    if sdk.selected_folder == -1:
        return
    print("selected directory : " + sdk.selected_folder)

    sdk.executable_game = find_executable_game(sdk.selected_folder)
    print("executable game : " + sdk.executable_game)

    sdk.game_name = find_game_name(sdk.selected_folder)
    print("game name : " + sdk.game_name)

    sdk.bin_folder = bin_folder(sdk.selected_folder)
    print("bin directory : " + sdk.bin_folder)

    try:
        root.iconbitmap(sdk.selected_folder + '/resource/game.ico')
    except tk.TclError:
        print("Error: Failed to set icon.")
    
    print("Projet open")

    button_init()

def button_init():

    if sdk.first_init == True:
        return
    
    # Create "Build Map" button
    btn_build_map = tk.Button(root, text="Build all Maps", command=build_all_map)
    btn_build_map.pack()

    # Create "Build Texture" button
    btn_build_texture = tk.Button(root, text="Build all Textures", command=build_all_texture)
    btn_build_texture.pack()

    btn_build_model = tk.Button(root, text="Build all Models", command=build_all_model)
    btn_build_model.pack()

    btn_build_caption = tk.Button(root, text="Build all Captions", command=build_all_caption)
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

    sdk.first_init = True


sdk = SourceSDK() 

# Create the main window
root = tk.Tk()
root.title("Source SDK")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add "Open" option to the "File" menu
file_menu.add_command(label="Open", command=Init)
file_menu.add_command(label="Build Map", command=build_map)
file_menu.add_command(label="Build Texture", command=build_texture)
file_menu.add_command(label="Build Model", command=build_model)
file_menu.add_command(label="Build Caption", command=build_caption)

# Create a Text widget to display terminal output
terminal = Terminal(root, wrap=tk.WORD, height=30, width=90)
terminal.pack()

# Redirect sys.stdout and sys.stderr to the Terminal widget
sys.stdout = terminal
sys.stderr = terminal

lbl_result = tk.Label(root, text="Tools", wraplength=400)
lbl_result.pack()



# Start the GUI event loop
root.mainloop()
