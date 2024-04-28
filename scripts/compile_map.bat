@echo off

cd %1
cd ../
set "current_directory=%CD%"

set "bin_directory=%current_directory%\bin"
echo "%bin_directory%"
set "custom_directory=%current_directory%\custom"
echo "%custom_directory%"

mkdir "%custom_directory%\maps"

for %%f in ("%custom_directory%\mapsrc\*.vmf") do (
    echo Processing file: %%f
    "%bin_directory%\vbsp.exe" -game "%custom_directory%" "%%f"
    "%bin_directory%\vvis.exe" -game "%custom_directory%" "%custom_directory%\mapsrc\%%~nf.bsp"
    "%bin_directory%\vrad.exe" -game "%custom_directory%" "%custom_directory%\mapsrc\%%~nf.bsp"
    move "%custom_directory%\mapsrc\%%~nf.bsp" "%custom_directory%\maps\"
)

echo "Processing complete."
