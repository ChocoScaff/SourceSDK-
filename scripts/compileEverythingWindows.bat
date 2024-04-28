@echo off

rem Set the path to the Visual Studio 2013 compiler (replace with your actual path)
set "MSBUILD_PATH=C:\Program Files (x86)\MSBuild\12.0\Bin\MSBuild.exe"

rem Set the path to your solution file and the desired configuration (Debug or Release)
set "SOLUTION_PATH=%~dp0src\everything.sln"
set "CONFIGURATION=Debug"

rem Execute the MSBuild command to build the solution
"%MSBUILD_PATH%" "%SOLUTION_PATH%" /p:Configuration=%CONFIGURATION%

rem Check for build success or failure
if %errorlevel% equ 0 (
    echo Build succeeded.
) else (
    echo Build failed.
)


