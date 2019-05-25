@echo off

set SOURCE_FOLDER=%~dp0
call "%SOURCE_FOLDER%\get_python_path.bat"

"%PYTHON_PATH%\Scripts\pip3.7.exe" install -r "%SOURCE_FOLDER%\requirements.txt" > NUL
"%PYTHON_PATH%\python.exe" -E "%SOURCE_FOLDER%\main\traffic_analyzer.py" download