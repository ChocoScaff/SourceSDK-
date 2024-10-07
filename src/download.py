import requests
import zipfile
import os

class Download:
    """
    @brief Class Download
    TODO add github download
    """

    def download_VTF_Edit():
        """
        """

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
    
    def download_crowbar_decompile():
        """
        """

        url = "https://github.com/mrglaster/Source-models-decompiler-cmd/releases/download/Update/CrowbarDecompiler.1.1.zip"
        response = requests.get(url)

        if response.status_code == 200:
            # Create a temporary file to save the zip content
            temp_zip_file = os.path.join(os.getcwd(), "CrowbarDecompiler.1.1.zip")
            
            # Write the zip content to the temporary file
            with open(temp_zip_file, "wb") as f:
                f.write(response.content)
            
            os.makedirs(os.getcwd() + "/CrowbarDecompiler.1.1/")

            # Extract the contents of the zip file
            with zipfile.ZipFile(temp_zip_file, "r") as zip_ref:
                zip_ref.extractall(os.getcwd() + "/CrowbarDecompiler.1.1/")

            # Remove the temporary zip file
            os.remove(temp_zip_file)
            
            print("Download and extraction completed successfully.")
        else:
            print(f"Failed to download zip file. Status code: {response.status_code}")

    def download_VPKEdit():
        """
        """
        url = "https://github.com/craftablescience/VPKEdit/releases/download/v4.3.0/VPKEdit-Windows-Standalone-GUI-msvc-Release.zip"
        response = requests.get(url)

        if response.status_code == 200:
            # Create a temporary file to save the zip content
            temp_zip_file = os.path.join(os.getcwd(), "VPKEdit-Windows-Standalone-GUI-msvc-Release.zip")
            
            # Write the zip content to the temporary file
            with open(temp_zip_file, "wb") as f:
                f.write(response.content)
            
            os.makedirs(os.getcwd() + "/VPKEdit-Windows-Standalone-GUI-msvc-Release/")

            # Extract the contents of the zip file
            with zipfile.ZipFile(temp_zip_file, "r") as zip_ref:
                zip_ref.extractall(os.getcwd() + "/VPKEdit-Windows-Standalone-GUI-msvc-Release/")

            # Remove the temporary zip file
            os.remove(temp_zip_file)
            
            print("Download and extraction completed successfully.")
        else:
            print(f"Failed to download zip file. Status code: {response.status_code}")
     