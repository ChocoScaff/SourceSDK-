import tkinter as tk
import os
import subprocess
from tkinter import filedialog
import sys
import shutil
import git
import urllib.request
import json
import webbrowser
from tkinter import messagebox
import re

from sourceSDK import SourceSDK
from texture import Texture
from model import Model
from map import Map
from _vpk import VPK
from terminal import Terminal
from file import File
from button import Button
from caption import Caption

class AssetsBrowser():
    """
    @brief Class
    """

    sdk : SourceSDK
    texure : Texture
    model : Model
    map : Map
    vpk : VPK
    terminal : Terminal
    file : File
    button : Button
    caption : Caption

    def parse_gameinfo_txt(self):
        """
        parse game info txt
        @param file_path The path to the gameinfo.txt
        """

        gameinfo_path = os.path.join(self.sdk.selected_folder, "gameinfo.txt")
        print(gameinfo_path)

        inside_search_paths = False
        game_path_pattern = re.compile(r'^\s*game\s+([^\s]+)', re.MULTILINE)

        if os.path.isfile(gameinfo_path):
            with open(gameinfo_path, 'r') as file:
                for line in file:
                    
                    if re.search(r'^\s*SearchPaths', line):
                        inside_search_paths = True
                        continue
                    
                    # Check if the line ends the SearchPaths section
                    if inside_search_paths and re.search(r'^\s*}', line):
                        inside_search_paths = False
                        continue

                    # If inside the SearchPaths block, find game paths
                    if inside_search_paths:
                        line = line.lower()
                        if '|all_source_engine_paths|' in line:
                            line = line.replace('|all_source_engine_paths|', '')
                        match = game_path_pattern.match(line)
                        if match:
                            self.sdk.game_path.append(match.group(1).strip())

        print(self.sdk.game_path)

    def bin_folder(self,folder_path):
        """
        fin bin folder
        @param folder_path to the game
        @return binFolder
        """

        binFolder = self.sdk.parent_folder + "/bin"
        if os.path.exists(binFolder):
            pass
        else:
            #with open(folder_path + "bin.txt", 'r') as file:   
            folder = filedialog.askdirectory(title="Open bin Engine path",initialdir=self.sdk.parent_folder)
            binFolder = folder
        return binFolder

    def find_executable_game(self,folder_path):
        """
        fin exe
        @param folder_path to the game
        @return executable
        """

        executables = []
        for root, dirs, files in os.walk(self.sdk.parent_folder):
            for file in files:
                if file.endswith('.exe'):
                    executables.append(os.path.join(root, file))
        #print(executables)
        return executables[0]

    def find_game_name(self,folder_path):
        """
        fin game name
        @param folder_path to the game
        @return game name
        """
        game_name = os.path.basename(folder_path)
        return game_name

    def find_gameinfo_folder(self):
        """
        open folder whre gameinfo txt
        """

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

    def Init(self, folder=False):
        """
        Init software with parameter of the game
        @param folder=False
        """

        print("Wait...")

        if folder == False:
            if self.sdk.first_init == 1:
                self.button.destroy_button()
            self.sdk.selected_folder = self.find_gameinfo_folder()
            if self.sdk.selected_folder == -1:
                return
        else:
            if self.sdk.first_init == 1:
                self.button.destroy_button()
            self.sdk.selected_folder=folder

        print("selected directory : " + self.sdk.selected_folder)

        self.sdk.game_name = self.find_game_name(self.sdk.selected_folder)
        print("game name : " + self.sdk.game_name)

        self.sdk.parent_folder = os.path.dirname(self.sdk.selected_folder)

        self.sdk.bin_folder = self.bin_folder(self.sdk.selected_folder)
        print("bin directory : " + self.sdk.bin_folder)

        self.sdk.executable_game = self.find_executable_game(self.sdk.bin_folder)
        print("executable game : " + self.sdk.executable_game)

        self.parse_gameinfo_txt()

        try:
            self.sdk.root.iconbitmap(self.sdk.selected_folder + '/resource/game.ico')
        except tk.TclError:
            print("Error: Failed to set icon.")
        
        print("Project open")

        lbl_result = tk.Label(self.sdk.root, text="Tools", wraplength=400, background="#3e4637",fg='white')
        lbl_result.pack()

        self.texture = Texture(self.sdk)
        self.model = Model(self.sdk)
        self.map = Map(self.sdk)
        self.vpk = VPK(self.sdk)
        self.file = File(self.sdk)
        self.button = Button(self.sdk)
        self.caption = Caption(self.sdk)

        self.label_init()

    def label_init(self):
        """
        Init Labet
        """

        self.button.display()

        if self.sdk.first_init == 0:
            self.sdk.texture_menu = tk.Menu(self.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
            self.sdk.menu_bar.add_cascade(label="Texture", menu=self.sdk.texture_menu)
            self.sdk.map_menu = tk.Menu(self.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
            self.sdk.menu_bar.add_cascade(label="Map", menu=self.sdk.map_menu)
            self.sdk.model_menu = tk.Menu(self.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
            self.sdk.menu_bar.add_cascade(label="Model", menu=self.sdk.model_menu)
            self.sdk.other_menu = tk.Menu(self.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
            self.sdk.menu_bar.add_cascade(label="Other", menu=self.sdk.other_menu)

            self.sdk.map_menu.add_command(label="Build Map", command=self.map.build_map)
            self.sdk.map_menu.add_command(label="Build All Maps", command=self.map.build_all_map)
            self.sdk.map_menu.add_command(label="Info Map", command=self.map.info_map)

            self.sdk.texture_menu.add_command(label="Build Texture", command=self.texture.build_texture)
            self.sdk.texture_menu.add_command(label="Build All Textures", command=self.texture.build_all_texture)
            self.sdk.texture_menu.add_command(label="See Texture", command=self.texture.open_vtf)
            self.sdk.texture_menu.add_command(label="Texture To TGA", command=self.texture.texture_to_tga)
            self.sdk.texture_menu.add_command(label="Generate vmt", command=self.texture.generate_vmt)

            self.sdk.model_menu.add_command(label="Build Model", command=self.model.build_model)
            self.sdk.model_menu.add_command(label="Build All Models", command=self.model.build_all_model)
            self.sdk.model_menu.add_command(label="Generate QC File", command=self.model.generate_qc_file)

            self.sdk.other_menu.add_command(label="Create VPK", command=self.vpk.create_VPK)
            self.sdk.other_menu.add_command(label="Display VPK", command=self.vpk.display_VPK)
            self.sdk.other_menu.add_command(label="Display VPK Contents", command=self.vpk.display_vpk_contents)
            self.sdk.other_menu.add_command(label="Extract VPK", command=self.vpk.extract_VPK)

            self.sdk.other_menu.add_command(label="Build Caption", command=self.caption.build_caption)
            self.sdk.other_menu.add_command(label="Build All Captions", command=self.caption.build_all_caption)

            #if os.path.exists(self.sdk.selected_folder + "/src/creategameprojects.bat"):
            self.sdk.other_menu.add_command(label="Generate games", command=self.generate_games)
            #if os.path.exists(self.sdk.selected_folder + "/src/createallprojects.bat"):
            self.sdk.other_menu.add_command(label="Generate everything", command=self.generate_everything)
            self.sdk.other_menu.add_command(label="Download source code", command=self.downbload_source_code)
            self.sdk.other_menu.add_command(label="MsBuild", command=self.msbuild_compile)
            self.sdk.other_menu.add_command(label="Open in file explorer", command=self.open_file_explorer)

        self.sdk.first_init = 1


    def new_project(self):
        """
        Init New project
        """
        
        directory = filedialog.askdirectory(title="Select a Directory")
        game_name = self.find_game_name(directory)

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
                
                self.Init(directory)

            else:
                print("The directory must be empty")     
            

    # Function to handle keyboard shortcuts
    def handle_shortcut(self, event):
        """
        @param event get event keyboard
        """
        key = event.keysym
        if key == "n":
            self.new_project()
        elif key == "o":
            self.Init()

    def launch_exit(self):
        """
        exit program
        """
        exit()

    def open_about_window(self):
        """
        """
        about_window = tk.Toplevel(self.sdk.root)
        about_window.title("About")

        # Add text to the window
        about_text = tk.Label(about_window, text="Software created by ChocoScaff.\nYou can find the source code here:")
        about_text.pack()

        # Add hyperlink
        def open_link(event):
            webbrowser.open_new("https://github.com/ChocoScaff/SourceSDK-")

        hyperlink = tk.Label(about_window, text="https://github.com/ChocoScaff/SourceSDK-", fg="blue", cursor="hand2")
        hyperlink.pack()
        hyperlink.bind("<Button-1>", open_link)

    def generate_games(self):
        """
        execute creategameprojects.bat'
        """
        command = f'cd /D "{self.sdk.selected_folder}\\src" && creategameprojects.bat'
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def generate_everything(self):
        """
        execute createallprojects.bat'
        """
        command = f'cd /D "{self.sdk.selected_folder}\\src" && createallprojects.bat'
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def downbload_source_code(self):
        """
        Download source code source sdk 2013
        """

        self.download_github_code("https://github.com/ValveSoftware/source-test.sdk-2013", self.sdk.selected_folder + "/src/")

        shutil.rmtree(self.sdk.selected_folder + "/src/mp/")
        self.move_files(self.sdk.selected_folder + "/src/sp/src/", self.sdk.selected_folder + "/src/")
        shutil.rmtree(self.sdk.selected_folder + "/src/sp/")

        self.generate_games()
        self.generate_everything()

        self.Init()

    def download_github_code(self, repo_url, destination_folder):
        """
        """
        git.Repo.clone_from(repo_url, destination_folder)

    def move_files(self, source_folder, destination_folder):
        """
        """
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


    def get_latest_release_version(self, repo_owner, repo_name):
        """
        return last version
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                latest_version = data['tag_name']
                return latest_version
        except Exception as e:
            return f"Error: {e}"

    def check_software_version(self, local_version, github_version):
        """
        check local version
        """
        if local_version == github_version:
            print("You have the latest version installed.")
        else:
            print(f"There is a newer version ({github_version}) available on GitHub.")

    def sdk_Doc(self):
        """
        Open SDK Docs
        """
        webbrowser.open("https://developer.valvesoftware.com/wiki/SDK_Docs")

    def msbuild_compile(self):
        """
        compile SLN with msbuild
        """
        msbuildpath = self.find_msbuild()
        if msbuildpath == None:
            print("don't find msbuild")
            return
        
        sln_path = filedialog.askopenfilename(title="Select sln file", filetypes=[("sln files", "*.sln")])
        command= '"' + msbuildpath + '"' + ' ' + '"' + sln_path + '"' + " /p:Configuration=Debug"
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def find_msbuild(self):
        """
        find msbuild
        """
        # Walk through all directories and subdirectories starting from the root directory
        for dirpath, _, filenames in os.walk("C:\Program Files (x86)\MSBuild"):
            # Check if MSBuild.exe exists in the current directory
            if 'MSBuild.exe' in filenames:
                return os.path.join(dirpath, 'MSBuild.exe')

        # MSBuild.exe not found in any directory under the root directory
        return None


    def open_file_explorer(self):
        """
        open folder in file explorer
        TODO open exe if same name of the folder
        """
        os.startfile(self.sdk.selected_folder)

test = AssetsBrowser()

test.sdk = SourceSDK()

# Replace these with your GitHub repository owner and name
repo_owner = "ChocoScaff"
repo_name = "SourceSDK-"

# Replace this with the version of your local software
local_version = "0.5.1"

github_version = test.get_latest_release_version(repo_owner, repo_name)

if github_version:
    test.check_software_version(local_version, github_version)
else:
    print("Failed to fetch the latest version from GitHub.")
    download = messagebox.askyesno("New Version Available", f"There is a newer version ({github_version}) available on GitHub. Do you want to download it?")
    if download:
        webbrowser.open(f"https://github.com/{repo_owner}/{repo_name}/releases/latest")
    else:
        messagebox.showinfo("Version Check", "You chose not to download the new version.")

# Create the main window
test.sdk.root = tk.Tk()
test.sdk.root.title("Source SDK : assetsBrowser " + local_version)

test.sdk.root.tk_setPalette(background="#4c5844", foreground="white")

test.sdk.root.configure(background="#3e4637")

test.sdk.menu_bar = tk.Menu(test.sdk.root)
test.sdk.root.config(menu=test.sdk.menu_bar,background="#3e4637")

# Create a "File" menu
file_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
test.sdk.menu_bar.add_cascade(label="File", menu=file_menu)

# Add "Open" option to the "File" menu
file_menu.add_command(label="New", command=test.new_project, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=test.Init, accelerator="Ctrl+O")
#previous_projects_menu = tk.Menu(file_menu, tearoff=0)
#file_menu.add_cascade(label="Previous Projects", menu=previous_projects_menu)
file_menu.add_command(label="Exit", command=test.launch_exit)

help_menu = tk.Menu(test.sdk.menu_bar, tearoff=0,background="#4c5844",fg="white")
test.sdk.menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="sdk Doc", command=test.sdk_Doc)
help_menu.add_command(label="About", command=test.open_about_window)

# Create a Text widget to display terminal output
test.terminal = Terminal(test.sdk.root, wrap=tk.WORD, height=30, width=120)
test.terminal.pack()

# Redirect sys.stdout and sys.stderr to the Terminal widget
sys.stdout = test.terminal
sys.stderr = test.terminal

# Bind keyboard shortcuts to the root window
test.sdk.root.bind("<Control-n>", test.handle_shortcut)
test.sdk.root.bind("<Control-o>", test.handle_shortcut)

# Start the GUI event loop
test.sdk.root.mainloop()