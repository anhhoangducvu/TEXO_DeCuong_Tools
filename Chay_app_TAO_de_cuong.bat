@echo off
cd /d "%~dp0"
python -m streamlit run app_tao_de_cuong.py --server.port 8511
pause
