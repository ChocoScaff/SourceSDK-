cd /d %~dp0
pyinstaller.exe --onefile .\assetsBrowser.py --icon .\lambda.ico --add-data icons/*;icons