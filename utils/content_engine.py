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
        Önce eski content tablosuna, sonra yeni icerikler tablosuna bakar.
        """
        contents = self.get_recommended_content(lesson, topic, subtopic)
        
        # Eski content tablosunda bulunamadıysa yeni icerikler tablosuna bak
        if not contents:
            contents = self._get_icerikler_content(lesson, topic, subtopic)
        
        if not contents:
            return {}
            
        # Şimdilik ilk uygun içeriği dönüyoruz (MVP)
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
    
    def _get_icerikler_content(self, lesson: str, topic: str, subtopic: str) -> List[Dict[str, Any]]:
        """
        Yeni icerikler tablosundan NotebookLM içeriklerini getirir.
        meb_kazanimlar tablosuyla join yaparak curriculum_map_subtopic eşleşmesi yapar.
        """
        try:
            if self.db.db_type != "supabase" or not self.db._client:
                return []
            
            # 1. Önce kazanım ID'sini bul (curriculum_map_subtopic = subtopic)
            kazanim_result = self.db._client.table('meb_kazanimlar').select('kazanim_id').eq('ders', lesson).eq('curriculum_map_subtopic', subtopic).limit(1).execute()
            
            if not kazanim_result.data:
                return []
            
            kazanim_id = kazanim_result.data[0]['kazanim_id']
            
            # 2. Bu kazanıma ait içerikleri getir
            icerik_result = self.db._client.table('icerikler').select('*').eq('kazanim_id', kazanim_id).eq('status', 'approved').execute()
            
            if not icerik_result.data:
                return []
            
            # 3. İçerikleri content formatına çevir
            formatted_contents = []
            for icerik in icerik_result.data:
                formatted = {
                    'content_id': icerik.get('icerik_id'),
                    'lesson': lesson,
                    'topic': topic,
                    'subtopic': subtopic,
                    'content_type': icerik.get('icerik_tipi'),
                    'summary_bullets': f"📺 {icerik.get('baslik', 'İçerik')}\n\nBu konu için NotebookLM'den hazırlanmış {icerik.get('icerik_tipi', 'içerik')} bulunuyor.",
                    'strategy_steps': f"1. Video/rehberi izle\n2. Flashcard'ları çalış\n3. Quiz ile test et",
                    'common_mistakes': "NotebookLM içerikleri ile pekiştir.",
                    'video_url': icerik.get('video_url'),
                    'source': 'notebooklm',
                    'active': True
                }
                formatted_contents.append(formatted)
            
            return formatted_contents
            
        except Exception as e:
            print(f"Icerikler fetch error: {e}")
            return []

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
