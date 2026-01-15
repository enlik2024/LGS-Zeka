"""
Google Sheets Bağlantı Testi
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

print("=" * 60)
print("Google Sheets Bağlantı Testi")
print("=" * 60)

try:
    # Secrets'tan bilgileri al
    print("\n1. Secrets dosyası okunuyor...")
    
    if 'gcp_service_account' not in st.secrets:
        print("❌ HATA: gcp_service_account secrets'ta bulunamadı!")
        exit(1)
    
    if 'google_sheets' not in st.secrets or 'spreadsheet_key' not in st.secrets['google_sheets']:
        print("❌ HATA: spreadsheet_key secrets'ta bulunamadı!")
        print("   Beklenen: st.secrets['google_sheets']['spreadsheet_key']")
        exit(1)
    
    print("✓ Secrets dosyası okundu")
    
    # Credentials oluştur
    print("\n2. Credentials oluşturuluyor...")
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds_dict = dict(st.secrets["gcp_service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    print("✓ Credentials oluşturuldu")
    
    # Client oluştur
    print("\n3. Google Sheets client oluşturuluyor...")
    client = gspread.authorize(credentials)
    print("✓ Client oluşturuldu")
    
    # Spreadsheet aç
    print("\n4. Spreadsheet açılıyor...")
    spreadsheet_key = st.secrets["google_sheets"]["spreadsheet_key"]
    print(f"   Spreadsheet Key: {spreadsheet_key}")
    
    spreadsheet = client.open_by_key(spreadsheet_key)
    print(f"✓ Spreadsheet açıldı: {spreadsheet.title}")
    
    # Sheet'leri listele
    print("\n5. Sheet'ler listeleniyor...")
    worksheets = spreadsheet.worksheets()
    print(f"✓ Toplam {len(worksheets)} sheet bulundu:")
    for ws in worksheets:
        print(f"   - {ws.title}")
    
    # deneme_sonuclari sheet'ini aç
    print("\n6. 'deneme_sonuclari' sheet'i açılıyor...")
    worksheet = spreadsheet.worksheet("deneme_sonuclari")
    print(f"✓ Sheet açıldı: {worksheet.title}")
    
    # İlk satırı oku (başlıklar)
    print("\n7. Sütun başlıkları okunuyor...")
    headers = worksheet.row_values(1)
    print(f"✓ Başlıklar: {headers}")
    
    # Veri sayısı
    print("\n8. Veri sayısı kontrol ediliyor...")
    all_values = worksheet.get_all_values()
    print(f"✓ Toplam {len(all_values)} satır (başlık dahil)")
    
    print("\n" + "=" * 60)
    print("🎉 TÜM TESTLER BAŞARILI!")
    print("=" * 60)
    print("\nGoogle Sheets bağlantısı çalışıyor.")
    print("Artık 'streamlit run app.py' ile uygulamayı başlatabilirsiniz.")
    
except gspread.exceptions.SpreadsheetNotFound:
    print("\n" + "=" * 60)
    print("❌ HATA: Spreadsheet Bulunamadı")
    print("=" * 60)
    print("\nOlası Nedenler:")
    print("1. Spreadsheet key yanlış")
    print("2. Service Account ile paylaşım yapılmamış")
    print("\nÇözüm:")
    print("1. Google Sheets URL'sinden key'i kontrol edin")
    print("2. Service Account email'ini Google Sheets'te paylaşın:")
    print(f"   {creds_dict.get('client_email', 'N/A')}")
    
except gspread.exceptions.WorksheetNotFound:
    print("\n" + "=" * 60)
    print("❌ HATA: 'deneme_sonuclari' Sheet'i Bulunamadı")
    print("=" * 60)
    print("\nÇözüm:")
    print("Google Sheets'te 'deneme_sonuclari' adında bir sheet oluşturun")
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ HATA")
    print("=" * 60)
    print(f"\nHata Mesajı: {str(e)}")
    print(f"Hata Tipi: {type(e).__name__}")
    
    import traceback
    print("\nDetaylı Hata:")
    traceback.print_exc()
