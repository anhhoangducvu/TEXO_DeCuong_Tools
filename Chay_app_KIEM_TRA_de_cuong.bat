@echo off
cd /d "%~dp0"
python -m streamlit run app_kiem_tra_de_cuong.py --server.port 8512
pause
