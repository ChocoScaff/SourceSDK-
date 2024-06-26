import tkinter as tk
from PIL import Image, ImageTk
import sourceSDK
from tkinter import filedialog
import os
import subprocess


class Texture:
    """
    @Brief Class Texture
    """

    sdk : sourceSDK

    def __init__(self, sourceSDK) -> None:
        """
        """
        self.sdk = sourceSDK

    def display_tga_file(self,filename):
        """
        """

        image_windows = []

        image = Image.open(filename)
        image_window = tk.Toplevel()
        image_window.title(filename)
        image_window.geometry(f"{image.width}x{image.height}")

        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image_window, image=photo)
        label.photo = photo  # Prevents garbage collection
        label.pack()

        image_windows.append(image_window)

    def build_all_texture(self):
        """
        Build all textures in materialsrc
        """

        print("wait...")
        vtex = (self.sdk.bin_folder + "/vtex.exe")
        for root, dirs, files in os.walk(self.sdk.selected_folder + "/materialsrc"):
            for file in files:
                if file.endswith(".tga"):
                    tga_file_path = os.path.join(root, file)
                    command = ('"' + vtex + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -nopause "  + '"' + tga_file_path + '"' )
                    print(command)
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result)

    def build_texture(self,file=None):
        """
        """
        if file == None:
            filenameTGA = filedialog.askopenfile(title="Select .tga file", filetypes=[("TGA files", "*.tga")], initialdir=self.sdk.selected_folder + "/materialsrc")
            file = filenameTGA.name
        vtex = (self.sdk.bin_folder + "/vtex.exe")
        command = ('"' + vtex + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -nopause "  + '"' + file + '"' )
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    
    def open_vtf(self):
        """
        """

        filenamevtf = filedialog.askopenfile(title="Select .vtf file", filetypes=[("VTF files", "*.vtf")], initialdir=self.sdk.selected_folder + "/materials")
        self.open_VTF(filenamevtf.name)
    
    def open_VTF(self,file=""):
        """
        """
        
        if os.path.exists(r"C:\Program Files\Nem's Tools\VTFEdit\VTFEdit.exe"):
            command = '"' + r"C:\Program Files\Nem's Tools\VTFEdit\VTFEdit.exe" + '" ' + '"' + file + '"'
        else:
            command = '"' + os.getcwd() + "/VTFEdit/x64/VTFEdit.exe" + '" ' + '"' + file + '"'
        subprocess.Popen(command)

    def texture_to_tga(self, file=None, output=None):
        """
        Converts a .vtf file to a .tga file using vtf2tga.exe.
        
        Parameters:
            file (str): Path to the input .vtf file. If not provided, a file dialog will prompt the user to select a file.
            output (str): Directory where the output .tga file will be saved. If not provided, a directory dialog will prompt the user to select a directory.
        
        Returns:
            None
        """
        if file == None:
            filenameVTF = filedialog.askopenfile(title="Select .vtf file", filetypes=[("VTF file", "*.vtf")], initialdir=self.sdk.selected_folder + "/materials")
            file = filenameVTF.name

        if output == None:
            outputDir = filedialog.askdirectory(title="Select a Directory",initialdir=self.sdk.selected_folder + "/materialsrc")

        base_name = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(outputDir, base_name + ".tga")

        command = f'"{self.sdk.bin_folder}/vtf2tga.exe" -i "{file}" -o "{output_file}"'        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    
    def generate_vmt(self):
        """
        """

        filenameVMTs = filedialog.askopenfilenames(title="Select .vtf file", filetypes=[("texture file", "*.vtf")], initialdir=self.sdk.selected_folder + "/materials")

        diffuse_texture = None
        normal_texture = None
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

        popup = tk.Toplevel()
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
        if normal_texture != None:
            normal_texture = normal_texture[normal_texture.find("/materials/") + 11:]
            vmt = vmt.replace("texture_normal",normal_texture)
        else:
            vmt = vmt.replace('"$normalmap" "texture_normal"',"")

        print(vmt)

        fileVMT = self.sdk.selected_folder + "/materials/" + diffuse_texture[:-4] + ".vmt"
        fileVMT = str(fileVMT)
        fileVMT = fileVMT.replace("_diffuse", "")
        
        print(fileVMT)

        try:
            with open(fileVMT, 'w') as file:
                file.write(vmt)
            print(f"String saved to '{fileVMT}' successfully.")
        except Exception as e:
            print(f"Error: {e}")