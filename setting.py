
import os

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