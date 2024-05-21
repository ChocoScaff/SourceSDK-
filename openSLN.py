import sourceSDK
import os
class OpenSLN:
    """
    @brief Class OpenSLN
    """

    sdk : sourceSDK

    def __init__(self, sourceSDK) -> None:
        """
        """
        self.sdk = sourceSDK

    def open_games(self):
        """
        """
        self.open_sln_file(self.sdk.selected_folder + "/src/games.sln")

    def open_everything(self):
        """
        """
        self.open_sln_file(self.sdk.selected_folder + "/src/everything.sln")
    
    def open_sln_file(self, sln_file_path):
        """
        """
        
        # Check if the .sln file exists
        if os.path.exists(sln_file_path):
            # Open the .sln file with the default application
            os.startfile(sln_file_path)
        else:
            print("Error: .sln file not found!")