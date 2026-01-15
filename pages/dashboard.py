"""
Dashboard Sayfası
Gelişmiş analitik ve raporlama.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.analysis_engine import get_analysis_engine
from utils.config_manager import get_config_manager
from utils.event_logger import get_event_logger
from utils.db_manager import get_db_manager

def show():
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #4ECDC4;'>📊 Gelişim Kokpiti</h1>
        </div>
    """, unsafe_allow_html=True)
    
    analysis = get_analysis_engine()
    config = get_config_manager()
    
    # Gerçek student_id'yi al
    db = get_db_manager()
    user = db.get_current_user()
    student_id = user.get('student_id', 'pilot_ogrenci_01')
    
    # Veli Modu Toggle
    parent_mode = st.toggle("👨‍👩‍👧‍👦 Veli Modu (Sadeleştirilmiş Görünüm)")
    
    if parent_mode:
        st.info("Veli modu aktif: Sadece temel KPI'lar ve özet rapor gösteriliyor.")
        
        # Sade KPI'lar
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Genel Başarı", "%68", "+2%")
        with col2:
            st.metric("Çözülen Soru", "1,250", "+150")
            
        st.markdown("---")
        st.subheader("Haftalık Özet")
        report_html = analysis.generate_weekly_report_html(student_id)
        st.components.v1.html(report_html, height=400, scrolling=True)
        return

    # Normal Öğrenci Modu
    tabs = st.tabs(["📈 Genel Bakış", "🔥 Konu Haritası", "📅 Gelişim", "📜 Geçmiş Denemeler", "📄 Raporlar"])
    
    with tabs[0]:
        st.subheader("Genel Durum")
        
        # Gerçek Veri Hesaplama
        try:
            logger = get_event_logger()
            if logger.log_file.exists():
                events_df = pd.read_csv(logger.log_file)
                total_interactions = len(events_df)
                active_days = events_df['timestamp'].apply(lambda x: str(x)[:10]).nunique()
                
                # Son 24 saat
                now = pd.Timestamp.now()
                events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
                last_24h = len(events_df[events_df['timestamp'] > (now - pd.Timedelta(days=1))])
            else:
                total_interactions = 0
                active_days = 0
                last_24h = 0
        except Exception as e:
            st.error(f"Log okuma hatası: {e}")
            total_interactions = 0
            active_days = 0
            last_24h = 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Toplam Etkileşim", f"{total_interactions}", f"+{last_24h} (24s)")
        col2.metric("Aktif Gün", f"{active_days}", "Gün")
        col3.metric("Seri", "5 Gün", "Sabit") # Streak şimdilik static veya gamification'dan alınabilir
        
        # Zayıf Konular
        st.markdown("### ⚠️ Alarm Veren Konular")
        weakest = analysis.get_weakest_topics(student_id)
        if weakest:
            for item in weakest:
                st.error(f"{item['lesson']} > {item['topic']} (Skor: {item['score']})")
        else:
            st.info("Henüz yeterli veri yok.")

    with tabs[1]:
        st.subheader("🎯 Konu Hakimiyeti")
        
        # Mastery Manager entegrasyonu
        from utils.mastery_manager import get_mastery_manager
        mastery = get_mastery_manager()
        
        # Özet kartları
        summary = mastery.get_mastery_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📚 Toplam Konu", summary["total_topics"])
        with col2:
            st.metric("✅ Hakimiyet", summary["mastered"], help="≥%80")
        with col3:
            st.metric("📖 Öğreniyor", summary["learning"], help="%20-%80")
        with col4:
            st.metric("📊 Ortalama", f"%{summary['average_mastery']}")
        
        st.markdown("---")
        
        # Ders bazlı ilerleme
        lessons = ["Matematik", "Fen Bilimleri", "Türkçe"]
        
        for lesson in lessons:
            lesson_data = mastery.get_mastery_for_lesson(lesson)
            
            if lesson_data:
                with st.expander(f"📘 {lesson} ({len(lesson_data)} konu)", expanded=False):
                    for topic_data in lesson_data:
                        pct = topic_data["mastery_percent"]
                        subtopic = topic_data["subtopic"]
                        
                        # Renk belirleme
                        if pct >= 80:
                            color = "🟢"
                        elif pct >= 40:
                            color = "🟡"
                        else:
                            color = "🔴"
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.progress(pct / 100, text=f"{color} {subtopic}")
                        with col2:
                            st.write(f"**%{pct}**")
        
        # Zayıf konular uyarısı
        weak_topics = mastery.get_weak_topics(3)
        if weak_topics:
            st.markdown("### ⚠️ En Zayıf Konular")
            for topic in weak_topics:
                st.warning(f"📌 {topic['lesson']} > {topic['subtopic']} - %{topic['mastery_percent']}")
                if st.button(f"Bu Konuyu Öğren", key=f"learn_{topic['subtopic']}"):
                    st.session_state.learning_lesson = topic["lesson"]
                    st.session_state.learning_topic = topic["topic"]
                    st.session_state.learning_subtopic = topic["subtopic"]
                    st.switch_page("pages/ogren.py")
        else:
            # Eski heatmap fallback
            heatmap_data = analysis.get_mastery_heatmap_data(student_id)
            if not heatmap_data.empty:
                st.bar_chart(heatmap_data, x="Konu", y="Skor", color="Ders")
            else:
                st.info("Henüz konu hakimiyeti verisi yok. Öğren bölümünden konuları çalışmaya başla!")

    with tabs[2]:
        st.subheader("Net Gelişimi")
        trend_data = analysis.get_net_trend_data(student_id)
        
        if not trend_data.empty:
            st.line_chart(trend_data, x='created_at', y='score', color='lesson')
        else:
            st.info("Henüz sınav verisi yok.")

    with tabs[3]:
        st.subheader("Geçmiş Denemeler")
        history = analysis.get_exam_history(student_id) # current_user -> pilot_ogrenci_01
        # Not: Gerçek app'te session_state'den alınmalı
        
        if history:
            for exam in history:
                # Tarih formatlama
                date_str = exam.get('created_at', '')
                try:
                    dt = pd.to_datetime(date_str)
                    date_display = dt.strftime("%d.%m.%Y %H:%M")
                except:
                    date_display = date_str
                    
                score = exam.get('score', 0)
                try:
                    score = float(score) if score else 0.0
                except (ValueError, TypeError):
                    score = 0.0
                
                with st.expander(f"{date_display} - {exam.get('title', 'Deneme')} (Başarı: %{score:.1f})"):
                    st.write(f"**Mod:** {exam.get('mode', 'Bilinmiyor')}")
                    st.write(f"**Durum:** {exam.get('status', 'Tamamlandı')}")
                    # İleride buraya "Detay Gör" butonu eklenebilir
        else:
            st.info("Henüz çözülmüş deneme bulunmuyor.")

    with tabs[4]:
        st.subheader("Raporlar")
        if st.button("📄 Haftalık Raporu İndir (PDF)"):
            st.toast("PDF oluşturuluyor... (Simülasyon)")
            
        report_html = analysis.generate_weekly_report_html(student_id)
        with st.expander("Rapor Önizleme", expanded=True):
            st.components.v1.html(report_html, height=400, scrolling=True)

if __name__ == "__main__":
    show()
