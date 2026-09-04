@echo off
set SCRIPT=backend\streamlit_app.py
if not "%~1"=="" set SCRIPT=%~1

echo Running Streamlit using the virtual environment...
set PYTHONPATH=%cd%\backend
.\venv\Scripts\python.exe -m streamlit run %SCRIPT%
