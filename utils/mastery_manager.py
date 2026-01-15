"""
Mastery Tracking Manager
Konu hakimiyeti izleme ve yönetimi
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


class MasteryManager:
    """Konu hakimiyeti yöneticisi."""
    
    def __init__(self):
        self._initialize_session_state()
        
    def _initialize_session_state(self):
        """Session state başlatma."""
        if 'topic_mastery' not in st.session_state:
            st.session_state.topic_mastery = {}
    
    def update_mastery(self, lesson: str, topic: str, subtopic: str, 
                       activity_type: str, success: bool = True):
        """
        Konu hakimiyetini güncelle.
        
        Args:
            lesson: Ders adı
            topic: Konu
            subtopic: Alt konu
            activity_type: "view", "flashcard", "quiz", "socratic"
            success: Başarılı mı?
        """
        key = f"{lesson}_{topic}_{subtopic}"
        
        if key not in st.session_state.topic_mastery:
            st.session_state.topic_mastery[key] = {
                "lesson": lesson,
                "topic": topic,
                "subtopic": subtopic,
                "mastery_percent": 0,
                "views": 0,
                "flashcards": 0,
                "quizzes": 0,
                "socratic_sessions": 0,
                "last_activity": None,
                "created_at": datetime.now().isoformat()
            }
        
        data = st.session_state.topic_mastery[key]
        data["last_activity"] = datetime.now().isoformat()
        
        # Aktivite tipine göre güncelle
        if activity_type == "view":
            data["views"] += 1
            increment = 5  # %5 artış
        elif activity_type == "flashcard":
            data["flashcards"] += 1
            increment = 10 if success else 5
        elif activity_type == "quiz":
            data["quizzes"] += 1
            increment = 15 if success else 5
        elif activity_type == "socratic":
            data["socratic_sessions"] += 1
            increment = 20 if success else 10
        else:
            increment = 5
        
        # Mastery yüzdesini güncelle (max %100)
        data["mastery_percent"] = min(100, data["mastery_percent"] + increment)
        
        # Supabase'e kaydet
        self._save_to_db(key, data)
    
    def _save_to_db(self, key: str, data: Dict):
        """Supabase'e kaydet."""
        try:
            from utils.db_manager import get_db_manager
            db = get_db_manager()
            
            if db.db_type == "supabase" and db._client:
                record = {
                    "mastery_id": key,
                    "student_id": "pilot_ogrenci_01",
                    "lesson": data["lesson"],
                    "topic": data["topic"],
                    "subtopic": data["subtopic"],
                    "mastery_percent": data["mastery_percent"],
                    "views": data["views"],
                    "flashcards": data["flashcards"],
                    "quizzes": data["quizzes"],
                    "socratic_sessions": data["socratic_sessions"],
                    "last_activity": data["last_activity"]
                }
                
                # Upsert (varsa güncelle, yoksa ekle)
                db._client.table("topic_mastery").upsert(
                    record, 
                    on_conflict="mastery_id"
                ).execute()
        except Exception as e:
            # Sessizce devam et (session state yeterli)
            pass
    
    def get_mastery_for_lesson(self, lesson: str) -> List[Dict]:
        """Dersin tüm konularının hakimiyetini getir."""
        results = []
        for key, data in st.session_state.topic_mastery.items():
            if data["lesson"] == lesson:
                results.append(data)
        return sorted(results, key=lambda x: x["mastery_percent"], reverse=True)
    
    def get_all_mastery(self) -> List[Dict]:
        """Tüm konuların hakimiyetini getir."""
        return list(st.session_state.topic_mastery.values())
    
    def get_mastery_summary(self) -> Dict:
        """Genel hakimiyet özeti."""
        all_data = self.get_all_mastery()
        
        if not all_data:
            return {
                "total_topics": 0,
                "mastered": 0,
                "learning": 0,
                "not_started": 0,
                "average_mastery": 0
            }
        
        mastered = len([d for d in all_data if d["mastery_percent"] >= 80])
        learning = len([d for d in all_data if 20 <= d["mastery_percent"] < 80])
        not_started = len([d for d in all_data if d["mastery_percent"] < 20])
        
        avg = sum(d["mastery_percent"] for d in all_data) / len(all_data)
        
        return {
            "total_topics": len(all_data),
            "mastered": mastered,
            "learning": learning,
            "not_started": not_started,
            "average_mastery": round(avg, 1)
        }
    
    def get_weak_topics(self, limit: int = 5) -> List[Dict]:
        """En zayıf konuları getir."""
        all_data = self.get_all_mastery()
        return sorted(all_data, key=lambda x: x["mastery_percent"])[:limit]
    
    def load_from_db(self):
        """Supabase'den mastery verilerini yükle."""
        try:
            from utils.db_manager import get_db_manager
            db = get_db_manager()
            
            df = db.fetch_data("topic_mastery")
            if not df.empty:
                df = df[df['student_id'] == 'pilot_ogrenci_01']
                
                for _, row in df.iterrows():
                    key = row.get('mastery_id', '')
                    if key:
                        st.session_state.topic_mastery[key] = {
                            "lesson": row.get('lesson', ''),
                            "topic": row.get('topic', ''),
                            "subtopic": row.get('subtopic', ''),
                            "mastery_percent": int(row.get('mastery_percent', 0)),
                            "views": int(row.get('views', 0)),
                            "flashcards": int(row.get('flashcards', 0)),
                            "quizzes": int(row.get('quizzes', 0)),
                            "socratic_sessions": int(row.get('socratic_sessions', 0)),
                            "last_activity": row.get('last_activity')
                        }
        except Exception:
            pass


# Singleton
_manager_instance = None

def get_mastery_manager() -> MasteryManager:
    """MasteryManager instance döndürür."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = MasteryManager()
        _manager_instance.load_from_db()
    
    # Session state her zaman kontrol et (Rerun'larda kaybolabilir)
    _manager_instance._initialize_session_state()
    return _manager_instance
