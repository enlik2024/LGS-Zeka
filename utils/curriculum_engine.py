"""
Curriculum Engine
Müfredat haritası ve konu doğrulama motoru.
"""

import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional
from utils.db_manager import get_db_manager

class CurriculumEngine:
    """
    Müfredat verilerini yönetir ve etiket doğrulaması yapar.
    """
    
    def __init__(self):
        self.db = get_db_manager()
        
    def load_curriculum_map(self) -> pd.DataFrame:
        """Müfredat haritasını yükler."""
        return self.db.fetch_data("curriculum_map")
        
    def validate_tags(self, lesson: str, topic: str, subtopic: str) -> bool:
        """
        Verilen ders/konu/altkonu üçlüsünün müfredatta olup olmadığını doğrular.
        """
        df = self.load_curriculum_map()
        if df.empty:
            return False # Müfredat yoksa doğrulama başarısız
            
        # Case-insensitive check might be needed, but for now strict match
        match = df[
            (df['lesson'] == lesson) &
            (df['topic'] == topic) &
            (df['subtopic'] == subtopic) &
            (df['active'].astype(str).str.lower() == 'true')
        ]
        
        return not match.empty

    def get_topics_for_lesson(self, lesson: str) -> List[str]:
        """Derse ait konuları getirir."""
        df = self.load_curriculum_map()
        if df.empty:
            return []
        return df[df['lesson'] == lesson]['topic'].unique().tolist()

    def get_subtopics_for_topic(self, lesson: str, topic: str) -> List[str]:
        """Konuya ait alt konuları getirir."""
        df = self.load_curriculum_map()
        if df.empty:
            return []
        return df[
            (df['lesson'] == lesson) & 
            (df['topic'] == topic)
        ]['subtopic'].unique().tolist()

# Singleton
@st.cache_resource
def get_curriculum_engine() -> CurriculumEngine:
    return CurriculumEngine()
