@echo off
echo ===================================================
echo Sadece Port 8502 (Bu Proje) Durduruluyor...
echo Diger projeleriniz (8501 vb.) etkilenmeyecek.
echo ===================================================

:: Port 8502'yi kullanan PID'yi bul ve oldur
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8502" ^| find "LISTENING"') do (
    echo PID %%a sonlandiriliyor...
    taskkill /f /pid %%a
)

echo.
echo Islem tamamlandi.
pause
