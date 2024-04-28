cd "%1src\"

call "%CD_CURRENT%creategameprojects.bat"

set "file=games.sln"
set "find=#"
set "replace=VisualStudioVersion = 17.5.33530.505`r`nMinimumVisualStudioVersion = 10.0.40219.1"

powershell -Command "(Get-Content '%file%') -replace '%find%', '%replace%' | Set-Content '%file%'"

pause