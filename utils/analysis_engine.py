"""
Analysis Engine
Öğrenci performans analizi ve ustalık (mastery) hesaplamaları.
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional
from utils.db_manager import get_db_manager

class AnalysisEngine:
    """
    Öğrenci gelişimini ve konu ustalığını analiz eden motor.
    """
    
    def __init__(self):
        self.db = get_db_manager()
        
    def compute_mastery_scores(self, student_id: str) -> Dict[str, Dict[str, float]]:
        """
        Öğrencinin ders ve konu bazlı ustalık skorlarını hesaplar (0-100).
        
        Returns:
            Dict: {
                "Matematik": {
                    "Üslü İfadeler": 75.5,
                    "Kareköklü İfadeler": 40.0
                },
                ...
            }
        """
        # 1. Verileri çek
        answers_df = self.db.fetch_data("answers")
        questions_df = self.db.fetch_data("questions")
        
        if answers_df.empty or questions_df.empty:
            return {}
            
        # 2. Merge (Cevaplar + Soru Detayları)
        # student_id filtresi
        student_answers = answers_df[answers_df['student_id'] == student_id]
        
        if student_answers.empty:
            return {}
            
        # question_id üzerinden birleştir
        # Not: CSV'de kolon isimleri küçük harf olabilir, kontrol etmek lazım.
        # db_manager robust ama kolon isimleri standart olmalı.
        
        try:
            merged = pd.merge(
                student_answers, 
                questions_df, 
                on='question_id', 
                how='inner'
            )
        except KeyError:
            # Kolon ismi uyuşmazlığı olabilir
            return {}

        # 3. Hesaplama
        mastery_map = {}
        
        # Dersleri gez
        if 'lesson' in merged.columns:
            lessons = merged['lesson'].unique()
        elif 'Ders' in merged.columns: # Eski format desteği
            lessons = merged['Ders'].unique()
        else:
            return {}
            
        for lesson in lessons:
            lesson_df = merged[merged.get('lesson', merged.get('Ders')) == lesson]
            mastery_map[lesson] = {}
            
            # Konuları gez
            topics = lesson_df.get('topic', lesson_df.get('Konu')).unique()
            
            for topic in topics:
                topic_df = lesson_df[lesson_df.get('topic', lesson_df.get('Konu')) == topic]
                
                # Basit Ağırlıklı Ortalama
                # Zorluk (1-5) * Doğru (1/0)
                # Mastery = (Toplam Kazanılan Puan / Maksimum Mümkün Puan) * 100
                
                total_points = 0
                max_points = 0
                
                for _, row in topic_df.iterrows():
                    difficulty = int(row.get('difficulty_label', row.get('Zorluk', 1)))
                    is_correct = 1 if str(row.get('is_correct')).lower() == 'true' else 0
                    
                    total_points += is_correct * difficulty
                    max_points += difficulty
                
                if max_points > 0:
                    score = (total_points / max_points) * 100
                else:
                    score = 0.0
                    
                mastery_map[lesson][topic] = round(score, 1)
                
        return mastery_map

    def build_student_skill_summary(self, student_id: str) -> Dict[str, Any]:
        """
        Öğrencinin yetenek özetini çıkarır (LLM için).
        """
        mastery = self.compute_mastery_scores(student_id)
        weakest = self.get_weakest_topics(student_id, limit=5)
        
        return {
            "student_id": student_id,
            "mastery_scores": mastery,
            "weakest_topics": weakest,
            "generated_at": pd.Timestamp.now().isoformat()
        }

    def get_weakest_topics(self, student_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        En zayıf 3 konuyu getirir.
        """
        mastery = self.compute_mastery_scores(student_id)
        flat_list = []
        
        for lesson, topics in mastery.items():
            for topic, score in topics.items():
                flat_list.append({
                    "lesson": lesson,
                    "topic": topic,
                    "score": score
                })
        
        # Skora göre artan sırala (en düşük en üstte)
        sorted_topics = sorted(flat_list, key=lambda x: x['score'])
        
        return sorted_topics[:limit]

    def get_mastery_heatmap_data(self, student_id: str) -> pd.DataFrame:
        """
        Heatmap için veri hazırlar: Konu vs. Ustalık Seviyesi.
        """
        mastery = self.compute_mastery_scores(student_id)
        data = []
        
        for lesson, topics in mastery.items():
            for topic, score in topics.items():
                data.append({
                    "Ders": lesson,
                    "Konu": topic,
                    "Skor": score,
                    "Seviye": "Zayıf" if score < 40 else "Orta" if score < 70 else "İyi"
                })
                
        return pd.DataFrame(data)

    def get_net_trend_data(self, student_id: str) -> pd.DataFrame:
        """
        Net trend analizi için veri (Tarih vs. Net).
        """
        exams_df = self.db.fetch_data("exams")
        if exams_df.empty:
            return pd.DataFrame()
            
        # Sadece bu öğrencinin sınavları
        student_exams = exams_df[exams_df['student_id'] == student_id].copy()
        
        # Tarihe göre sırala
        if 'created_at' in student_exams.columns:
            student_exams['created_at'] = pd.to_datetime(student_exams['created_at'])
            student_exams = student_exams.sort_values('created_at')
            
            # Net hesaplama (Basitçe: Doğru - Yanlış/3)
            # Bu veri exams tablosunda yoksa hesaplanmalı, şimdilik 'score' kolonunu kullanıyoruz
            # Eğer score yoksa rastgele veri üretmeyelim, boş dönelim
            if 'score' in student_exams.columns:
                # Geriye dönük uyumluluk: lesson kolonu yoksa ekle
                if 'lesson' not in student_exams.columns:
                    student_exams['lesson'] = 'Genel'
                    
                return student_exams[['created_at', 'score', 'lesson']]
        
        return pd.DataFrame()

    def get_exam_history(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Öğrencinin geçmiş sınavlarını listeler.
        """
        exams_df = self.db.fetch_data("exams")
        
        if exams_df.empty:
            return []
        
        student_exams = exams_df[exams_df['student_id'] == student_id].copy()
        
        if student_exams.empty:
            return []
            
        # Tarihe göre tersten sırala (En yeni en üstte)
        if 'created_at' in student_exams.columns:
            student_exams['created_at'] = pd.to_datetime(student_exams['created_at'])
            student_exams = student_exams.sort_values('created_at', ascending=False)
            
        return student_exams.to_dict('records')

    def generate_weekly_report_html(self, student_id: str) -> str:
        """
        Haftalık rapor için HTML üretir.
        """
        mastery = self.compute_mastery_scores(student_id)
        weakest = self.get_weakest_topics(student_id)
        
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #2c3e50;">📅 Haftalık Gelişim Raporu</h2>
            <hr>
            <h3 style="color: #e74c3c;">⚠️ Odaklanılması Gereken Konular</h3>
            <ul>
        """
        
        for item in weakest:
            html += f"<li><b>{item['lesson']} - {item['topic']}</b>: %{item['score']}</li>"
            
        html += """
            </ul>
            <hr>
            <h3 style="color: #27ae60;">🏆 Genel Durum</h3>
            <p>Konu bazlı ustalık seviyeleriniz güncellendi. Detaylar için panele göz atın.</p>
        </div>
        """
        return html

# Singleton
@st.cache_resource
def get_analysis_engine() -> AnalysisEngine:
    return AnalysisEngine()
