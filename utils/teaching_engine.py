"""
Teaching Engine
Öğretici içerik öneri motoru.
"""

import streamlit as st
from typing import Dict, Any, List
from utils.db_manager import get_db_manager

class TeachingEngine:
    """
    Yanlış sorudan öğrenmeye köprü kuran motor.
    """
    
    def __init__(self):
        self.db = get_db_manager()
        
    def suggest_content_for_wrong_question(self, question_id: str, student_id: str) -> List[Dict[str, Any]]:
        """
        Yanlış yapılan soru için içerik önerir.
        Öncelik: Publisher > AI Variant > AI Generated
        """
        # 1. Soruyu bul
        questions_df = self.db.fetch_data("questions")
        if questions_df.empty:
            return []
            
        question = questions_df[questions_df['question_id'] == question_id]
        if question.empty:
            return []
            
        lesson = question.iloc[0]['lesson']
        topic = question.iloc[0]['topic']
        subtopic = question.iloc[0]['subtopic']
        
        # 2. Tüm onaylı içerikleri çek
        # get_approved_content limitli dönüyor, o yüzden manuel filtreleyelim
        all_content = self.db.load_content()
        if all_content.empty:
            return []
            
        mask = (
            (all_content['lesson'] == lesson) &
            (all_content['topic'] == topic) &
            (all_content['subtopic'] == subtopic) &
            (all_content['status'] == 'approved') &
            (all_content['active'].astype(str).str.lower() == 'true')
        )
        candidates = all_content[mask]
        
        if candidates.empty:
            return []
            
        # 3. Öncelik Sıralaması
        # Config'den okumak en iyisi ama şimdilik hardcoded priority (MVP)
        # Priority: publisher > ai_variant_of_publisher > ai_generated
        
        selected = []
        
        # A) Publisher
        pub_content = candidates[candidates['source_type'] == 'publisher']
        if not pub_content.empty:
            selected.extend(pub_content.head(1).to_dict('records'))
            
        # B) AI Variant
        if len(selected) < 2:
            var_content = candidates[candidates['source_type'] == 'ai_variant_of_publisher']
            if not var_content.empty:
                selected.extend(var_content.head(1).to_dict('records'))
                
        # C) AI Generated (Fallback)
        if len(selected) < 2:
            ai_content = candidates[candidates['source_type'] == 'ai_generated']
            if not ai_content.empty:
                needed = 2 - len(selected)
                selected.extend(ai_content.head(needed).to_dict('records'))
                
        return selected

# Singleton
@st.cache_resource
def get_teaching_engine() -> TeachingEngine:
    return TeachingEngine()
