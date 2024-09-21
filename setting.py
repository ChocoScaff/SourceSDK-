
import os
import tkinter as tk
from tkinter import colorchooser

class Setting():
    """
    """
    def __init__(self,SourceSDK):
        """
        Initialize settings class.
        """
        self.source_sdk = SourceSDK
        self.setting_file = os.path.join(os.getcwd(), "setting.ini")
        
        if os.path.exists(os.getcwd() + "/setting.ini"):
            self.load_settings()
        else:
            self.createSettingIni()
            self.load_settings()
    

    def createSettingIni(self):
        """
        Create default setting.ini file if it doesn't exist.
        """
        settings_content = """
background_color=#4c5844
foreground_color=white
secondary_background_color=#3e4637
"""
        try:
            with open(self.setting_file, 'w') as file:
                file.write(settings_content)
            print(f"Settings file created successfully at '{self.setting_file}'.")
        except Exception as e:
            print(f"Error: {e}")
    
    def load_settings(self):
        """
        Load settings from the setting.ini file and apply them to SourceSDK.
        """
        try:
            with open(self.setting_file, 'r') as file:
                settings = {}
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=')
                        settings[key.strip()] = value.strip()

            # Apply settings to SourceSDK
            self.source_sdk.background_color = settings.get('background_color', '#4c5844')
            self.source_sdk.foreground_color = settings.get('foreground_color', 'white')
            self.source_sdk.secondary_background_color = settings.get('secondary_background_color', '#3e4637')
            print("Settings loaded successfully.")
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def create_gui(self):
        # Window title and size
        self.root = tk.Toplevel(self.source_sdk.root)
        self.root.title("Settings")
        self.root.geometry("500x300")

        # Label and entry for Background Color
        tk.Label(self.root, text="Background Color:").grid(row=0, column=0, padx=10, pady=10)
        self.bg_color_entry = tk.Entry(self.root, width=30)
        self.bg_color_entry.grid(row=0, column=1)
        self.bg_color_entry.insert(0, self.source_sdk.background_color)

        # Button to pick background color
        tk.Button(self.root, text="Pick Color", command=self.pick_bg_color).grid(row=0, column=2)

        # Label and entry for Foreground Color
        tk.Label(self.root, text="Foreground Color:").grid(row=1, column=0, padx=10, pady=10)
        self.fg_color_entry = tk.Entry(self.root, width=30)
        self.fg_color_entry.grid(row=1, column=1)
        self.fg_color_entry.insert(0, self.source_sdk.foreground_color)
       

        # Label and entry for Secondary Background Color
        tk.Label(self.root, text="Secondary Background Color:").grid(row=2, column=0, padx=10, pady=10)
        self.sec_bg_color_entry = tk.Entry(self.root, width=30)
        self.sec_bg_color_entry.grid(row=2, column=1)
        self.sec_bg_color_entry.insert(0, self.source_sdk.secondary_background_color)

        # Button to pick secondary background color
        tk.Button(self.root, text="Pick Color", command=self.pick_sec_bg_color).grid(row=2, column=2)

        # Save button
        tk.Button(self.root, text="Save Settings", command=self.save_settings).grid(row=3, column=1, pady=20)

    def pick_bg_color(self):
        # Color chooser for background color
        color_code = colorchooser.askcolor(title="Choose Background Color")[1]
        if color_code:
            self.bg_color_entry.delete(0, tk.END)
            self.bg_color_entry.insert(0, color_code)

    def pick_fg_color(self):
        # Color chooser for foreground color
        color_code = colorchooser.askcolor(title="Choose Foreground Color")[1]
        if color_code:
            self.fg_color_entry.delete(0, tk.END)
            self.fg_color_entry.insert(0, color_code)

    def pick_sec_bg_color(self):
        # Color chooser for secondary background color
        color_code = colorchooser.askcolor(title="Choose Secondary Background Color")[1]
        if color_code:
            self.sec_bg_color_entry.delete(0, tk.END)
            self.sec_bg_color_entry.insert(0, color_code)

    def save_settings(self):
        # Save the settings from the input fields into the SDK
        self.source_sdk.background_color = self.bg_color_entry.get()
        self.source_sdk.foreground_color = self.fg_color_entry.get()
        self.source_sdk.secondary_background_color = self.sec_bg_color_entry.get()

        # Save settings to file
        try:
            with open(self.setting_file, 'w') as file:
                file.write(f"background_color={self.source_sdk.background_color}\n")
                file.write(f"foreground_color={self.source_sdk.foreground_color}\n")
                file.write(f"secondary_background_color={self.source_sdk.secondary_background_color}\n")
            print("Settings saved successfully.")
            print("Need restart to take effect.")
        except Exception as e:
            print(f"Error while saving settings: {e}")
