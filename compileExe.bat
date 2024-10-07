cd /d %~dp0
pyinstaller.exe --onefile .\src\assetsBrowser.py --icon .\lambda.ico --add-data icons/*;icons --clean