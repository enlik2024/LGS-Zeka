"""
LGS-Zeka Platform - Tam Sistem Testi
Tüm modüllerin entegrasyonunu test eder.
"""

import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))


def print_header(text: str):
    """Başlık yazdır."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def test_imports():
    """Tüm modül import'larını test eder."""
    print_header("TEST 1: Modül Import'ları")
    
    modules = [
        ("utils.db_manager", ["DatabaseManager", "get_db_manager"]),
        ("utils.gemini_helper", ["GeminiHelper", "get_gemini_helper"]),
        ("utils.scoring", ["LGSScoring", "LGSConstants", "get_lgs_scoring"]),
    ]
    
    all_passed = True
    
    for module_name, classes in modules:
        try:
            module = __import__(module_name, fromlist=classes)
            for class_name in classes:
                if hasattr(module, class_name):
                    print(f"✓ {module_name}.{class_name}")
                else:
                    print(f"✗ {module_name}.{class_name} bulunamadı")
                    all_passed = False
        except Exception as e:
            print(f"✗ {module_name} import hatası: {str(e)}")
            all_passed = False
    
    return all_passed


def test_pages():
    """Sayfa modüllerini test eder."""
    print_header("TEST 2: Sayfa Modülleri")
    
    pages = ["dashboard", "ai_koc", "soru_analiz"]
    
    all_passed = True
    
    for page in pages:
        try:
            module = __import__(f"pages.{page}", fromlist=["show"])
            if hasattr(module, "show"):
                print(f"✓ pages.{page}.show() mevcut")
            else:
                print(f"✗ pages.{page}.show() bulunamadı")
                all_passed = False
        except Exception as e:
            print(f"✗ pages.{page} import hatası: {str(e)}")
            all_passed = False
    
    return all_passed


def test_file_structure():
    """Dosya yapısını test eder."""
    print_header("TEST 3: Dosya Yapısı")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "utils/__init__.py",
        "utils/db_manager.py",
        "utils/gemini_helper.py",
        "utils/scoring.py",
        "pages/__init__.py",
        "pages/dashboard.py",
        "pages/ai_koc.py",
        "pages/soru_analiz.py",
        ".streamlit/config.toml",
        ".streamlit/secrets.toml.example",
    ]
    
    all_passed = True
    
    for file_path in required_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} eksik")
            all_passed = False
    
    return all_passed


def test_documentation():
    """Dokümantasyon dosyalarını test eder."""
    print_header("TEST 4: Dokümantasyon")
    
    docs = [
        "README.md",
        "PROJECT_ROADMAP.md",
        "KURULUM_REHBERI.md",
        "GOOGLE_SHEETS_TEMPLATE.md",
        "FAZ1_TAMAMLANDI.md",
        "FAZ2_TAMAMLANDI.md",
        "FAZ3_TAMAMLANDI.md",
    ]
    
    all_passed = True
    
    for doc in docs:
        doc_path = ROOT_DIR / doc
        if doc_path.exists():
            size = doc_path.stat().st_size
            print(f"✓ {doc} ({size} bytes)")
        else:
            print(f"✗ {doc} eksik")
            all_passed = False
    
    return all_passed


def test_constants():
    """Sabit değerleri test eder."""
    print_header("TEST 5: Sabitler ve Konfigürasyon")
    
    try:
        from utils.scoring import LGSConstants
        
        constants = LGSConstants()
        
        # Katsayılar
        assert constants.TURKCE_KATSAYI == 4, "Türkçe katsayı hatalı"
        assert constants.MATEMATIK_KATSAYI == 4, "Matematik katsayı hatalı"
        assert constants.FEN_KATSAYI == 4, "Fen katsayı hatalı"
        
        print("✓ Ders katsayıları doğru")
        
        # Ortalama ve std
        assert constants.TURKCE_ORTALAMA > 0, "Türkçe ortalama hatalı"
        assert constants.TURKCE_STD > 0, "Türkçe std hatalı"
        
        print("✓ İstatistiksel parametreler tanımlı")
        
        # Puan aralıkları
        assert constants.MIN_PUAN == 0.0, "Min puan hatalı"
        assert constants.MAX_PUAN == 500.0, "Max puan hatalı"
        
        print("✓ Puan aralıkları doğru")
        
        return True
        
    except Exception as e:
        print(f"✗ Sabitler test hatası: {str(e)}")
        return False


def test_integration():
    """Entegrasyon testi."""
    print_header("TEST 6: Entegrasyon")
    
    try:
        # Scoring + DataFrame
        from utils.scoring import get_lgs_scoring
        import pandas as pd
        from datetime import datetime
        
        scoring = get_lgs_scoring()
        
        # Test DataFrame
        df = pd.DataFrame({
            'Tarih': [datetime.now()] * 3,
            'Ders': ['Matematik', 'Fen Bilimleri', 'Türkçe'],
            'Konu': ['Test', 'Test', 'Test'],
            'Dogru': [8, 7, 9],
            'Yanlis': [2, 1, 0],
            'Bos': [0, 2, 1],
            'Net': [7.33, 6.67, 9.0]
        })
        
        result = scoring.calculate_from_dataframe(df)
        
        assert result['lgs_puani'] > 0, "LGS puanı hesaplanamadı"
        assert result['toplam_net'] > 0, "Toplam net hesaplanamadı"
        
        print(f"✓ Scoring + DataFrame entegrasyonu çalışıyor")
        print(f"  LGS Puanı: {result['lgs_puani']:.2f}")
        print(f"  Toplam Net: {result['toplam_net']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Entegrasyon hatası: {str(e)}")
        return False


def test_helper_functions():
    """Yardımcı fonksiyonları test eder."""
    print_header("TEST 7: Yardımcı Fonksiyonlar")
    
    try:
        # Gemini helper fonksiyonları
        from utils.gemini_helper import format_solution_steps, get_difficulty_badge
        
        steps = ["Adım 1", "Adım 2"]
        formatted = format_solution_steps(steps)
        assert "Adım 1" in formatted, "Solution steps formatı hatalı"
        print("✓ format_solution_steps çalışıyor")
        
        badge = get_difficulty_badge(3)
        assert "Orta" in badge, "Difficulty badge hatalı"
        print("✓ get_difficulty_badge çalışıyor")
        
        # Scoring helper fonksiyonları
        from utils.scoring import format_score, get_score_color
        
        score_str = format_score(456.789)
        assert score_str == "456.79", "Score format hatalı"
        print("✓ format_score çalışıyor")
        
        color = get_score_color(450)
        assert color.startswith("#"), "Score color hatalı"
        print("✓ get_score_color çalışıyor")
        
        return True
        
    except Exception as e:
        print(f"✗ Yardımcı fonksiyon hatası: {str(e)}")
        return False


def test_streamlit_compatibility():
    """Streamlit uyumluluğunu test eder."""
    print_header("TEST 8: Streamlit Uyumluluk")
    
    try:
        import streamlit as st
        print(f"✓ Streamlit yüklü (v{st.__version__})")
        
        import pandas as pd
        print(f"✓ Pandas yüklü (v{pd.__version__})")
        
        import plotly
        print(f"✓ Plotly yüklü (v{plotly.__version__})")
        
        return True
        
    except ImportError as e:
        print(f"✗ Paket eksik: {str(e)}")
        print("  Lütfen 'pip install -r requirements.txt' çalıştırın")
        return False


def generate_project_stats():
    """Proje istatistiklerini oluşturur."""
    print_header("PROJE İSTATİSTİKLERİ")
    
    # Dosya sayıları
    py_files = list(ROOT_DIR.rglob("*.py"))
    md_files = list(ROOT_DIR.rglob("*.md"))
    
    # Satır sayıları
    total_lines = 0
    for py_file in py_files:
        if 'venv' not in str(py_file):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    total_lines += len(f.readlines())
            except:
                pass
    
    print(f"📊 Python Dosyaları: {len([f for f in py_files if 'venv' not in str(f)])}")
    print(f"📄 Dokümantasyon: {len(md_files)}")
    print(f"📝 Toplam Python Satırı: ~{total_lines}")
    
    # Modüller
    print(f"\n🔧 Modüller:")
    print(f"  - utils/db_manager.py")
    print(f"  - utils/gemini_helper.py")
    print(f"  - utils/scoring.py")
    
    print(f"\n📱 Sayfalar:")
    print(f"  - pages/dashboard.py")
    print(f"  - pages/ai_koc.py")
    print(f"  - pages/soru_analiz.py")
    
    print(f"\n🧪 Test Scriptleri:")
    print(f"  - test_gemini.py")
    print(f"  - test_scoring.py")
    print(f"  - test_complete.py")


def main():
    """Ana test fonksiyonu."""
    print("\n" + "="*70)
    print("  LGS-Zeka Platform - Tam Sistem Testi")
    print("="*70)
    
    results = []
    
    # Testleri çalıştır
    results.append(("Modül Import'ları", test_imports()))
    results.append(("Sayfa Modülleri", test_pages()))
    results.append(("Dosya Yapısı", test_file_structure()))
    results.append(("Dokümantasyon", test_documentation()))
    results.append(("Sabitler", test_constants()))
    results.append(("Entegrasyon", test_integration()))
    results.append(("Yardımcı Fonksiyonlar", test_helper_functions()))
    results.append(("Streamlit Uyumluluk", test_streamlit_compatibility()))
    
    # Özet
    print_header("TEST SONUÇLARI")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ BAŞARILI" if result else "✗ BAŞARISIZ"
        print(f"{test_name:.<40} {status}")
    
    print(f"\nToplam: {passed}/{total} test başarılı")
    
    # Proje istatistikleri
    generate_project_stats()
    
    # Final mesaj
    print_header("SONUÇ")
    
    if passed == total:
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("\n✅ Proje production-ready durumda!")
        print("\n🚀 Uygulamayı başlatmak için:")
        print("   streamlit run app.py")
    else:
        print(f"⚠️  {total - passed} test başarısız oldu.")
        print("\n📋 Lütfen hataları düzeltin ve tekrar test edin.")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
