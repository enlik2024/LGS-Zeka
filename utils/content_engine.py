"""
Content Engine
İçerik öneri ve öğrenme paketi oluşturma motoru.
"""

import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional
from utils.db_manager import get_db_manager
from utils.curriculum_engine import get_curriculum_engine

class ContentEngine:
    """
    Doğru içeriği doğru zamanda önerir.
    """
    
    def __init__(self):
        self.db = get_db_manager()
        self.curriculum = get_curriculum_engine()
        
    def load_content_df(self) -> pd.DataFrame:
        """İçerik veritabanını yükler."""
        return self.db.fetch_data("content")
        
    def get_recommended_content(self, lesson: str, topic: str, subtopic: str) -> List[Dict[str, Any]]:
        """
        Belirtilen konu için içerik önerir.
        """
        # 1. Etiket Doğrulama (Strict Rule)
        if not self.curriculum.validate_tags(lesson, topic, subtopic):
            # st.warning(f"Müfredat dışı etiket: {lesson} > {topic} > {subtopic}")
            return []
            
        # 2. İçerik Filtreleme
        df = self.load_content_df()
        if df.empty:
            return []
            
        # Filtrele
        candidates = df[
            (df['lesson'] == lesson) &
            (df['topic'] == topic) &
            (df['subtopic'] == subtopic) &
            (df['active'].astype(str).str.lower() == 'true')
        ]
        
        return candidates.to_dict('records')

    def build_learning_packet(self, student_id: str, lesson: str, topic: str, subtopic: str) -> Dict[str, Any]:
        """
        Öğrenci için bir öğrenme paketi (fiche) hazırlar.
        """
        contents = self.get_recommended_content(lesson, topic, subtopic)
        
        if not contents:
            return {}
            
        # Şimdilik ilk uygun içeriği dönüyoruz (MVP)
        # İleride: Öğrencinin seviyesine göre seçim yapılabilir
        selected_content = contents[0]
        
        return {
            "packet_id": f"pkt_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}",
            "student_id": student_id,
            "lesson": lesson,
            "topic": topic,
            "subtopic": subtopic,
            "content": selected_content,
            "created_at": pd.Timestamp.now().isoformat()
        }

    def suggest_content_for_wrong_question(self, question_id: str) -> Dict[str, Any]:
        """
        Yanlış yapılan bir soru için içerik önerir.
        """
        # Soru detaylarını bul
        questions_df = self.db.fetch_data("questions")
        if questions_df.empty:
            return {}
            
        question_row = questions_df[questions_df['question_id'] == question_id]
        if question_row.empty:
            return {}
            
        row = question_row.iloc[0]
        lesson = row['lesson']
        topic = row['topic']
        subtopic = row.get('subtopic') # Subtopic olmayabilir
        
        if not subtopic:
            # Subtopic yoksa topic bazlı en genel içeriği bulmaya çalış veya ilkini al
            # Şimdilik boş dönelim, subtopic zorunlu gibi davranalım
            return {}
            
        return self.build_learning_packet("current_user", lesson, topic, subtopic)

    def load_flashcards_local(self, lesson, topic, subtopic):
        """Yerel JSON dosyasından flashcard yükler."""
        import json
        import os
        
        file_path = "data/flashcards_store.json"
        
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            key = f"{lesson}|{topic}|{subtopic}"
            return data.get(key)
        except Exception as e:
            print(f"Flashcard Load Error: {e}")
            return None

    def save_flashcards_local(self, lesson, topic, subtopic, cards):
        """Yerel JSON dosyasına flashcard kaydeder."""
        import json
        import os
        
        file_path = "data/flashcards_store.json"
        
        # Dizin kontrolü
        if not os.path.exists("data"):
            os.makedirs("data")
            
        data = {}
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                data = {}
        
        key = f"{lesson}|{topic}|{subtopic}"
        data[key] = cards
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_flashcards(self, lesson, topic, subtopic, cards):
        """Hibrit Kayıt: Önce Bulut (Supabase), sonra Yerel (Yedek)."""
        # 1. Cloud
        self.db.save_flashcards_db(lesson, topic, subtopic, cards)
        # 2. Local
        self.save_flashcards_local(lesson, topic, subtopic, cards)

    def load_flashcards(self, lesson, topic, subtopic):
        """Hibrit Yükleme: Önce Bulut, yoksa Yerel."""
        # 1. Cloud
        cards = self.db.load_flashcards_db(lesson, topic, subtopic)
        if cards: return cards
        # 2. Local
        return self.load_flashcards_local(lesson, topic, subtopic)

# Singleton
@st.cache_resource
def get_content_engine() -> ContentEngine:
    return ContentEngine()
