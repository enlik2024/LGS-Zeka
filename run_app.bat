@echo off
echo ===================================================
echo LGS Neural-Koc Baslatiliyor...
echo Port: 8502
echo ===================================================

:: Venv kontrolu
if not exist "venv\Scripts\streamlit.exe" (
    echo HATA: venv bulunamadi! Lutfen once kurulumu yapin.
    pause
    exit /b
)

:: Uygulamayi baslat
.\venv\Scripts\streamlit run app.py --server.port 8502 --server.address localhost

pause
