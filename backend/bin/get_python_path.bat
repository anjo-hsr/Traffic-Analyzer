@echo off

if exist "C:\Program Files (x86)\Python37-32\python.exe" goto echo32
if exist "C:\Program Files\Python37-32\python.exe" goto echo64

echo "No python 3.7 installation found in Program Files folders."
exit


:echo32
set PYTHON_PATH="C:\Program Files (x86)\Python37-32\python.exe"
goto return


:echo64
set PYTHON_PATH="C:\Program Files\Python37-32\python.exe"
goto return


:return
exit /b