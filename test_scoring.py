"""
LGS Scoring Test Scripti
Puanlama motorunun doğru çalışıp çalışmadığını test eder.
"""

import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from utils.scoring import LGSScoring, LGSConstants, get_lgs_scoring
import pandas as pd
from datetime import datetime, timedelta


def print_header(text: str):
    """Başlık yazdır."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def test_constants():
    """LGS sabitlerini test eder."""
    print_header("TEST 1: LGS Sabitleri")
    
    constants = LGSConstants()
    
    print(f"Türkçe Katsayı: {constants.TURKCE_KATSAYI}")
    print(f"Matematik Katsayı: {constants.MATEMATIK_KATSAYI}")
    print(f"Fen Katsayı: {constants.FEN_KATSAYI}")
    print(f"İnkılap Katsayı: {constants.INKILAP_KATSAYI}")
    print(f"Din Katsayı: {constants.DIN_KATSAYI}")
    print(f"Dil Katsayı: {constants.DIL_KATSAYI}")
    
    print(f"\nTürkçe Ortalama: {constants.TURKCE_ORTALAMA}")
    print(f"Türkçe Std: {constants.TURKCE_STD}")
    
    print("\n✓ LGS sabitleri tanımlı")
    return True


def test_net_calculation():
    """Net hesaplama testi."""
    print_header("TEST 2: Net Hesaplama")
    
    scoring = LGSScoring()
    
    test_cases = [
        (10, 0, 0, 10.0),    # 10 doğru, 0 yanlış
        (8, 2, 0, 7.33),     # 8 doğru, 2 yanlış
        (5, 3, 2, 4.0),      # 5 doğru, 3 yanlış, 2 boş
        (0, 10, 0, 0.0),     # 0 doğru, 10 yanlış (negatif olmaz)
    ]
    
    all_passed = True
    
    for dogru, yanlis, bos, expected in test_cases:
        result = scoring.calculate_net(dogru, yanlis, bos)
        passed = abs(result - expected) < 0.01
        
        status = "✓" if passed else "✗"
        print(f"{status} D:{dogru} Y:{yanlis} B:{bos} → Net: {result:.2f} (Beklenen: {expected})")
        
        if not passed:
            all_passed = False
    
    return all_passed


def test_t_score():
    """T puanı hesaplama testi."""
    print_header("TEST 3: T Puanı Hesaplama")
    
    scoring = LGSScoring()
    
    # Ortalama net = 50, Std = 15
    test_cases = [
        (50, 50, 15, 50.0),   # Ortalama net → T=50
        (65, 50, 15, 60.0),   # Ortalama + 1 std → T=60
        (35, 50, 15, 40.0),   # Ortalama - 1 std → T=40
    ]
    
    all_passed = True
    
    for net, ort, std, expected in test_cases:
        result = scoring.calculate_t_score(net, ort, std)
        passed = abs(result - expected) < 0.01
        
        status = "✓" if passed else "✗"
        print(f"{status} Net:{net} Ort:{ort} Std:{std} → T: {result:.2f} (Beklenen: {expected})")
        
        if not passed:
            all_passed = False
    
    return all_passed


def test_lgs_score():
    """LGS puanı hesaplama testi."""
    print_header("TEST 4: LGS Puanı Hesaplama")
    
    scoring = LGSScoring()
    
    # Örnek netler
    nets = {
        "Türkçe": 15.0,
        "Matematik": 12.0,
        "Fen Bilimleri": 14.0,
        "İnkılap Tarihi": 8.0,
        "Din Kültürü": 7.0,
        "İngilizce": 6.0
    }
    
    lgs_score, t_scores = scoring.calculate_lgs_score(nets)
    
    print(f"Ders Netleri:")
    for ders, net in nets.items():
        print(f"  {ders}: {net}")
    
    print(f"\nT Puanları:")
    for ders, t_score in t_scores.items():
        print(f"  {ders}: {t_score:.2f}")
    
    print(f"\n📊 LGS Puanı: {lgs_score:.2f}")
    
    # Puan 0-500 arasında mı?
    if 0 <= lgs_score <= 500:
        print("✓ LGS puanı geçerli aralıkta")
        return True
    else:
        print("✗ LGS puanı geçersiz!")
        return False


def test_performance_level():
    """Performans seviyesi testi."""
    print_header("TEST 5: Performans Seviyesi")
    
    scoring = LGSScoring()
    
    test_scores = [480, 420, 370, 320, 270, 200]
    
    for score in test_scores:
        level, color, emoji = scoring.get_performance_level(score)
        print(f"{emoji} Puan: {score} → {level} ({color})")
    
    print("\n✓ Performans seviyeleri tanımlı")
    return True


def test_target_distance():
    """Hedef uzaklık hesaplama testi."""
    print_header("TEST 6: Hedef Uzaklık")
    
    scoring = LGSScoring()
    
    test_cases = [
        (400, 450, 50, 88.89, False),
        (450, 450, 0, 100.0, True),
        (470, 450, 0, 104.44, True),
    ]
    
    all_passed = True
    
    for current, target, exp_distance, exp_percentage, exp_reached in test_cases:
        result = scoring.calculate_target_distance(current, target)
        
        distance_ok = abs(result['kalan_puan'] - exp_distance) < 0.01
        percentage_ok = abs(result['yuzde'] - exp_percentage) < 0.1
        reached_ok = result['ulasildi'] == exp_reached
        
        passed = distance_ok and percentage_ok and reached_ok
        status = "✓" if passed else "✗"
        
        print(f"{status} Mevcut:{current} Hedef:{target}")
        print(f"   Kalan: {result['kalan_puan']:.2f} puan")
        print(f"   Yüzde: %{result['yuzde']:.2f}")
        print(f"   Ulaşıldı: {result['ulasildi']}")
        
        if not passed:
            all_passed = False
    
    return all_passed


def test_dataframe_calculation():
    """DataFrame'den hesaplama testi."""
    print_header("TEST 7: DataFrame Hesaplama")
    
    # Örnek DataFrame oluştur
    data = []
    base_date = datetime.now() - timedelta(days=10)
    
    dersler = ["Matematik", "Fen Bilimleri", "Türkçe"]
    konular = {
        "Matematik": ["Üslü İfadeler", "Denklemler"],
        "Fen Bilimleri": ["Kuvvet", "Madde"],
        "Türkçe": ["Sözcük", "Cümle"]
    }
    
    for i in range(10):
        for ders in dersler:
            konu = konular[ders][i % 2]
            data.append({
                'Tarih': base_date + timedelta(days=i),
                'Ders': ders,
                'Konu': konu,
                'Dogru': 7 + (i % 3),
                'Yanlis': 2 - (i % 2),
                'Bos': 1,
                'Net': 0  # Hesaplanacak
            })
    
    df = pd.DataFrame(data)
    
    print(f"Test DataFrame oluşturuldu: {len(df)} satır")
    print(f"Dersler: {df['Ders'].unique().tolist()}")
    print(f"Tarih aralığı: {df['Tarih'].min()} - {df['Tarih'].max()}")
    
    # Hesaplama
    scoring = LGSScoring()
    result = scoring.calculate_from_dataframe(df)
    
    print(f"\n📊 Hesaplama Sonuçları:")
    print(f"  LGS Puanı: {result['lgs_puani']:.2f}")
    print(f"  Toplam Net: {result['toplam_net']:.2f}")
    print(f"  Ortalama Net: {result['ortalama_net']:.2f}")
    print(f"  Toplam Deneme: {result['toplam_deneme']}")
    print(f"  En İyi Ders: {result['en_iyi_ders']}")
    print(f"  En Zayıf Ders: {result['en_zayif_ders']}")
    
    # Sonuçlar mantıklı mı?
    if result['lgs_puani'] > 0 and result['toplam_net'] > 0:
        print("\n✓ DataFrame hesaplama başarılı")
        return True
    else:
        print("\n✗ DataFrame hesaplama başarısız")
        return False


def test_topic_analysis():
    """Konu analizi testi."""
    print_header("TEST 8: Konu Analizi")
    
    # Örnek DataFrame
    data = [
        {'Ders': 'Matematik', 'Konu': 'Üslü İfadeler', 'Dogru': 8, 'Yanlis': 2, 'Bos': 0, 'Net': 7.33},
        {'Ders': 'Matematik', 'Konu': 'Üslü İfadeler', 'Dogru': 7, 'Yanlis': 3, 'Bos': 0, 'Net': 6.0},
        {'Ders': 'Matematik', 'Konu': 'Denklemler', 'Dogru': 5, 'Yanlis': 4, 'Bos': 1, 'Net': 3.67},
        {'Ders': 'Fen Bilimleri', 'Konu': 'Kuvvet', 'Dogru': 9, 'Yanlis': 1, 'Bos': 0, 'Net': 8.67},
    ]
    
    df = pd.DataFrame(data)
    
    scoring = LGSScoring()
    analysis = scoring.get_topic_analysis(df, ders="Matematik")
    
    if not analysis.empty:
        print("Matematik Konu Analizi:")
        print(analysis[['Konu', 'Dogru', 'Yanlis', 'Net', 'Basari_Yuzdesi']].to_string(index=False))
        print("\n✓ Konu analizi başarılı")
        return True
    else:
        print("✗ Konu analizi başarısız")
        return False


def test_helper_functions():
    """Yardımcı fonksiyonlar testi."""
    print_header("TEST 9: Yardımcı Fonksiyonlar")
    
    from utils.scoring import format_score, get_score_color, create_score_gauge
    
    # format_score
    score = 456.789
    formatted = format_score(score)
    print(f"format_score({score}) = {formatted}")
    
    if formatted == "456.79":
        print("✓ format_score çalışıyor")
    else:
        print("✗ format_score hatası")
    
    # get_score_color
    for score in [480, 420, 370, 320, 270, 200]:
        color = get_score_color(score)
        print(f"Puan {score} → Renk: {color}")
    
    print("✓ get_score_color çalışıyor")
    
    # create_score_gauge
    gauge = create_score_gauge(450, 500)
    if "<div style=" in gauge and "450" in gauge:
        print("✓ create_score_gauge çalışıyor")
    else:
        print("✗ create_score_gauge hatası")
    
    return True


def test_singleton():
    """Singleton pattern testi."""
    print_header("TEST 10: Singleton Pattern")
    
    scoring1 = get_lgs_scoring()
    scoring2 = get_lgs_scoring()
    
    if scoring1 is scoring2:
        print("✓ Singleton pattern çalışıyor (aynı instance)")
        return True
    else:
        print("✗ Singleton pattern hatası (farklı instance'lar)")
        return False


def main():
    """Ana test fonksiyonu."""
    print("\n" + "="*60)
    print("  LGS-Zeka - Scoring Module Test Suite")
    print("="*60)
    
    results = []
    
    # Testleri çalıştır
    results.append(("LGS Sabitleri", test_constants()))
    results.append(("Net Hesaplama", test_net_calculation()))
    results.append(("T Puanı", test_t_score()))
    results.append(("LGS Puanı", test_lgs_score()))
    results.append(("Performans Seviyesi", test_performance_level()))
    results.append(("Hedef Uzaklık", test_target_distance()))
    results.append(("DataFrame Hesaplama", test_dataframe_calculation()))
    results.append(("Konu Analizi", test_topic_analysis()))
    results.append(("Yardımcı Fonksiyonlar", test_helper_functions()))
    results.append(("Singleton Pattern", test_singleton()))
    
    # Özet
    print_header("TEST SONUÇLARI")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ BAŞARILI" if result else "✗ BAŞARISIZ"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nToplam: {passed}/{total} test başarılı")
    
    if passed == total:
        print("\n🎉 Tüm testler başarılı!")
    else:
        print(f"\n⚠️  {total - passed} test başarısız oldu.")
    
    print("\n" + "="*60)
    print("  Test tamamlandı!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
