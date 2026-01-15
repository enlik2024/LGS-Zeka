"""
LGS Puanlama Motoru
LGS sınavı için net hesaplama ve puan dönüşüm işlemleri
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import streamlit as st
from dataclasses import dataclass
from datetime import datetime


# LGS Sabitleri
@dataclass
class LGSConstants:
    """LGS hesaplama sabitleri."""
    
    # Ders katsayıları
    TURKCE_KATSAYI: int = 4
    MATEMATIK_KATSAYI: int = 4
    FEN_KATSAYI: int = 4
    INKILAP_KATSAYI: int = 1
    DIN_KATSAYI: int = 1
    DIL_KATSAYI: int = 1
    
    # Standart sapma ve ortalama (MEB 2024 verileri - örnek)
    # Not: Gerçek değerler her yıl MEB tarafından açıklanır
    TURKCE_ORTALAMA: float = 50.0
    TURKCE_STD: float = 15.0
    
    MATEMATIK_ORTALAMA: float = 45.0
    MATEMATIK_STD: float = 18.0
    
    FEN_ORTALAMA: float = 48.0
    FEN_STD: float = 16.0
    
    INKILAP_ORTALAMA: float = 55.0
    INKILAP_STD: float = 12.0
    
    DIN_ORTALAMA: float = 52.0
    DIN_STD: float = 13.0
    
    DIL_ORTALAMA: float = 50.0
    DIL_STD: float = 14.0
    
    # Soru sayıları
    TURKCE_SORU: int = 20
    MATEMATIK_SORU: int = 20
    FEN_SORU: int = 20
    INKILAP_SORU: int = 10
    DIN_SORU: int = 10
    DIL_SORU: int = 10
    
    # Puan aralıkları
    MIN_PUAN: float = 0.0
    MAX_PUAN: float = 500.0


class LGSScoring:
    """LGS puanlama ve hesaplama sınıfı."""
    
    def __init__(self, constants: Optional[LGSConstants] = None):
        """
        LGSScoring başlatıcı.
        
        Args:
            constants: LGS sabitleri (None ise varsayılan kullanılır)
        """
        self.constants = constants or LGSConstants()
    
    def calculate_net(
        self,
        dogru: int,
        yanlis: int,
        bos: int = 0
    ) -> float:
        """
        Net hesaplar.
        
        Args:
            dogru: Doğru sayısı
            yanlis: Yanlış sayısı
            bos: Boş sayısı (kullanılmaz, bilgi amaçlı)
            
        Returns:
            float: Hesaplanan net
        """
        try:
            net = dogru - (yanlis / 3.0)
            return round(max(0, net), 2)  # Negatif net olmaz
        except Exception as e:
            st.error(f"Net hesaplama hatası: {str(e)}")
            return 0.0
    
    def calculate_t_score(
        self,
        net: float,
        ortalama: float,
        std: float
    ) -> float:
        """
        T puanı hesaplar (Standart puan).
        
        Formül: T = 10 * ((Net - Ortalama) / Std) + 50
        
        Args:
            net: Öğrenci neti
            ortalama: Sınav ortalaması
            std: Standart sapma
            
        Returns:
            float: T puanı
        """
        try:
            if std == 0:
                return 50.0  # Standart sapma 0 ise ortalama puan
            
            t_score = 10 * ((net - ortalama) / std) + 50
            return round(t_score, 2)
        except Exception as e:
            st.error(f"T puanı hesaplama hatası: {str(e)}")
            return 50.0
    
    def calculate_lgs_score(
        self,
        nets: Dict[str, float]
    ) -> Tuple[float, Dict[str, float]]:
        """
        LGS puanını hesaplar.
        
        Args:
            nets: Ders bazlı netler
                  {"Türkçe": 15.5, "Matematik": 12.0, ...}
        
        Returns:
            Tuple[float, Dict]: (Toplam LGS puanı, Ders bazlı T puanları)
        """
        try:
            # Ders mapping
            ders_mapping = {
                "Türkçe": ("TURKCE", self.constants.TURKCE_KATSAYI),
                "Matematik": ("MATEMATIK", self.constants.MATEMATIK_KATSAYI),
                "Fen Bilimleri": ("FEN", self.constants.FEN_KATSAYI),
                "Fen": ("FEN", self.constants.FEN_KATSAYI),
                "İnkılap Tarihi": ("INKILAP", self.constants.INKILAP_KATSAYI),
                "İnkılap": ("INKILAP", self.constants.INKILAP_KATSAYI),
                "Din Kültürü": ("DIN", self.constants.DIN_KATSAYI),
                "Din": ("DIN", self.constants.DIN_KATSAYI),
                "İngilizce": ("DIL", self.constants.DIL_KATSAYI),
                "Yabancı Dil": ("DIL", self.constants.DIL_KATSAYI),
            }
            
            t_scores = {}
            weighted_sum = 0.0
            total_weight = 0
            
            for ders, net in nets.items():
                if ders not in ders_mapping:
                    continue
                
                ders_key, katsayi = ders_mapping[ders]
                
                # Ortalama ve std al
                ortalama = getattr(self.constants, f"{ders_key}_ORTALAMA")
                std = getattr(self.constants, f"{ders_key}_STD")
                
                # T puanı hesapla
                t_score = self.calculate_t_score(net, ortalama, std)
                t_scores[ders] = t_score
                
                # Ağırlıklı toplam
                weighted_sum += t_score * katsayi
                total_weight += katsayi
            
            # LGS puanı = (Ağırlıklı toplam / Toplam ağırlık) * 5
            if total_weight > 0:
                lgs_score = (weighted_sum / total_weight) * 5
                lgs_score = round(min(max(lgs_score, 0), 500), 2)
            else:
                lgs_score = 0.0
            
            return lgs_score, t_scores
            
        except Exception as e:
            st.error(f"LGS puanı hesaplama hatası: {str(e)}")
            return 0.0, {}
    
    def calculate_from_dataframe(
        self,
        df: pd.DataFrame,
        date_filter: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, any]:
        """
        DataFrame'den LGS puanı ve istatistikleri hesaplar.
        
        Args:
            df: Deneme sonuçları DataFrame
            date_filter: Tarih filtresi (başlangıç, bitiş)
            
        Returns:
            Dict: Hesaplama sonuçları
        """
        try:
            if df.empty:
                return self._empty_result()
            
            # Tarih filtresi
            if date_filter and 'Tarih' in df.columns:
                start_date, end_date = date_filter
                df = df[(df['Tarih'] >= start_date) & (df['Tarih'] <= end_date)]
            
            # Net hesaplama (eğer yoksa)
            if 'Net' not in df.columns and all(col in df.columns for col in ['Dogru', 'Yanlis']):
                df['Net'] = df.apply(
                    lambda row: self.calculate_net(row['Dogru'], row['Yanlis']),
                    axis=1
                )
            
            # Ders bazlı toplam netler
            if 'Ders' in df.columns and 'Net' in df.columns:
                ders_nets = df.groupby('Ders')['Net'].sum().to_dict()
            else:
                return self._empty_result()
            
            # LGS puanı hesapla
            lgs_score, t_scores = self.calculate_lgs_score(ders_nets)
            
            # İstatistikler
            result = {
                'lgs_puani': lgs_score,
                't_puanlari': t_scores,
                'ders_netleri': ders_nets,
                'toplam_net': sum(ders_nets.values()),
                'ortalama_net': sum(ders_nets.values()) / len(ders_nets) if ders_nets else 0,
                'toplam_deneme': len(df['Tarih'].unique()) if 'Tarih' in df.columns else len(df),
                'en_iyi_ders': max(ders_nets, key=ders_nets.get) if ders_nets else None,
                'en_zayif_ders': min(ders_nets, key=ders_nets.get) if ders_nets else None,
            }
            
            return result
            
        except Exception as e:
            st.error(f"DataFrame hesaplama hatası: {str(e)}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, any]:
        """Boş sonuç döndürür."""
        return {
            'lgs_puani': 0.0,
            't_puanlari': {},
            'ders_netleri': {},
            'toplam_net': 0.0,
            'ortalama_net': 0.0,
            'toplam_deneme': 0,
            'en_iyi_ders': None,
            'en_zayif_ders': None,
        }
    
    def get_performance_level(self, lgs_score: float) -> Tuple[str, str, str]:
        """
        LGS puanına göre performans seviyesi döndürür.
        
        Args:
            lgs_score: LGS puanı
            
        Returns:
            Tuple[str, str, str]: (Seviye, Renk, Emoji)
        """
        if lgs_score >= 450:
            return "Mükemmel", "#28A745", "🏆"
        elif lgs_score >= 400:
            return "Çok İyi", "#5CB85C", "⭐"
        elif lgs_score >= 350:
            return "İyi", "#FFC107", "👍"
        elif lgs_score >= 300:
            return "Orta", "#FF9800", "📈"
        elif lgs_score >= 250:
            return "Gelişmeli", "#FF6B6B", "💪"
        else:
            return "Çalışmalı", "#DC3545", "📚"
    
    def calculate_target_distance(
        self,
        current_score: float,
        target_score: float
    ) -> Dict[str, any]:
        """
        Hedef puana uzaklığı hesaplar.
        
        Args:
            current_score: Mevcut puan
            target_score: Hedef puan
            
        Returns:
            Dict: Uzaklık bilgileri
        """
        distance = target_score - current_score
        percentage = (current_score / target_score * 100) if target_score > 0 else 0
        
        return {
            'uzaklik': round(distance, 2),
            'yuzde': round(percentage, 2),
            'ulasildi': current_score >= target_score,
            'kalan_puan': round(max(0, distance), 2)
        }
    
    def get_topic_analysis(
        self,
        df: pd.DataFrame,
        ders: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Konu bazlı analiz yapar.
        
        Args:
            df: Deneme sonuçları
            ders: Ders filtresi (None ise tüm dersler)
            
        Returns:
            pd.DataFrame: Konu analizi
        """
        try:
            if df.empty:
                return pd.DataFrame()
            
            # Ders filtresi
            if ders:
                df = df[df['Ders'] == ders]
            
            if 'Konu' not in df.columns:
                return pd.DataFrame()
            
            # Konu bazlı toplam
            analysis = df.groupby('Konu').agg({
                'Dogru': 'sum',
                'Yanlis': 'sum',
                'Bos': 'sum',
                'Net': 'sum'
            }).reset_index()
            
            # Toplam soru sayısı
            analysis['Toplam_Soru'] = analysis['Dogru'] + analysis['Yanlis'] + analysis['Bos']
            
            # Başarı yüzdesi
            analysis['Basari_Yuzdesi'] = (
                analysis['Dogru'] / analysis['Toplam_Soru'] * 100
            ).round(2)
            
            # Sıralama (en çok yanlış yapılan konular)
            analysis = analysis.sort_values('Yanlis', ascending=False)
            
            return analysis
            
        except Exception as e:
            st.error(f"Konu analizi hatası: {str(e)}")
            return pd.DataFrame()


# Singleton instance
@st.cache_resource
def get_lgs_scoring(constants: Optional[LGSConstants] = None) -> LGSScoring:
    """
    LGSScoring singleton instance döndürür.
    
    Args:
        constants: LGS sabitleri
        
    Returns:
        LGSScoring: Scoring instance
    """
    return LGSScoring(constants=constants)


# Yardımcı fonksiyonlar
def format_score(score: float) -> str:
    """
    Puanı formatlar.
    
    Args:
        score: Puan
        
    Returns:
        str: Formatlanmış puan
    """
    return f"{score:.2f}"


def get_score_color(score: float) -> str:
    """
    Puana göre renk döndürür.
    
    Args:
        score: LGS puanı
        
    Returns:
        str: Hex renk kodu
    """
    if score >= 450:
        return "#28A745"
    elif score >= 400:
        return "#5CB85C"
    elif score >= 350:
        return "#FFC107"
    elif score >= 300:
        return "#FF9800"
    elif score >= 250:
        return "#FF6B6B"
    else:
        return "#DC3545"


def create_score_gauge(score: float, max_score: float = 500) -> str:
    """
    Puan göstergesi HTML'i oluşturur.
    
    Args:
        score: Mevcut puan
        max_score: Maksimum puan
        
    Returns:
        str: HTML gauge
    """
    percentage = (score / max_score * 100) if max_score > 0 else 0
    color = get_score_color(score)
    
    return f"""
    <div style='
        width: 100%;
        background-color: #E9ECEF;
        border-radius: 10px;
        overflow: hidden;
        height: 30px;
        position: relative;
    '>
        <div style='
            width: {percentage}%;
            background-color: {color};
            height: 100%;
            transition: width 0.3s ease;
        '></div>
        <div style='
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #262730;
            font-weight: 600;
        '>
            {score:.2f} / {max_score}
        </div>
    </div>
    """
