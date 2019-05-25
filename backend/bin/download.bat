@echo off

set SOURCE_FOLDER=%~dp0
call "%SOURCE_FOLDER%\get_python_path.bat"
%PYTHON_PATH% -E "%SOURCE_FOLDER%\main\traffic_analyzer.py" download