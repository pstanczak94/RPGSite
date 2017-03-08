@echo off

setlocal DisableDelayedExpansion

set ScriptPath=%~dp0
set CurrentDrive=%ScriptPath:~0,2%

for /f %%L in (%ScriptPath%\pythonpaths.txt) do (
	set "line=%%L"
	
	setlocal EnableDelayedExpansion
	
	set iPythonPath=!line:{driveletter}=%CurrentDrive%!
	
	if exist !iPythonPath!\python.exe (
		!iPythonPath!\python.exe %*
		exit /b
	)
	
	endlocal
)

where /q python.exe

if .%ERRORLEVEL%.==.0. (
	python.exe %*
	exit /b
)

where /q py.exe

if .%ERRORLEVEL%.==.0. (
	py.exe %*
	exit /b
)

echo Unable to find python executable...
