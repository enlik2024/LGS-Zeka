@echo off
echo ==========================================
echo BOZUK VENV ONARILIYOR (GUVENLI MOD)...
echo ==========================================

echo [1/3] Eski sanal ortam (venv) temizleniyor...
if exist venv (
    rmdir /s /q venv
)

echo [2/3] Yeni venv olusturuluyor...
:: Python 3.13 veya varsayilan python'u dene
py -3.13 -m venv venv || python -m venv venv

echo [3/3] Gerekli kutuphaneler yukleniyor (Onbelleksiz)...
:: --no-cache-dir ile onbellek permission hatalarini asiyoruz
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\pip install --no-cache-dir -r requirements.txt

echo.
echo ==========================================
echo KURULUM BASARIYLA TAMAMLANDI! 
echo ==========================================
echo.
echo Lutfen simdi tekrar "run_app.bat" dosyasini calistirin.
echo.
pause
