from asyncio.windows_events import NULL
import string
import tkinter as tk
from turtle import st
from click import open_file
import srctools
import os
import subprocess
from tkinter import Listbox, filedialog
import sys
from vtf2img import Parser
import shutil
import git
import ctypes as ct
import urllib.request
import json
import webbrowser
from tkinter import messagebox

class SourceSDK():
    selected_folder : string
    bin_folder : string
    executable_game : string
    game_name : string
    first_init : bool
    btn_hammer : tk.Button
    btn_hammer_plus_plus : tk.Button
    btn_hlmv : tk.Button
    btn_hlfaceposer : tk.Button
    btn_qc_eyes : tk.Button
    btn_games : tk.Button
    btn_everything : tk.Button
    btn_particle : tk.Button
    btn_Launch : tk.Button
    btn_Launch_dev : tk.Button
    other_menu : tk.Menu
    texture_menu : tk.Menu
    map_menu : tk.Menu
    model_menu : tk.Menu
    menu_bar : tk.Menu
    scrollbar : tk.Scrollbar
    listbox : tk.Listbox

    def __init__(self):
        self.first_init = 0

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
    binFolder = parent_folder + "/bin"
    if os.path.exists(binFolder):
        pass
    else:
        #with open(folder_path + "bin.txt", 'r') as file:   
        folder = filedialog.askdirectory(title="Open bin Engine path",initialdir=parent_folder)
        binFolder = bin_folder(folder)
    return binFolder

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
    print("wait...")
    mapsrc_directory = os.path.join(sdk.selected_folder, "mapsrc")
    map_directory = os.path.join(sdk.selected_folder, "maps")
    vbsp = (sdk.bin_folder + "/vbsp.exe")
    vvis = (sdk.bin_folder + "/vvis.exe")
    vrad = (sdk.bin_folder + "/vrad.exe")

    try:
        os.makedirs(map_directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder: {e}")

    for root, dirs, files in os.walk(sdk.selected_folder + "/mapsrc"):
        for file in files:
            if file.endswith(".vmf"):
                    vmf_file_path = os.path.join(root, file)
                    command = ('"' + vbsp + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + vmf_file_path + '"')
                    print(command)
                    #Execute the command in cmd
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result)

                    fileBSP = vmf_file_path
                    #file_directory = os.path.dirname(fileBSP)
                    fileBSP = os.path.splitext(os.path.basename(fileBSP))[0]

                    # Create the new .bsp file path
                    fileBSP = fileBSP + ".bsp"

                    command = ('"' + vvis + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
                    print(command)
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result)

                    command = ('"' + vrad + '"' + " -game " + '"' + sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
                    print(command)
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result)

                    # Move bsp file to maps directory
                    directoryBSP = mapsrc_directory + "/" + fileBSP
                    try:
                        os.remove(map_directory + "/" + fileBSP)
                    except os.error:
                        print("cant remove :" + map_directory + "/" + fileBSP)
                    
                    shutil.move(directoryBSP, map_directory)

def build_map():  

    mapsrc_directory = os.path.join(sdk.selected_folder, "mapsrc")
    map_directory = os.path.join(sdk.selected_folder, "maps")

    filenameVMF = filedialog.askopenfile(title="Select .vmf file", filetypes=[("VMF files", "*.vmf")], initialdir=mapsrc_directory)

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
    filenameTGA = filedialog.askopenfile(title="Select .tga file", filetypes=[("TGA files", "*.tga")], initialdir=sdk.selected_folder + "/materialsrc")
    vtex = (sdk.bin_folder + "/vtex.exe")
    command = ('"' + vtex + '"' + " -game " + '"' + sdk.selected_folder + '"' + " -nopause "  + '"' + filenameTGA.name + '"' )
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_model():
    filenameQC = filedialog.askopenfile(title="Select .qc file", filetypes=[("QC files", "*.qc")], initialdir=sdk.selected_folder + "/modelsrc")
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
    filenameTXT = filedialog.askopenfile(title="Select .txt file", filetypes=[("TXT files", "closecaption*.txt")], initialdir=sdk.selected_folder + "/resource")
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

def open_hlmv():
    subprocess.Popen([sdk.bin_folder + "/hlmv.exe"])

def open_qc_eyes():
    subprocess.Popen([sdk.bin_folder + "/qc_eyes.exe"])

def open_hlfaceposer():
    subprocess.Popen([sdk.bin_folder + "/hlfaceposer.exe"])

def particle():
    command = ('"' + sdk.executable_game + '"' + " -game " + '"' + sdk.selected_folder + '"' + " -tools -nop4 -dev -sw -console")
    print(command)
    subprocess.Popen(command)

def Launch_dev():
    command = ('"' + sdk.executable_game + '"' + " -game " + '"' + sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720 -usercon -sw +sv_cheats 1")
    print(command)
    subprocess.Popen(command)

def Launch():
    command = ('"' + sdk.executable_game + '"' + " -game " + '"' + sdk.selected_folder + '"')
    print(command)
    subprocess.Popen(command)


def Init(folder=False):
    print("Wait...")

    if folder == False:
        if sdk.first_init == 1:
            reload_button()
        sdk.selected_folder = find_gameinfo_folder()
        if sdk.selected_folder == -1:
            return
    else:
        if sdk.first_init == 1:
            reload_button()
        sdk.selected_folder=folder

    print("selected directory : " + sdk.selected_folder)

    sdk.game_name = find_game_name(sdk.selected_folder)
    print("game name : " + sdk.game_name)

    sdk.bin_folder = bin_folder(sdk.selected_folder)
    print("bin directory : " + sdk.bin_folder)

    sdk.executable_game = find_executable_game(sdk.bin_folder)
    print("executable game : " + sdk.executable_game)

    try:
        root.iconbitmap(sdk.selected_folder + '/resource/game.ico')
    except tk.TclError:
        print("Error: Failed to set icon.")
    
    print("Project open")

    Launch_dev()

    lbl_result = tk.Label(root, text="Tools", wraplength=400, background="#3e4637",fg='white')
    lbl_result.pack()

    button_init()

    display_files()

def button_init():

    if os.path.isfile(sdk.bin_folder + "/hammer.exe"):
        sdk.btn_hammer = tk.Button(root, text="hammer", command=open_hammer,image=iconHammer,compound=tk.LEFT, background="#4c5844",fg="white")
        sdk.btn_hammer.pack(side="left")
    
    if os.path.isfile(sdk.bin_folder + "/hammerplusplus.exe"):
        sdk.btn_hammer_plus_plus = tk.Button(root, text="hammer++", command=open_hammer_plus_plus, image=iconHpp, compound=tk.LEFT, background="#4c5844",fg="white")    
        sdk.btn_hammer_plus_plus.pack(side="left")

    if os.path.isfile(sdk.bin_folder + "/hlmv.exe"):
        sdk.btn_hlmv = tk.Button(root, text="hlmv", command=open_hlmv, image=iconHLMV, compound=tk.LEFT, background="#4c5844",fg="white")
        sdk.btn_hlmv.pack(side="left")

    if os.path.isfile(sdk.bin_folder + "/qc_eyes.exe"):
        sdk.btn_qc_eyes= tk.Button(root, text="qc_eyes", command=open_qc_eyes, image=iconQc_eyes, compound=tk.LEFT, background="#4c5844",fg="white")
        sdk.btn_qc_eyes.pack(side="left")

    if os.path.isfile(sdk.bin_folder + "/hlfaceposer.exe"):
        sdk.btn_hlfaceposer = tk.Button(root, text="hlfaceposer", command=open_hlfaceposer, image=iconHlposer, compound=tk.LEFT, background="#4c5844",fg="white")
        sdk.btn_hlfaceposer.pack(side="left")

    if os.path.exists(sdk.selected_folder + "/src/games.sln"):
        sdk.btn_games = tk.Button(root, text="games", command=open_games, image=iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
        sdk.btn_games.pack(side="left")

    if os.path.exists(sdk.selected_folder + "/src/everything.sln"):
        sdk.btn_everything = tk.Button(root, text="everything", command=open_everything, image=iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
        sdk.btn_everything.pack(side="left")

    sdk.btn_particle = tk.Button(root, text="Particle", command=particle, image=iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
    sdk.btn_particle.pack(side="left")

    sdk.btn_Launch_dev = tk.Button(root, text="Launch Dev", command=Launch_dev, image=iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
    sdk.btn_Launch_dev.pack(side="left")

    sdk.btn_Launch = tk.Button(root, text="Launch", command=Launch, image=iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
    sdk.btn_Launch.pack(side="left")

    if sdk.first_init == 0:
        sdk.texture_menu = tk.Menu(sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        sdk.menu_bar.add_cascade(label="Texture", menu=sdk.texture_menu)
        sdk.map_menu = tk.Menu(sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        sdk.menu_bar.add_cascade(label="Map", menu=sdk.map_menu)
        sdk.model_menu = tk.Menu(sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        sdk.menu_bar.add_cascade(label="Model", menu=sdk.model_menu)
        sdk.other_menu = tk.Menu(sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        sdk.menu_bar.add_cascade(label="Other", menu=sdk.other_menu)

        sdk.map_menu.add_command(label="Build Map", command=build_map)
        sdk.map_menu.add_command(label="Build All Maps", command=build_all_map)
        sdk.map_menu.add_command(label="Info Map", command=info_map)

        sdk.texture_menu.add_command(label="Build Texture", command=build_texture)
        sdk.texture_menu.add_command(label="Build All Textures", command=build_all_texture)
        sdk.texture_menu.add_command(label="See Texture", command=open_vtf)
        sdk.texture_menu.add_command(label="Texture To TGA", command=texture_to_tga)
        sdk.texture_menu.add_command(label="Generate vmt", command=generate_vmt)

        sdk.model_menu.add_command(label="Build Model", command=build_model)
        sdk.model_menu.add_command(label="Build All Models", command=build_all_model)
        sdk.model_menu.add_command(label="Generate QC File", command=generate_qc_file)

        sdk.other_menu.add_command(label="Create VPK", command=create_VPK)
        sdk.other_menu.add_command(label="Display VPK", command=display_VPK)
        sdk.other_menu.add_command(label="Extract VPK", command=extract_VPK)
        sdk.other_menu.add_command(label="Build Caption", command=build_caption)
        sdk.other_menu.add_command(label="Build All Captions", command=build_all_caption)

        #if os.path.exists(sdk.selected_folder + "/src/creategameprojects.bat"):
        sdk.other_menu.add_command(label="Generate games", command=generate_games)

        #if os.path.exists(sdk.selected_folder + "/src/createallprojects.bat"):
        sdk.other_menu.add_command(label="Generate everything", command=generate_everything)

        sdk.other_menu.add_command(label="Download source code", command=downbload_source_code)

    sdk.first_init = 1

def reload_button():
    print("reload")   

    if os.path.isfile(sdk.bin_folder + "/hammer.exe"):
        sdk.btn_hammer.destroy()
    if os.path.isfile(sdk.bin_folder + "/hammerplusplus.exe"):
        sdk.btn_hammer_plus_plus.destroy()
    if os.path.isfile(sdk.bin_folder + "/qc_eyes.exe"):
        sdk.btn_qc_eyes.destroy()
    if os.path.exists(sdk.selected_folder + "/src/everything.sln"):
        sdk.btn_everything.destroy()
    if os.path.exists(sdk.selected_folder + "/src/games.sln"):
        sdk.btn_games.destroy()
    if os.path.isfile(sdk.bin_folder + "/hlmv.exe"):
        sdk.btn_hlmv.destroy()
    if os.path.isfile(sdk.bin_folder + "/hlfaceposer.exe"):
        sdk.btn_hlfaceposer.destroy()

    sdk.btn_Launch.destroy()
    sdk.btn_particle.destroy()
    sdk.btn_Launch_dev.destroy()

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
            os.mkdir(directory + "/src")

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
            
            Init(directory)

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
    filenamevtf = filedialog.askopenfile(title="Select .vtf file", filetypes=[("VTF files", "*.vtf")], initialdir=sdk.selected_folder + "/materials")
    view_vtf_image(filenamevtf.name)

# Function to handle keyboard shortcuts
def handle_shortcut(event):
    key = event.keysym
    if key == "n":
        new_project()
    elif key == "o":
        Init()

def info_map():
    filenamevmf = filedialog.askopenfile(title="Select .vmf file", filetypes=[("VMF files", "*.vmf")], initialdir=sdk.selected_folder + "/mapsrc")
    vmf = srctools.VMF.parse(filenamevmf.name)
    entities = vmf.entities
    print("Number of entities in the VMF:", len(entities))
    print(entities)
    cameras = vmf.cameras
    print("Number of cameras in the VMF:", len(cameras))
    print(cameras)

def launch_exit():
    exit()

def create_VPK():
    directory = filedialog.askdirectory(title="Select a Directory")
    command = '"' + sdk.bin_folder + "/vpk.exe" + '" ' + '"' + directory + '"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def extract_VPK():
    filenamevpk = filedialog.askopenfile(title="Select .vpk file", filetypes=[("VPK files", "*.vpk")], initialdir=sdk.selected_folder)
    command = '"' + sdk.bin_folder + "/vpk.exe" + '" ' + '"' + filenamevpk.name + '"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def display_VPK():
    filenamevpk = filedialog.askopenfile(title="Select .vpk file", filetypes=[("VPK files", "*.vpk")], initialdir=sdk.selected_folder)
    command = '"' + sdk.bin_folder + "/vpk.exe" + '"' + " L " + '"' + filenamevpk.name + '"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def open_about_window():
    # Create a new window for about information
    about_window = tk.Toplevel(root)
    about_window.title("About")

    # Add text to the window
    about_text = tk.Label(about_window, text="Software create by ChocoScaff.\nYou can find source code.\nhttps://github.com/ChocoScaff/SourceSDK-")
    about_text.pack()

def open_sln_file(sln_file_path):
    
    # Check if the .sln file exists
    if os.path.exists(sln_file_path):
        # Open the .sln file with the default application
        os.startfile(sln_file_path)
    else:
        print("Error: .sln file not found!")

def open_games():
    open_sln_file(sdk.selected_folder + "/src/games.sln")

def open_everything():
    open_sln_file(sdk.selected_folder + "/src/everything.sln")

def generate_games():
    command = f'cd /D "{sdk.selected_folder}\\src" && creategameprojects.bat'
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def generate_everything():
    command = f'cd /D "{sdk.selected_folder}\\src" && createallprojects.bat'
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def downbload_source_code():

    download_github_code("https://github.com/ValveSoftware/source-sdk-2013", sdk.selected_folder + "/src/")

    shutil.rmtree(sdk.selected_folder + "/src/mp/")
    move_files(sdk.selected_folder + "/src/sp/src/", sdk.selected_folder + "/src/")
    shutil.rmtree(sdk.selected_folder + "/src/sp/")

    generate_games()
    generate_everything()

    Init()

def download_github_code(repo_url, destination_folder):
    git.Repo.clone_from(repo_url, destination_folder)

def move_files(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get a list of all files in the source folder
    files = os.listdir(source_folder)

    # Move each file to the destination folder
    for file in files:
        source_file = os.path.join(source_folder, file)
        destination_file = os.path.join(destination_folder, file)
        shutil.move(source_file, destination_file)


def get_latest_release_version(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            latest_version = data['tag_name']
            return latest_version
    except Exception as e:
        return f"Error: {e}"

def check_software_version(local_version, github_version):
    if local_version == github_version:
        print("You have the latest version installed.")
    else:
        print(f"There is a newer version ({github_version}) available on GitHub.")

def SDK_Doc():
    webbrowser.open("https://developer.valvesoftware.com/wiki/SDK_Docs")

def generate_qc_file():

    filenameModel = filedialog.askopenfile(title="Select .smd or .dmx file", filetypes=[("model file", "*.smd *.dmx")], initialdir=sdk.selected_folder + "/modelsrc")
    print(filenameModel)
    print(filenameModel.name)
    TexureDirectory = filedialog.askdirectory(title="Select Texure Directory",initialdir=sdk.selected_folder + "/materials/models")
    print(TexureDirectory)

    popup = tk.Toplevel(root)
    popup.title("Material Selector")

    materials = ["Concrete", "Wood", "Dirt", "Grass", "Water", "Ice", "Metal", "Sand", "Rock"]

    selected_materialTK = tk.StringVar()

    def select_material(material):
        selected_materialTK.set(material)
        popup.destroy() 

    for material in materials:
        button = tk.Button(popup, text=material, command=lambda m=material: select_material(m))
        button.pack()

    popup.wait_window()

    selected_material = selected_materialTK.get()

    qc_file="""
$modelname "modelNameToReplace"
$cdmaterials "textureDirectoryToReplace"
$collisionmodel	"modelToReplace"
$sequence idle	"modelToReplace"
$body bodystrToReplace "modelToReplace"
$surfaceprop sufaceReplace
$scale 1
    """

    modelNamestr = filenameModel.name[filenameModel.name.find("/modelsrc/") + 10:]
    texturestr = TexureDirectory[TexureDirectory.find("/materials/") + 11:]
    modelstr =modelNamestr[modelNamestr.find('/') + 1:]
    bodystr = modelstr[:-4]

    qc_file = qc_file.replace("modelNameToReplace",modelNamestr)
    qc_file = qc_file.replace("textureDirectoryToReplace",texturestr)
    qc_file = qc_file.replace("bodystrToReplace",bodystr)
    qc_file = qc_file.replace("sufaceReplace",selected_material)
    qc_file = qc_file.replace("modelToReplace",modelstr)

    print(qc_file)

    fileQC = sdk.selected_folder + "/modelsrc/" + modelNamestr[:-4] + ".qc"
    print(fileQC)

    try:
        with open(fileQC, 'w') as file:
            file.write(qc_file)
        print(f"String saved to '{filenameModel}' successfully.")
    except Exception as e:
        print(f"Error: {e}")

def texture_to_tga():
    filenameVTF = filedialog.askopenfile(title="Select .vtf file", filetypes=[("VTF file", "*.vtf")], initialdir=sdk.selected_folder + "/materials")
    command = '"' + sdk.bin_folder + "/vtf2tga.exe" + '"'+ " -i " + '"' + filenameVTF.name + '"' 
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def generate_vmt():

    filenameVMTs = filedialog.askopenfilenames(title="Select .vtf file", filetypes=[("texture file", "*.vtf")], initialdir=sdk.selected_folder + "/materials")

    diffuse_texture = NULL
    normal_texture = NULL
    if len(filenameVMTs) == 1:
        print(filenameVMTs)
        vtfName = str(filenameVMTs)
        print(vtfName)
        diffuse_texture = vtfName[:-3]
    else:
        for vmt in filenameVMTs:
            print(vmt)
            if "diffuse" in vmt.lower():
                diffuse_texture = vmt
            elif "normal" in vmt.lower():
                normal_texture = vmt

    popup = tk.Toplevel(root)
    popup.title("shader Selector")

    shaders = ["LightmappedGeneric", "VertexLitGeneric", "WorldVertexTransition", "UnlitGeneric", "Sky"]

    selected_shaderTK = tk.StringVar()

    def select_shader(shader):
        selected_shaderTK.set(shader)
        popup.destroy() 

    for shader in shaders:
        button = tk.Button(popup, text=shader, command=lambda m=shader: select_shader(m))
        button.pack()

    popup.wait_window()

    selected_shader = selected_shaderTK.get()

    vmt="""
"shader"
{
	"$basetexture" "texture_diffuse"
    "$normalmap" "texture_normal"
}
"""
    vmt = vmt.replace("shader",selected_shader)

    diffuse_texture = diffuse_texture[diffuse_texture.find("/materials/") + 11:]
    vmt = vmt.replace("texture_diffuse",diffuse_texture)
    if normal_texture != NULL:
        normal_texture = normal_texture[normal_texture.find("/materials/") + 11:]
        vmt = vmt.replace("texture_normal",normal_texture)
    else:
        vmt = vmt.replace('"$normalmap" "texture_normal"',"")

    print(vmt)

    fileVMT = sdk.selected_folder + "/materials/" + diffuse_texture[:-4] + ".vmt"
    fileVMT = str(fileVMT)
    fileVMT = fileVMT.replace("_diffuse", "")
    
    print(fileVMT)

    try:
        with open(fileVMT, 'w') as file:
            file.write(vmt)
        print(f"String saved to '{fileVMT}' successfully.")
    except Exception as e:
        print(f"Error: {e}")

def list_files():
    target_extensions = [".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp"]
    files = []
    for root, dirs, files_in_dir in os.walk(sdk.selected_folder):
        for file_name in files_in_dir:
            for ext in target_extensions:
                if file_name.endswith(ext):
                    files.append(os.path.relpath(os.path.join(root, file_name), sdk.selected_folder))
    files.sort()  # Sort files alphabetically
    return files

def display_files():
    files = list_files()

    # Création du widget Listbox
    sdk.listbox = Listbox(root)
    
    # Création du widget Scrollbar
    sdk.scrollbar = tk.Scrollbar(root)
    
    # Configure the Listbox to use the Scrollbar
    sdk.listbox.config(yscrollcommand=sdk.scrollbar.set)
    sdk.scrollbar.config(command=sdk.listbox.yview)

    sdk.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sdk.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Insert files into the Listbox
    for file in files:
        sdk.listbox.insert(tk.END, file)
    
    sdk.listbox.bind("<Double-Button-1>", open_file)

def open_file(event):
    selected_index = sdk.listbox.curselection()
    
    if selected_index:
        file = sdk.listbox.get(selected_index)
        file_name, file_extension = os.path.splitext(file)
        print(file)
        open_file_source_extension(file_extension,sdk.selected_folder + "/" + file, file[5:-4])

def open_file_source_extension(file_extension, filepath, file):
    if file_extension == ".vtf":   
        try:
            os.startfile(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
        view_vtf_image(filepath)
        
    elif file_extension == ".mdl":
        command = '"' + sdk.bin_folder + "/hlmv.exe" + '"'+ ' "' + filepath + '"' 
        subprocess.Popen(command)
    elif file_extension == ".vmf":
        #subprocess.Popen([sdk.bin_folder + "/hammer.exe" + ' "' + file + '"'])
        command = '"' + sdk.bin_folder + "/hammer.exe" + '"'+ ' "' + filepath + '"' 
        subprocess.Popen(command)
    elif file_extension == ".vcd":
        command = '"' + sdk.bin_folder + "/hlfaceposer.exe" + '"'+ ' "' + filepath + '"' 
        subprocess.Popen(command)
    elif file_extension == ".bsp":
        command = ('"' + sdk.executable_game + '"' + " -game " + '"' + sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720  -sw +sv_cheats 1 +map " + file)
        print(command)
        subprocess.Popen(command)
    else:
        try:
            os.startfile(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

# Replace these with your GitHub repository owner and name
repo_owner = "ChocoScaff"
repo_name = "SourceSDK-"

# Replace this with the version of your local software
local_version = "0.1.2"

github_version = get_latest_release_version(repo_owner, repo_name)

if github_version:
    check_software_version(local_version, github_version)
else:
    print("Failed to fetch the latest version from GitHub.")
    download = messagebox.askyesno("New Version Available", f"There is a newer version ({github_version}) available on GitHub. Do you want to download it?")
    if download:
        webbrowser.open(f"https://github.com/{repo_owner}/{repo_name}/releases/latest")
    else:
        messagebox.showinfo("Version Check", "You chose not to download the new version.")

sdk = SourceSDK()

# Create the main window
root = tk.Tk()
root.title("Source SDK")

root.tk_setPalette(background="#4c5844", foreground="white")

root.configure(background="#3e4637")

sdk.menu_bar = tk.Menu(root)
root.config(menu=sdk.menu_bar,background="#3e4637")

# Create a "File" menu
file_menu = tk.Menu(sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
sdk.menu_bar.add_cascade(label="File", menu=file_menu)

# Add "Open" option to the "File" menu
file_menu.add_command(label="New", command=new_project, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=Init, accelerator="Ctrl+O")
#previous_projects_menu = tk.Menu(file_menu, tearoff=0)
#file_menu.add_cascade(label="Previous Projects", menu=previous_projects_menu)
file_menu.add_command(label="Exit", command=launch_exit)

help_menu = tk.Menu(sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
sdk.menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="SDK Doc", command=SDK_Doc)
help_menu.add_command(label="About", command=open_about_window)

# Create a Text widget to display terminal output
terminal = Terminal(root, wrap=tk.WORD, height=20, width=80)
terminal.pack()

# Redirect sys.stdout and sys.stderr to the Terminal widget
sys.stdout = terminal
sys.stderr = terminal

# Bind keyboard shortcuts to the root window
root.bind("<Control-n>", handle_shortcut)
root.bind("<Control-o>", handle_shortcut)

iconHpp = tk.PhotoImage(file=os.getcwd() + "/icons/hpp.png")
iconHammer = tk.PhotoImage(file=os.getcwd() + "/icons/hammer.png")
iconSource = tk.PhotoImage(file=os.getcwd() + "/icons/source.png")
iconHLMV = tk.PhotoImage(file=os.getcwd() + "/icons/hlmv.png")
iconQc_eyes = tk.PhotoImage(file=os.getcwd() + "/icons/qc_eyes.png")
iconHlposer = tk.PhotoImage(file=os.getcwd() + "/icons/hlposer.png")
iconVisualStudio = tk.PhotoImage(file=os.getcwd() + "/icons/Visual_Studio.png")

# Start the GUI event loop
root.mainloop()
