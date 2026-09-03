param([string]$Script = "backend/ui/copilot_ui.py")

Write-Host "Running Streamlit using the virtual environment..."
.\venv\Scripts\python.exe -m streamlit run $Script
