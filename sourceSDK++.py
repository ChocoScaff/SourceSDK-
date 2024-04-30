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
from vtf2img import Parser
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
        command = "setx VProject " + '"' + selected_folder + '"'
        result = subprocess.run(command, shell=True)
        print(result)
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
    try:
        os.remove(map_directory + "/" + fileBSP)
    except os.error:
        print("cant remove :" + map_directory + "/" + fileBSP)
    
    shutil.move(directoryBSP, map_directory)
        
def build_all_texture():
    print("wait...")
    vtex = (sdk.bin_folder + "/vtex.exe")
    for root, dirs, files in os.walk(sdk.selected_folder + "/materialsrc"):
        for file in files:
            if file.endswith(".tga"):
                tga_file_path = os.path.join(root, file)
                command = ('"' + vtex + '"' + " -game " + '"' + sdk.selected_folder + '"' + " -nopause "  + '"' + tga_file_path + '"' )
                print(command)
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(result)

def build_texture():
    filenameTGA = filedialog.askopenfile(title="Select .tga file", filetypes=[("TGA files", "*.tga")])
    vtex = (sdk.bin_folder + "/vtex.exe")
    command = ('"' + vtex + '"' + " -game " + '"' + sdk.selected_folder + '"' + " -nopause "  + '"' + filenameTGA.name + '"' )
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_model():
    filenameQC = filedialog.askopenfile(title="Select .qc file", filetypes=[("QC files", "*.qc")])
    mdl = (sdk.bin_folder + "/studiomdl.exe")
    command = ('"' + mdl + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + filenameQC.name + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_all_model():
    print("wait...")
    mdl = (sdk.bin_folder + "/captioncompiler.exe")
    for root, dirs, files in os.walk(sdk.selected_folder + "/modelsrc"):
        for file in files:
            if file.endswith(".qc"):
                qc_file_path = os.path.join(root, file)
                command = ('"' + mdl + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + qc_file_path + '"')
                print(command)
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(result)

def build_caption():
    filenameTXT = filedialog.askopenfile(title="Select .txt file", filetypes=[("TXT files", "closecaption*.txt")])
    captioncompiler = (sdk.bin_folder + "/captioncompiler.exe")
    command = ('"' + captioncompiler + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + filenameTXT.name + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_all_caption():
    print("wait...")
    captioncompiler = (sdk.bin_folder + "/captioncompiler.exe")
    for root, dirs, files in os.walk(sdk.selected_folder + "/resource"):
        for file in files:
            if file.startswith("closecaption") and file.endswith(".txt"):
                caption_file_path = os.path.join(root, file)
                command = ('"' + captioncompiler + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + caption_file_path + '"')
                print(command)
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(result)

def open_hammer(file=""):
    subprocess.Popen([sdk.bin_folder + "/hammer.exe" + " " + file])

def open_hammer_plus_plus():
    subprocess.Popen([sdk.bin_folder + "/hammerplusplus.exe"])
    icon_path = "icons/hpp.png" // add icons
    icon_image = Image.open(icon_path)
    icon_image = icon_image.resize((32, 32),

def open_hlmv():
    subprocess.Popen([sdk.bin_folder + "/hlmv.exe"])

def open_qc_eyes():
    subprocess.Popen([sdk.bin_folder + "/qc_eyes.exe"])

def open_hlfaceposer():
    subprocess.Popen([sdk.bin_folder + "/hlfaceposer.exe"])

def particle():
    command = ('"' + sdk.executable_game + '"' + " -game " + sdk.game_name + " -tools -nop4 -w 1920 -h 1080 -dev ")
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def Launch_dev():
    command = ('"' + sdk.executable_game + '"' + " -game " + sdk.game_name + " -console -dev")
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def Launch():
    command = ('"' + sdk.executable_game + '"' + " -game " + sdk.game_name)
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)


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

    texture_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Texture", menu=texture_menu)
    map_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Map", menu=map_menu)
    model_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Model", menu=model_menu)
    other_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Other", menu=other_menu)

    map_menu.add_command(label="Build Map", command=build_map)
    map_menu.add_command(label="Build All Maps", command=build_all_map)
    texture_menu.add_command(label="Build Texture", command=build_texture)
    texture_menu.add_command(label="Build All Textures", command=build_all_texture)
    texture_menu.add_command(label="See Texture", command=open_vtf)

    model_menu.add_command(label="Build Model", command=build_model)
    model_menu.add_command(label="Build All Models", command=build_all_model)

    other_menu.add_command(label="Build Caption", command=build_caption)
    other_menu.add_command(label="Build All Captions", command=build_all_caption)


    sdk.first_init = True

def new_project():
    
    directory = filedialog.askdirectory(title="Select a Directory")
    game_name = find_game_name(directory)

    print(directory)
    print(game_name)
    if directory:
        files_in_dir = os.listdir(directory)
    
        # Check if the directory is empty
        if not files_in_dir:

            os.mkdir(directory + "/materialsrc")
            os.mkdir(directory + "/materials")
            os.mkdir(directory + "/models")
            os.mkdir(directory + "/modelsrc")
            os.mkdir(directory + "/bin")
            os.mkdir(directory + "/cfg")
            os.mkdir(directory + "/scripts")
            os.mkdir(directory + "/maps")
            os.mkdir(directory + "/mapsrc")
            os.mkdir(directory + "/resource")
            os.mkdir(directory + "/particles")
            os.mkdir(directory + "/sound")
            os.mkdir(directory + "/media")
            os.mkdir(directory + "/expressions")
            os.mkdir(directory + "/scenes")

            gameinfo_content = """
            "GameInfo"
            {
            game 		"replace"
            title 		"replace"
            type		singleplayer_only
            icon		"resource/game"

            FileSystem
            {
                SteamAppId		243730		// Source SDK Base 2013
                
                SearchPaths
                {
                    mod+mod_write+default_write_path		|gameinfo_path|.
                    game+game_write		replace
                    gamebin				replace/bin
                    Game				|gameinfo_path|.
                    Game				|all_source_engine_paths|replace
                }
            }
            }
            """

            # Write the content to the file
            gameinfo_content.replace("replace", game_name)
            gameInfo = directory + "/gameinfo.txt"
            try:
                with open(gameInfo, 'w') as file:
                    file.write(gameinfo_content.replace('replace', game_name))
                print(f"String saved to '{directory}' successfully.")
            except Exception as e:
                print(f"Error: {e}")

        else:
            print("The directory must be empty")
            
def view_vtf_image(file_path):

    parser = Parser(file_path)
    header = parser.header

    print(f"VTF version: {header.version}, Image size: {header.width}x{header.height}")
    # VTF version: 7.5, Image size: 2048x2048

    image = parser.get_image()

    image.show()   
        
def open_vtf():
    filenamevtf = filedialog.askopenfile(title="Select .vtf file", filetypes=[("VTF files", "*.vtf")])
    view_vtf_image(filenamevtf.name)

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
file_menu.add_command(label="New", command=new_project)
file_menu.add_command(label="Open", command=Init)


# Create a Text widget to display terminal output
terminal = Terminal(root, wrap=tk.WORD, height=20, width=80)
terminal.pack()

# Redirect sys.stdout and sys.stderr to the Terminal widget
sys.stdout = terminal
sys.stderr = terminal

lbl_result = tk.Label(root, text="Tools", wraplength=400)
lbl_result.pack()



# Start the GUI event loop
root.mainloop()
