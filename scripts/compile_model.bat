@echo off

cd /d %1
cd ../

set "current_directory=%CD%"

set "bin_directory=%current_directory%\bin"
echo "%bin_directory%"
set "custom_directory=%current_directory%\%2"
echo "%custom_directory%"

for /R "%custom_directory%\modelsrc" %%f in (*.qc) do (
    echo Processing file: %%f
    "%bin_directory%\studiomdl.exe" -game "%custom_directory%" "%%f"
)

echo "Processing complete."
