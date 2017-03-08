@echo off

setlocal EnableDelayedExpansion

set ScriptPath=%~dp0
set CurrentDrive=%ScriptPath:~0,2%

for /f "tokens=*" %%L in (%ScriptPath%\pythonpaths.txt) do (
	set line=%%L
	set PythonPath=!line:{driveletter}=%CurrentDrive%!
	if exist !PythonPath!\python.exe (
		!PythonPath!\python.exe %*
		exit /b
	)
)

endlocal

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
