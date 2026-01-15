"""
Gamification Manager
Oyunlaştırma sistemi: XP, seviye, streak, rozetler
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class GamificationManager:
    """Oyunlaştırma sistemi yöneticisi."""
    
    # Seviye tanımları
    LEVELS = [
        {"name": "Acemi 🥉", "min_xp": 0, "max_xp": 500, "color": "#CD7F32"},
        {"name": "Çırak 🥈", "min_xp": 500, "max_xp": 1500, "color": "#C0C0C0"},
        {"name": "Usta 🥇", "min_xp": 1500, "max_xp": 3000, "color": "#FFD700"},
        {"name": "Uzman 💎", "min_xp": 3000, "max_xp": 5000, "color": "#4ECDC4"},
        {"name": "Efsane 👑", "min_xp": 5000, "max_xp": float('inf'), "color": "#FF6B6B"}
    ]
    
    # XP kazanım tablosu
    XP_REWARDS = {
        "soru_analiz": 10,
        "dogru_cevap": 25,
        "gunluk_hedef": 50,
        "seri_bonus": 5,  # Her gün için
        "konu_tamamla": 100,
        "hata_analiz": 5,
        "ogretmen_sohbet": 50
    }
    
    def __init__(self):
        """Session state başlatma."""
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Tüm gamification değişkenlerini başlat."""
        if 'xp' not in st.session_state:
            # Supabase'den XP yüklemeyi dene
            xp_from_db = self._load_xp_from_db()
            st.session_state.xp = xp_from_db if xp_from_db else 0
        
        if 'level' not in st.session_state:
            st.session_state.level = self.LEVELS[0]['name']
        
        if 'streak' not in st.session_state:
            st.session_state.streak = 0
        
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = datetime.now()
        
        if 'total_questions' not in st.session_state:
            st.session_state.total_questions = 0
        
        if 'achievements' not in st.session_state:
            st.session_state.achievements = []
        
        if 'daily_xp' not in st.session_state:
            st.session_state.daily_xp = 0
    
    def _load_xp_from_db(self) -> int:
        """Supabase'den kullanıcı XP'sini yükle."""
        try:
            from utils.db_manager import get_db_manager
            db = get_db_manager()
            user = db.get_current_user()
            if user and 'xp' in user:
                return int(user.get('xp', 0))
        except Exception as e:
            print(f"XP load error: {e}")
        return 0
    
    def save_xp_to_db(self):
        """Supabase'e kullanıcı XP'sini kaydet."""
        try:
            from utils.db_manager import get_db_manager
            db = get_db_manager()
            if db.db_type == "supabase" and db._client:
                db._client.table("users").update({
                    "xp": st.session_state.xp
                }).eq("student_id", "pilot_ogrenci_01").execute()
        except Exception as e:
            print(f"XP save error: {e}")
    
    def add_xp(self, amount: int, reason: str = ""):
        """
        XP ekle ve seviye kontrolü yap.
        
        Args:
            amount: Eklenecek XP miktarı
            reason: XP kazanma nedeni
        """
        old_xp = st.session_state.xp
        old_level = self.get_current_level()
        
        # XP ekle
        st.session_state.xp += amount
        st.session_state.daily_xp += amount
        
        # Son aktivite zamanını güncelle
        st.session_state.last_activity = datetime.now()
        
        # Toast bildirimi
        emoji = "🔥" if amount >= 50 else "✨"
        st.toast(f"{emoji} +{amount} XP Kazandın! {reason}", icon="🎉")
        
        # Seviye atlama kontrolü
        new_level = self.get_current_level()
        
        if old_level != new_level:
            st.balloons()
            st.toast(f"🎊 Seviye Atladın! Artık {new_level}!", icon="👑")
            # Başarı ekle
            self.add_achievement(f"Seviye Atlama: {new_level}")
        
        # Supabase'e kaydet
        self.save_xp_to_db()
    
    def get_current_level(self) -> str:
        """Mevcut seviyeyi döndür."""
        xp = st.session_state.xp
        for level in self.LEVELS:
            if level['min_xp'] <= xp < level['max_xp']:
                return level['name']
        return self.LEVELS[-1]['name']
    
    def get_level_data(self) -> Dict:
        """Mevcut seviye verilerini döndür."""
        level_name = self.get_current_level()
        return next(l for l in self.LEVELS if l['name'] == level_name)
    
    def get_progress_to_next_level(self) -> float:
        """Bir sonraki seviyeye ilerleme yüzdesi."""
        xp = st.session_state.xp
        level_data = self.get_level_data()
        
        if level_data['max_xp'] == float('inf'):
            return 1.0
        
        progress = (xp - level_data['min_xp']) / (level_data['max_xp'] - level_data['min_xp'])
        return min(progress, 1.0)
    
    def update_streak(self):
        """Seri (streak) güncelle."""
        # Session state kontrolü
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = datetime.now()
            return
        
        now = datetime.now()
        last = st.session_state.last_activity
        
        # Aynı gün içinde
        if now.date() == last.date():
            return
        
        # Bir gün sonra (seri devam)
        elif now.date() == last.date() + timedelta(days=1):
            st.session_state.streak += 1
            bonus_xp = self.XP_REWARDS['seri_bonus'] * st.session_state.streak
            self.add_xp(bonus_xp, f"🔥 {st.session_state.streak} Günlük Seri!")
            
            # Milestone başarıları
            if st.session_state.streak == 7:
                self.add_achievement("7 Günlük Seri! 🔥")
            elif st.session_state.streak == 30:
                self.add_achievement("30 Günlük Seri! 🏆")
        
        # Seri kırıldı
        else:
            if st.session_state.streak > 0:
                st.warning(f"⚠️ {st.session_state.streak} günlük serin kırıldı. Yeniden başla!")
            st.session_state.streak = 1
        
        st.session_state.last_activity = now
    
    def add_achievement(self, achievement: str):
        """Başarı ekle."""
        if achievement not in st.session_state.achievements:
            st.session_state.achievements.append({
                "title": achievement,
                "date": datetime.now().isoformat()
            })
            st.toast(f"🏆 Yeni Başarı: {achievement}", icon="🎖️")
    
    def increment_question_count(self):
        """Soru sayısını artır."""
        st.session_state.total_questions += 1
        
        # Milestone başarıları
        if st.session_state.total_questions == 10:
            self.add_achievement("İlk 10 Soru! 🎯")
        elif st.session_state.total_questions == 50:
            self.add_achievement("50 Soru Tamamlandı! 💪")
        elif st.session_state.total_questions == 100:
            self.add_achievement("100 Soru Ustası! 🌟")
    
    def render_sidebar_stats(self):
        """Sidebar'da istatistikleri göster."""
        st.sidebar.markdown("### 🎮 Oyuncu Profili")
        
        # Seviye kartı
        level_data = self.get_level_data()
        xp = st.session_state.xp
        progress = self.get_progress_to_next_level()
        
        # Gradient kart
        st.sidebar.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {level_data['color']}40 0%, {level_data['color']}80 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid {level_data['color']};
            text-align: center;
            margin-bottom: 1rem;
        '>
            <h2 style='margin: 0; font-size: 1.8rem;'>{level_data['name']}</h2>
            <p style='margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold;'>💎 {xp} XP</p>
        </div>
        """, unsafe_allow_html=True)
        
        # İlerleme barı
        st.sidebar.progress(progress, text=f"Sonraki seviyeye: %{int(progress*100)}")
        
        # İstatistikler
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("🔥 Seri", f"{st.session_state.streak} gün")
        with col2:
            st.metric("⭐ Sorular", st.session_state.total_questions)
        
        # Günlük XP
        st.sidebar.metric("📊 Bugün", f"{st.session_state.daily_xp} XP")
        
        # Başarılar
        if st.session_state.achievements:
            with st.sidebar.expander("🏆 Başarılar"):
                for achievement in reversed(st.session_state.achievements[-5:]):
                    st.markdown(f"• {achievement['title']}")
    
    def render_level_badge(self) -> str:
        """Seviye rozeti HTML'i döndür."""
        level_data = self.get_level_data()
        
        return f"""
        <span style='
            background-color: {level_data['color']};
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        '>
            {level_data['name']}
        </span>
        """


# Singleton instance
@st.cache_resource
def _get_manager_instance() -> GamificationManager:
    """
    Cached manager instance.
    Internal use only.
    """
    return GamificationManager()

def get_gamification_manager() -> GamificationManager:
    """
    GamificationManager instance döndürür ve session state'i başlatır.
    
    Returns:
        GamificationManager: Gamification yöneticisi instance
    """
    manager = _get_manager_instance()
    # Her erişimde session state kontrolü yap
    manager._initialize_session_state()
    return manager
