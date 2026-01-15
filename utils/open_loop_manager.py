"""
Open Loop Manager
Açık döngü (tamamlanmamış görevler) yönetimi - Zeigarnik Etkisi
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional


class OpenLoopManager:
    """Açık döngü (tamamlanmamış görev) yöneticisi."""
    
    def __init__(self):
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Session state başlatma."""
        if 'open_loops' not in st.session_state:
            st.session_state.open_loops = []
    
    def add_loop(self, lesson: str, topic: str, subtopic: str, 
                 source: str = "analysis", reason: str = ""):
        """
        Açık döngü ekle.
        
        Args:
            lesson: Ders adı
            topic: Konu
            subtopic: Alt konu
            source: "analysis", "quiz", "self" (kullanıcı ekledi)
            reason: Neden açık döngü olduğu (örn: "3 soru yanlış")
        """
        loop_id = f"{lesson}_{topic}_{subtopic}"
        
        # Aynı döngü zaten varsa ekleme
        existing = [l for l in st.session_state.open_loops if l["id"] == loop_id]
        if existing:
            return
        
        loop = {
            "id": loop_id,
            "lesson": lesson,
            "topic": topic,
            "subtopic": subtopic,
            "source": source,
            "reason": reason,
            "created_at": datetime.now().isoformat(),
            "status": "open"  # open, in_progress, closed
        }
        
        st.session_state.open_loops.append(loop)
    
    def close_loop(self, loop_id: str):
        """Döngüyü kapat."""
        for loop in st.session_state.open_loops:
            if loop["id"] == loop_id:
                loop["status"] = "closed"
                loop["closed_at"] = datetime.now().isoformat()
                break
    
    def remove_loop(self, loop_id: str):
        """Döngüyü sil."""
        st.session_state.open_loops = [
            l for l in st.session_state.open_loops if l["id"] != loop_id
        ]
    
    def get_open_loops(self) -> List[Dict]:
        """Açık döngüleri getir."""
        return [l for l in st.session_state.open_loops if l["status"] == "open"]
    
    def get_loop_count(self) -> int:
        """Açık döngü sayısı."""
        return len(self.get_open_loops())
    
    def mark_in_progress(self, loop_id: str):
        """Döngüyü 'çalışılıyor' olarak işaretle."""
        for loop in st.session_state.open_loops:
            if loop["id"] == loop_id:
                loop["status"] = "in_progress"
                break


# Singleton
_manager_instance = None

def get_open_loop_manager() -> OpenLoopManager:
    """OpenLoopManager instance döndürür."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = OpenLoopManager()
    return _manager_instance


def render_open_loops_sidebar():
    """Sidebar'da açık döngüler paneli göster."""
    # Lazy initialization: Manager'ı burada çağır ki session state garanti olsun
    manager = get_open_loop_manager()
    
    # Session state kontrolü
    if 'open_loops' not in st.session_state:
        manager._initialize_session_state()
        
    open_loops = manager.get_open_loops()
    
    if not open_loops:
        return
    
    with st.expander(f"📋 Açık Döngüler ({len(open_loops)})", expanded=False):
        st.markdown("""
        <p style='font-size: 0.85rem; color: #6C757D;'>
            Tamamlanmayı bekleyen konular
        </p>
        """, unsafe_allow_html=True)
        
        for loop in open_loops[:5]:  # Max 5 göster
            col1, col2 = st.columns([4, 1])
            
            with col1:
                emoji = "🔴" if loop["source"] == "analysis" else "📌"
                st.markdown(f"""
                <div style='background: #FFF3CD; padding: 0.5rem; border-radius: 5px; margin: 0.3rem 0;'>
                    <span style='font-size: 0.85rem;'>{emoji} {loop['subtopic']}</span>
                    <br/>
                    <span style='font-size: 0.7rem; color: #6C757D;'>{loop['lesson']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📖", key=f"go_{loop['id']}", help="Konuyu Öğren"):
                    st.session_state.learning_lesson = loop["lesson"]
                    st.session_state.learning_topic = loop["topic"]
                    st.session_state.learning_subtopic = loop["subtopic"]
                    manager.mark_in_progress(loop["id"])
                    st.switch_page("pages/ogren.py")
        
        if len(open_loops) > 5:
            st.caption(f"...ve {len(open_loops) - 5} daha")
