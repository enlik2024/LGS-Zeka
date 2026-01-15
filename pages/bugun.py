"""
Bugün Sayfası
Günlük plan, zaman çizelgesi ve aktif görev takibi.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.schedule_engine import get_schedule_engine
from utils.gamification import get_gamification_manager
from utils.ui_components import render_block_timer

def show():
    """Bugün sayfasını gösterir."""
    
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #FF6B6B;'>📅 Bugünün Planı</h1>
            <p style='color: #6C757D; font-size: 1.1rem;'>
                Günlük hedeflerini takip et, zinciri kırma!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
def render_today_content():
    """Bugün sayfasının içeriğini render eder (Ana sayfada da kullanılabilir)."""
    
    # Motorları başlat
    schedule = get_schedule_engine()
    gm = get_gamification_manager()
    
    # Verileri çek
    blocks = schedule.get_today_blocks()
    active_block = schedule.find_active_block(blocks)
    next_block = schedule.find_next_block(blocks)
    progress = schedule.calculate_progress(blocks)
    
    # Üst kısım: Progress ve Özet
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.metric("Tamamlanan", f"%{progress:.0f}")
        
    with col2:
        # Progress bar
        st.progress(progress / 100)
        if progress == 100:
            st.success("🎉 Günlük hedeflerin tamamlandı!")
        else:
            st.info(f"Hedefine ulaşmana %{100 - progress:.0f} kaldı.")
            
    with col3:
        st.metric("Kalan Blok", len(blocks)) # Basitleştirilmiş
        
    st.markdown("---")
    
    # Günlük Özet (Small Victory)
    summary = schedule.compute_daily_summary()
    if summary:
        st.info(f"💡 **Günün Özeti:** {summary}")
    
    st.markdown("---")
    
    # Aktif Blok Kartı (Varsa)
    if active_block:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h3 style='color: white; margin: 0;'>🔥 ŞU AN AKTİF</h3>
                    <h1 style='color: white; margin: 0.5rem 0;'>{active_block['task']}</h1>
                    <p style='color: white; opacity: 0.9; font-size: 1.1rem;'>
                        📝 {active_block['desc']}
                    </p>
                </div>
                <div style='text-align: right;'>
                    <h2 style='color: white; margin: 0;'>{active_block['start']} - {active_block['end']}</h2>
                    <p style='color: white; opacity: 0.8;'>{active_block['duration_min']} dk</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:

            if st.button("✅ Bloğu Tamamla", type="primary", use_container_width=True, key="btn_complete_block"):
                schedule.mark_block_completed(active_block['id'])
                gm.add_xp(50, "Blok tamamlandı! Harikasın! 🌟")
                st.balloons()
                st.rerun()
        


        with col2:
            # Odak Modu ve Timer
            if "focus_mode_active" not in st.session_state:
                st.session_state.focus_mode_active = False
                
            if st.session_state.focus_mode_active:
                if st.button("⏹️ Odak Modunu Bitir", use_container_width=True, key="btn_stop_focus"):
                    st.session_state.focus_mode_active = False
                    st.rerun()
                
                # Gerçek Timer Bileşeni
                render_block_timer(active_block['end'])
                
            else:
                if st.button("⏱️ Odak Modu Başlat", use_container_width=True, key="btn_focus_mode"):
                    st.session_state.focus_mode_active = True
                    st.toast("Odak modu aktif! İyi çalışmalar.", icon="🔥")
                    st.rerun()
                
    elif next_block:
        st.info(f"⏳ Sıradaki blok **{next_block['start']}** saatinde başlayacak: **{next_block['task']}**")
    elif blocks:
        st.success("🌟 Bugün için planlanan tüm bloklar bitti! İyi dinlenmeler.")
    else:
        st.warning("⚠️ Bugün için henüz bir çalışma planı oluşturulmamış. 'Ayarlar' sayfasından program oluşturabilirsin.")

    # Gün Bilgisi
    days_map = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }
    today_eng = datetime.now().strftime("%A")
    today_tr = days_map.get(today_eng, today_eng)
    
    st.info(f"📅 Bugün: **{today_tr}**")

    # Zaman Çizelgesi (Timeline)
    st.markdown("### 📋 Günlük Akış")
    
    now = datetime.now()
    
    for block in blocks:
        # Zaman hesaplamaları
        try:
            start_dt = datetime.combine(now.date(), datetime.strptime(block['start'], "%H:%M").time())
            end_dt = datetime.combine(now.date(), datetime.strptime(block['end'], "%H:%M").time())
            
            time_status_html = ""
            
            if now > end_dt:
                # Geçmiş blok
                diff = now - end_dt
                hours = diff.seconds // 3600
                mins = (diff.seconds % 3600) // 60
                time_str = f"{hours}s {mins}dk" if hours > 0 else f"{mins}dk"
                time_status_html = f"<span style='color: #6C757D; font-size: 0.8rem;'>🏁 {time_str} önce bitti</span>"
                
            elif now < start_dt:
                # Gelecek blok
                diff = start_dt - now
                hours = diff.seconds // 3600
                mins = (diff.seconds % 3600) // 60
                time_str = f"{hours}s {mins}dk" if hours > 0 else f"{mins}dk"
                time_status_html = f"<span style='color: #0D6EFD; font-size: 0.8rem;'>⏳ {time_str} kaldı</span>"
                
            else:
                # Aktif blok
                diff = end_dt - now
                hours = diff.seconds // 3600
                mins = (diff.seconds % 3600) // 60
                time_str = f"{hours}s {mins}dk" if hours > 0 else f"{mins}dk"
                time_status_html = f"<span style='color: #198754; font-weight: bold; font-size: 0.8rem;'>🔥 Bitişe {time_str}</span>"
                
        except Exception:
            time_status_html = ""

        # Stil belirleme
        is_active = active_block and active_block['id'] == block['id']
        is_completed = block.get('status') == 'completed'
        
        if is_completed:
            bg_color = "#D4EDDA" # Yeşilimsi
            border_color = "#28A745"
            icon = "✅"
        elif is_active:
            bg_color = "#FFF3CD" # Sarımsı
            border_color = "#FFC107"
            icon = "🔥"
        else:
            bg_color = "#F8F9FA" # Gri
            border_color = "#E9ECEF"
            icon = "📅"
        
        with st.container():
            st.markdown(f"""
            <div style='
                background-color: {bg_color};
                border-left: 5px solid {border_color};
                padding: 1rem;
                border-radius: 5px;
                margin-bottom: 1rem;
            '>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='font-size: 1.1rem;'>{icon} {block['task']}</strong>
                        <br>
                        <span style='color: #6C757D;'>{block['desc']}</span>
                        <br>
                        {time_status_html}
                    </div>
                    <div style='text-align: right;'>
                        <span style='font-weight: bold; color: #495057;'>{block['start']}</span>
                        <br>
                        <span style='font-size: 0.9rem; color: #ADB5BD;'>{block['type'].upper()}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show():
    """Bugün sayfasını gösterir."""
    
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #FF6B6B;'>📅 Bugünün Planı</h1>
            <p style='color: #6C757D; font-size: 1.1rem;'>
                Günlük hedeflerini takip et, zinciri kırma!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tab Yapısı
    tab_today, tab_week = st.tabs(["📅 Bugün", "🗓️ Haftalık Program"])
    
    with tab_today:
        render_today_content()
        
    with tab_week:
        st.subheader("Haftalık Ders Programı")
        
        schedule = get_schedule_engine()
        days_map = {
            "Monday": "Pazartesi",
            "Tuesday": "Salı",
            "Wednesday": "Çarşamba",
            "Thursday": "Perşembe",
            "Friday": "Cuma",
            "Saturday": "Cumartesi",
            "Sunday": "Pazar"
        }
        
        # Haftalık görünüm için kolonlar veya expanderlar
        # Mobilde kolonlar sıkışabilir, expander daha güvenli
        for day_eng, day_tr in days_map.items():
            day_blocks = schedule.get_schedule_for_day(day_eng)
            
            with st.expander(f"📌 {day_tr}", expanded=False):
                if not day_blocks:
                    st.info("Bu gün için planlanmış blok yok.")
                else:
                    # Basit tablo görünümü
                    df = pd.DataFrame(day_blocks)
                    if not df.empty:
                        # Gerekli kolonları seç ve yeniden adlandır
                        display_df = df[['start', 'end', 'task', 'type']].copy()
                        display_df.columns = ['Başlangıç', 'Bitiş', 'Ders/Görev', 'Tip']
                        st.table(display_df)

if __name__ == "__main__":
    show()
