import string
import tkinter as tk
import os
import subprocess
from tkinter import Listbox, filedialog
import sys
import shutil
import git
import urllib.request
import json
import webbrowser
from tkinter import messagebox
import requests
import zipfile

from sourceSDK import SourceSDK
from texture import Texture
from model import Model
from map import Map
from vpk import VPK

class Test():
    sdk : SourceSDK
    texure : Texture
    model : Model
    map : Map
    vpk : VPK


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


def build_caption():
    filenameTXT = filedialog.askopenfile(title="Select .txt file", filetypes=[("TXT files", "closecaption*.txt")], initialdir=test.sdk.selected_folder + "/resource")
    captioncompiler = (test.sdk.bin_folder + "/captioncompiler.exe")
    command = ('"' + captioncompiler + '"' + " -game " + '"' + test.sdk.selected_folder + '"' + " " + '"' + filenameTXT.name + '"')
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def build_all_caption():
    print("wait...")
    captioncompiler = (test.sdk.bin_folder + "/captioncompiler.exe")
    for root, dirs, files in os.walk(test.sdk.selected_folder + "/resource"):
        for file in files:
            if file.startswith("closecaption") and file.endswith(".txt"):
                caption_file_path = os.path.join(root, file)
                command = ('"' + captioncompiler + '"' + " -game " + '"' + test.sdk.selected_folder + '"' + " " + '"' + caption_file_path + '"')
                print(command)
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(result)

def open_hammer(file=""):
    subprocess.Popen([test.sdk.bin_folder + "/hammer.exe" + " " + file])

def open_hammer_plus_plus():
    subprocess.Popen([test.sdk.bin_folder + "/hammerplusplus.exe"])

def open_qc_eyes():
    subprocess.Popen([test.sdk.bin_folder + "/qc_eyes.exe"])

def open_hlfaceposer():
    subprocess.Popen([test.sdk.bin_folder + "/hlfaceposer.exe"])

def particle():
    command = ('"' + test.sdk.executable_game + '"' + " -game " + '"' + test.sdk.selected_folder + '"' + " -tools -nop4 -dev -sw -console")
    print(command)
    subprocess.Popen(command)

def Launch_dev():
    command = ('"' + test.sdk.executable_game + '"' + " -game " + '"' + test.sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720 -usercon -sw +sv_cheats 1")
    print(command)
    subprocess.Popen(command)

def Launch():
    command = ('"' + test.sdk.executable_game + '"' + " -game " + '"' + test.sdk.selected_folder + '"')
    print(command)
    subprocess.Popen(command)


def Init(folder=False):
    print("Wait...")

    if folder == False:
        if test.sdk.first_init == 1:
            reload_button()
        test.sdk.selected_folder = find_gameinfo_folder()
        if test.sdk.selected_folder == -1:
            return
    else:
        if test.sdk.first_init == 1:
            reload_button()
        test.sdk.selected_folder=folder

    print("selected directory : " + test.sdk.selected_folder)

    test.sdk.game_name = find_game_name(test.sdk.selected_folder)
    print("game name : " + test.sdk.game_name)

    test.sdk.bin_folder = bin_folder(test.sdk.selected_folder)
    print("bin directory : " + test.sdk.bin_folder)

    test.sdk.executable_game = find_executable_game(test.sdk.bin_folder)
    print("executable game : " + test.sdk.executable_game)

    """
    try:
        test.sdk.root.iconbitmap(test.sdk.selected_folder + '/resource/game.ico')
    except tk.TclError:
        print("Error: Failed to set icon.")
    """
    print("Project open")

    Launch_dev()

    lbl_result = tk.Label(test.sdk.root, text="Tools", wraplength=400, background="#3e4637",fg='white')
    lbl_result.pack()

    test.texture = Texture(test.sdk)
    test.model = Model(test.sdk)
    test.map = Map(test.sdk)
    test.vpk = VPK(test.sdk)

    button_init()

    display_files()

def button_init():

    if os.path.isfile(test.sdk.bin_folder + "/hammer.exe"):
        test.sdk.btn_hammer = tk.Button(test.sdk.root, text="hammer", command=open_hammer,image=iconHammer,compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_hammer.pack(side="left")
    
    if os.path.isfile(test.sdk.bin_folder + "/hammerplusplus.exe"):
        test.sdk.btn_hammer_plus_plus = tk.Button(test.sdk.root, text="hammer++", command=open_hammer_plus_plus, image=iconHpp, compound=tk.LEFT, background="#4c5844",fg="white")    
        test.sdk.btn_hammer_plus_plus.pack(side="left")

    if os.path.isfile(test.sdk.bin_folder + "/hlmv.exe"):
        test.sdk.btn_hlmv = tk.Button(test.sdk.root, text="hlmv", command=test.model.open_hlmv, image=iconHLMV, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_hlmv.pack(side="left")

    if os.path.isfile(test.sdk.bin_folder + "/qc_eyes.exe"):
        test.sdk.btn_qc_eyes= tk.Button(test.sdk.root, text="qc_eyes", command=open_qc_eyes, image=iconQc_eyes, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_qc_eyes.pack(side="left")

    if os.path.isfile(test.sdk.bin_folder + "/hlfaceposer.exe"):
        test.sdk.btn_hlfaceposer = tk.Button(test.sdk.root, text="hlfaceposer", command=open_hlfaceposer, image=iconHlposer, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_hlfaceposer.pack(side="left")

    if os.path.isfile(os.getcwd() + "/VTfEdit/x64/VTFEdit.exe"):
        test.sdk.btn_vtf_edit = tk.Button(test.sdk.root, text="vtfEdit", command=test.texture.open_VTF, image=iconVTFEdit, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_vtf_edit.pack(side="left")
    else:
        download_VTF_Edit()
        test.sdk.btn_vtf_edit = tk.Button(test.sdk.root, text="vtfEdit", command=test.texture.open_VTF, image=iconVTFEdit, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_vtf_edit.pack(side="left")
    
    if os.path.exists(test.sdk.selected_folder + "/src/games.sln"):
        test.sdk.btn_games = tk.Button(test.sdk.root, text="games", command=open_games, image=iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_games.pack(side="left")

    if os.path.exists(test.sdk.selected_folder + "/src/everything.sln"):
        test.sdk.btn_everything = tk.Button(test.sdk.root, text="everything", command=open_everything, image=iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
        test.sdk.btn_everything.pack(side="left")

    test.sdk.btn_particle = tk.Button(test.sdk.root, text="Particle", command=particle, image=iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
    test.sdk.btn_particle.pack(side="left")

    test.sdk.btn_Launch_dev = tk.Button(test.sdk.root, text="Launch Dev", command=Launch_dev, image=iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
    test.sdk.btn_Launch_dev.pack(side="left")

    test.sdk.btn_Launch = tk.Button(test.sdk.root, text="Launch", command=Launch, image=iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
    test.sdk.btn_Launch.pack(side="left")

    if test.sdk.first_init == 0:
        test.sdk.texture_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        test.sdk.menu_bar.add_cascade(label="Texture", menu=test.sdk.texture_menu)
        test.sdk.map_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        test.sdk.menu_bar.add_cascade(label="Map", menu=test.sdk.map_menu)
        test.sdk.model_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        test.sdk.menu_bar.add_cascade(label="Model", menu=test.sdk.model_menu)
        test.sdk.other_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
        test.sdk.menu_bar.add_cascade(label="Other", menu=test.sdk.other_menu)

        test.sdk.map_menu.add_command(label="Build Map", command=test.map.build_map)
        test.sdk.map_menu.add_command(label="Build All Maps", command=test.map.build_all_map)
        test.sdk.map_menu.add_command(label="Info Map", command=test.map.info_map)

        test.sdk.texture_menu.add_command(label="Build Texture", command=test.texture.build_texture)
        test.sdk.texture_menu.add_command(label="Build All Textures", command=test.texture.build_all_texture)
        test.sdk.texture_menu.add_command(label="See Texture", command=test.texture.open_vtf)
        test.sdk.texture_menu.add_command(label="Texture To TGA", command=test.texture.texture_to_tga)
        test.sdk.texture_menu.add_command(label="Generate vmt", command=test.texture.generate_vmt)

        test.sdk.model_menu.add_command(label="Build Model", command=test.model.build_model)
        test.sdk.model_menu.add_command(label="Build All Models", command=test.model.build_all_model)
        test.sdk.model_menu.add_command(label="Generate QC File", command=test.model.generate_qc_file)

        test.sdk.other_menu.add_command(label="Create VPK", command=test.vpk.create_VPK)
        test.sdk.other_menu.add_command(label="Display VPK", command=test.vpk.display_VPK)
        test.sdk.other_menu.add_command(label="Display VPK Contents", command=test.vpk.display_vpk_contents)
        test.sdk.other_menu.add_command(label="Extract VPK", command=test.vpk.extract_VPK)

        test.sdk.other_menu.add_command(label="Build Caption", command=build_caption)
        test.sdk.other_menu.add_command(label="Build All Captions", command=build_all_caption)

        #if os.path.exists(test.sdk.selected_folder + "/src/creategameprojects.bat"):
        test.sdk.other_menu.add_command(label="Generate games", command=generate_games)
        #if os.path.exists(test.sdk.selected_folder + "/src/createallprojects.bat"):
        test.sdk.other_menu.add_command(label="Generate everything", command=generate_everything)
        test.sdk.other_menu.add_command(label="Download source code", command=downbload_source_code)
        test.sdk.other_menu.add_command(label="MsBuild", command=msbuild_compile)
        test.sdk.other_menu.add_command(label="Open in file explorer", command=open_file_explorer)


    test.sdk.first_init = 1

def reload_button():
    print("reload")   

    if os.path.isfile(test.sdk.bin_folder + "/hammer.exe"):
        test.sdk.btn_hammer.destroy()
    if os.path.isfile(test.sdk.bin_folder + "/hammerplusplus.exe"):
        test.sdk.btn_hammer_plus_plus.destroy()
    if os.path.isfile(test.sdk.bin_folder + "/qc_eyes.exe"):
        test.sdk.btn_qc_eyes.destroy()
    if os.path.exists(test.sdk.selected_folder + "/src/everything.sln"):
        test.sdk.btn_everything.destroy()
    if os.path.exists(test.sdk.selected_folder + "/src/games.sln"):
        test.sdk.btn_games.destroy()
    if os.path.isfile(test.sdk.bin_folder + "/hlmv.exe"):
        test.sdk.btn_hlmv.destroy()
    if os.path.isfile(test.sdk.bin_folder + "/hlfaceposer.exe"):
        test.sdk.btn_hlfaceposer.destroy()
    if os.path.isfile(os.getcwd() + "/VTfEdit/x64/VTFEdit.exe"):
        test.sdk.btn_vtf_edit.destroy()

    test.sdk.btn_Launch.destroy()
    test.sdk.btn_particle.destroy()
    test.sdk.btn_Launch_dev.destroy()

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
        SteamAppId		243730		// Source test.sdk Base 2013
        
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
        
def open_vtf():
    filenamevtf = filedialog.askopenfile(title="Select .vtf file", filetypes=[("VTF files", "*.vtf")], initialdir=test.sdk.selected_folder + "/materials")
    test.texture.open_VTF(filenamevtf.name)

# Function to handle keyboard shortcuts
def handle_shortcut(event):
    key = event.keysym
    if key == "n":
        new_project()
    elif key == "o":
        Init()

def launch_exit():
    exit()

def open_about_window():
    # Create a new window for about information
    about_window = tk.Toplevel(test.sdk.root)
    about_window.title("About")

    # Add text to the window
    about_text = tk.Label(about_window, text="Software create by ChocoScaff.\nYou can find source code.\nhttps://github.com/ChocoScaff/test.sdk-")
    about_text.pack()

def open_sln_file(sln_file_path):
    
    # Check if the .sln file exists
    if os.path.exists(sln_file_path):
        # Open the .sln file with the default application
        os.startfile(sln_file_path)
    else:
        print("Error: .sln file not found!")

def open_games():
    open_sln_file(test.sdk.selected_folder + "/src/games.sln")

def open_everything():
    open_sln_file(test.sdk.selected_folder + "/src/everything.sln")

def generate_games():
    command = f'cd /D "{test.sdk.selected_folder}\\src" && creategameprojects.bat'
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def generate_everything():
    command = f'cd /D "{test.sdk.selected_folder}\\src" && createallprojects.bat'
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def downbload_source_code():

    download_github_code("https://github.com/ValveSoftware/source-test.sdk-2013", test.sdk.selected_folder + "/src/")

    shutil.rmtree(test.sdk.selected_folder + "/src/mp/")
    move_files(test.sdk.selected_folder + "/src/sp/src/", test.sdk.selected_folder + "/src/")
    shutil.rmtree(test.sdk.selected_folder + "/src/sp/")

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

def sdk_Doc():
    webbrowser.open("https://developer.valvesoftware.com/wiki/SDK_Docs")

def list_files():
    target_extensions = [".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", ".vpk", ".tga"]
    files = []
    for test.sdk.root, dirs, files_in_dir in os.walk(test.sdk.selected_folder):
        for file_name in files_in_dir:
            for ext in target_extensions:
                if file_name.endswith(ext):
                    files.append(os.path.relpath(os.path.join(test.sdk.root, file_name), test.sdk.selected_folder))

    files.sort()  # Sort files alphabetically
    return files

def display_files():
    files = list_files()

    # Création du widget Listbox
    test.sdk.listbox = Listbox()
    
    # Création du widget Scrollbar
    test.sdk.scrollbar = tk.Scrollbar()
    
    # Configure the Listbox to use the Scrollbar
    test.sdk.listbox.config(yscrollcommand=test.sdk.scrollbar.set)
    test.sdk.scrollbar.config(command=test.sdk.listbox.yview)

    test.sdk.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    test.sdk.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Insert files into the Listbox
    for file in files:
        test.sdk.listbox.insert(tk.END, file)
    
    test.sdk.listbox.bind("<Double-Button-1>", open_file)

def open_file(event):
    selected_index = test.sdk.listbox.curselection()
    
    if selected_index:
        file = test.sdk.listbox.get(selected_index)
        file_name, file_extension = os.path.splitext(file)
        print(file)
        open_file_source_extension(file_extension,test.sdk.selected_folder + "/" + file, file[5:-4])

def open_file_source_extension(file_extension, filepath, file):
    if file_extension == ".vtf":   
        test.texture.open_VTF(filepath)
        
    elif file_extension == ".mdl":
        command = '"' + test.sdk.bin_folder + "/hlmv.exe" + '"'+ ' "' + filepath + '"' 
        subprocess.Popen(command)
    elif file_extension == ".vmf":
        #subprocess.Popen([test.sdk.bin_folder + "/hammer.exe" + ' "' + file + '"'])
        command = '"' + test.sdk.bin_folder + "/hammer.exe" + '"'+ ' "' + filepath + '"' 
        subprocess.Popen(command)
    elif file_extension == ".vcd":
        command = '"' + test.sdk.bin_folder + "/hlfaceposer.exe" + '"'+ ' "' + filepath + '"' 
        subprocess.Popen(command)
    elif file_extension == ".bsp":
        command = ('"' + test.sdk.executable_game + '"' + " -game " + '"' + test.sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720  -sw +sv_cheats 1 +map " + file)
        print(command)
        subprocess.Popen(command)
    elif file_extension == ".vpk": 
        test.vpk.display_vpk_contents(filepath)
    elif file_extension == ".tga": 
        test.texture.display_tga_file(filepath)
    else:
        try:
            os.startfile(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

def download_VTF_Edit():
    url = "https://github.com/NeilJed/VTFLib/releases/download/1.3.2/vtfedit133.zip"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Create a temporary file to save the zip content
        temp_zip_file = os.path.join(os.getcwd(), "VTF.zip")
        
        # Write the zip content to the temporary file
        with open(temp_zip_file, "wb") as f:
            f.write(response.content)
        
        os.makedirs(os.getcwd() + "/VTFEdit/")

        # Extract the contents of the zip file
        with zipfile.ZipFile(temp_zip_file, "r") as zip_ref:
            zip_ref.extractall(os.getcwd() + "/VTFEdit/")

        # Remove the temporary zip file
        os.remove(temp_zip_file)
        
        print("Download and extraction completed successfully.")
    else:
        print(f"Failed to download zip file. Status code: {response.status_code}")


def msbuild_compile():
    msbuildpath = find_msbuild()
    if msbuildpath == None:
        print("don't find msbuild")
        return
    
    sln_path = filedialog.askopenfilename(title="Select sln file", filetypes=[("sln files", "*.sln")])
    command= '"' + msbuildpath + '"' + ' ' + '"' + sln_path + '"' + " /p:Configuration=Debug"
    print(command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result)

def find_msbuild():
    # Walk through all directories and subdirectories starting from the root directory
    for dirpath, _, filenames in os.walk("C:\Program Files (x86)\MSBuild"):
        # Check if MSBuild.exe exists in the current directory
        if 'MSBuild.exe' in filenames:
            return os.path.join(dirpath, 'MSBuild.exe')

    # MSBuild.exe not found in any directory under the root directory
    return None


def open_file_explorer():
    os.startfile(test.sdk.selected_folder)

# Replace these with your GitHub repository owner and name
repo_owner = "ChocoScaff"
repo_name = "SourceSDK-"

# Replace this with the version of your local software
local_version = "0.1.3"

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

test = Test()

test.sdk = SourceSDK()

# Create the main window
test.sdk.root = tk.Tk()
test.sdk.root.title("Source SDK : assetBrowser " + local_version)

test.sdk.root.tk_setPalette(background="#4c5844", foreground="white")

test.sdk.root.configure(background="#3e4637")

test.sdk.menu_bar = tk.Menu(test.sdk.root)
test.sdk.root.config(menu=test.sdk.menu_bar,background="#3e4637")

# Create a "File" menu
file_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
test.sdk.menu_bar.add_cascade(label="File", menu=file_menu)

# Add "Open" option to the "File" menu
file_menu.add_command(label="New", command=new_project, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=Init, accelerator="Ctrl+O")
#previous_projects_menu = tk.Menu(file_menu, tearoff=0)
#file_menu.add_cascade(label="Previous Projects", menu=previous_projects_menu)
file_menu.add_command(label="Exit", command=launch_exit)

help_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
test.sdk.menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="sdk Doc", command=sdk_Doc)
help_menu.add_command(label="About", command=open_about_window)

# Create a Text widget to display terminal output
terminal = Terminal(test.sdk.root, wrap=tk.WORD, height=20, width=100)
terminal.pack()

# Redirect sys.stdout and sys.stderr to the Terminal widget
sys.stdout = terminal
sys.stderr = terminal

# Bind keyboard shortcuts to the root window
test.sdk.root.bind("<Control-n>", handle_shortcut)
test.sdk.root.bind("<Control-o>", handle_shortcut)

base_path = os.path.dirname(os.path.abspath(__file__))
iconHpp = tk.PhotoImage(file=os.path.join(base_path, "icons", "hpp.png"))
iconHammer = tk.PhotoImage(file=os.path.join(base_path, "icons", "hammer.png"))
iconSource = tk.PhotoImage(file=os.path.join(base_path, "icons", "source.png"))
iconHLMV = tk.PhotoImage(file=os.path.join(base_path, "icons", "hlmv.png"))
iconQc_eyes = tk.PhotoImage(file=os.path.join(base_path, "icons", "qc_eyes.png"))
iconHlposer = tk.PhotoImage(file=os.path.join(base_path, "icons", "hlposer.png"))
iconVisualStudio = tk.PhotoImage(file=os.path.join(base_path, "icons", "Visual_Studio.png"))
iconVTFEdit = tk.PhotoImage(file=os.path.join(base_path, "icons", "VTFEdit.png"))

# Start the GUI event loop
test.sdk.root.mainloop()