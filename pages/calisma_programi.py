import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.scheduler_engine import get_scheduler_engine
from utils.calendar_exporter import CalendarExporter

def show():
    st.set_page_config(page_title="Çalışma Programı", page_icon="📅", layout="wide")
    
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #2E86AB;'>📅 Akıllı Çalışma Programı</h1>
            <p style='color: #6C757D; font-size: 1.1rem;'>
                LGS hedeflerine uygun, kişiselleştirilmiş programın burada!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("💡 **Nasıl Çalışır?** 'Akıllı Program Oluştur' butonu, boş etüt saatlerini senin eksiklerine ve LGS müfredatına göre otomatik doldurur.")
    
    with col2:
        scheduler = get_scheduler_engine()
        
        # --- VELİ KİMLİK DOĞRULAMA ---
        is_parent = st.session_state.get("is_parent_logged_in", False)
        
        if not is_parent:
            # Giriş Yapılmamışsa
            with st.expander("🔒 Veli Girişi (Düzenleme İçin)", expanded=True):
                st.info("Programı değiştirmek için veli girişi gereklidir.")
                pin = st.text_input("PIN Kodu", type="password", help="Varsayılan: 1234", key="sched_pin")
                if st.button("Giriş Yap", key="btn_login_sched"):
                    if pin == "1234":
                        st.session_state["is_parent_logged_in"] = True
                        st.success("Giriş Başarılı!")
                        st.rerun()
                    else:
                        st.error("Hatalı PIN!")
        else:
            # Giriş Yapılmışsa -> Kontrolleri Göster
            
            # Veli Kontrol Paneli / Ayarlar
            with st.expander("⚙️ Program Ayarları & Öncelikler (Veli Kontrol)", expanded=False):
                st.markdown("##### 🎯 Haftalık Ders Hedefleri")
                st.caption("ℹ️ Bu ayarlar **haftalık programın tamamına** uygulanır.")
                
                all_lessons = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "İngilizce", "Din Kültürü"]
                default_lessons = ["Matematik", "Fen Bilimleri", "Türkçe"]
                
                selected_lessons = st.multiselect(
                    "📅 Programa Dahil Edilecek Dersler",
                    all_lessons,
                    default=default_lessons,
                    help="Sadece seçili derslerden konu ataması yapılır."
                )
                
                custom_weights = {}
                topic_weights = {}
                
                if selected_lessons:
                    st.markdown("###### ⚖️ Ders ve Konu Ağırlıkları")
                    
                    # Create tabs or columns? Columns is better for side-by-side or vertical list.
                    # Given description, user wants "Subject Weight" -> "Subject Topics"
                    
                    for i, lesson in enumerate(selected_lessons):
                        with st.container(): # Group by lesson
                            st.markdown(f"**📚 {lesson}**")
                            col_l1, col_l2 = st.columns([1, 1])
                            
                            with col_l1:
                                # Ders Ağırlığı
                                weight = st.slider(f"{lesson} Genel Önemi", 0, 100, 50, 10, key=f"w_{lesson}")
                                custom_weights[lesson] = weight
                            
                            with col_l2:
                                # O derse ait konuları çek
                                if not scheduler.curriculum.empty:
                                    # Filter by lesson
                                    lesson_df = scheduler.curriculum[scheduler.curriculum['lesson'] == lesson]
                                    
                                    # Format: "Topic (Subtopic)" for granular selection
                                    # Use apply to create the comprehensive label
                                    topic_options = lesson_df.apply(
                                        lambda x: f"{x['topic']} ({x['subtopic']})", axis=1
                                    ).unique().tolist()
                                    
                                    selected_topics = st.multiselect(
                                        f"🎯 {lesson} - Öncelikli Konular",
                                        options=sorted(topic_options),
                                        key=f"t_sel_{lesson}",
                                        help="Bu derste özellikle ağırlık vermek istediğiniz alt konuları seçin. (Örn: 'EKOK' yazıp arayabilirsiniz)"
                                    )
                                    
                                    # Seçilen konular için ağırlık slider'ı
                                    if selected_topics:
                                        for t in selected_topics:
                                            t_w = st.slider(f"   ↳ {t} Önemi", 0, 100, 80, 10, key=f"tw_{t}")
                                            topic_weights[t] = t_w
                                else:
                                    st.warning("Konu listesi yüklenemedi.")
                            st.divider()

                else:
                    st.warning("⚠️ Lütfen en az bir ders seçin!")
                
                st.markdown("---")
                preserve_manual = st.checkbox("🔒 Manuel Ayarlanan Dersleri Koru", value=True, help="Eğer işaretli ise, elle değiştirdiğiniz bloklara (Örn: Özel Ders) dokunulmaz.")
            
            # Akıllı Program Oluştur Butonu
            if st.button("🚀 Akıllı Program Oluştur", type="primary", use_container_width=True):
                with st.spinner("Yapay zeka programını hazırlıyor..."):
                    schedule_data = scheduler.generate_weekly_schedule(
                        custom_weights=custom_weights,
                        topic_weights=topic_weights,
                        preserve_manual=preserve_manual
                    )
                    st.session_state['generated_schedule'] = schedule_data
                    st.success("Program başarıyla güncellendi!")
                    st.rerun()
            
            if st.button("🔓 Çıkış Yap (Veli)", key="btn_logout_sched"):
                st.session_state["is_parent_logged_in"] = False
                st.rerun()

    # --- Manuel Düzenleme (Data Editor) ---
    if st.session_state.get('generated_schedule') and is_parent:
        
        # Müfredat Yönetimi Çıkarıldı (Kullanıcı İsteği)
        
        with st.expander("🛠️ Programı Elle Düzenle (Veli)", expanded=False):
            st.info("Aşağıdaki tablodan dersleri ve konuları veritabanından seçebilirsiniz.")
            
            # Curriculum verisini hazırla (Selectbox seçenekleri için)
            if not scheduler.curriculum.empty:
                # 1. Ders Listesi
                raw_lessons = sorted(scheduler.curriculum['lesson'].unique().tolist())
                lesson_options = [f"📚 {l}" for l in raw_lessons] + ["☕ Molası", "Danışmanlık", "Diğer"]
                
                # 2. Konu Listesi (DERS - KONU formatında) -> Filtreleme kolaylığı için
                topic_options = []
                for _, row in scheduler.curriculum.iterrows():
                    # Format: "Matematik - Çarpanlar ve Katlar (EBOB...)"
                    topic_str = f"{row['lesson']} - {row['topic']} ({row['subtopic']})"
                    topic_options.append(topic_str)
                
                # Manuel eklemeler
                topic_options = sorted(list(set(topic_options))) + ["Konu Çalışması", "Soru Çözümü", "Deneme Sınavı", "Mola"]
            else:
                lesson_options = []
                topic_options = []

            # DataFrame'i düzenlenebilir yap
            current_df = pd.DataFrame(st.session_state['generated_schedule'])
            
            # Gerekli kolonları seç
            edit_df = current_df[['day_of_week', 'block_start', 'block_end', 'target_desc', 'task_type', 'block_type']].copy()
            
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                num_rows="fixed",
                column_config={
                    "day_of_week": st.column_config.TextColumn("Gün", disabled=True),
                    "block_start": st.column_config.TextColumn("Başlangıç", disabled=True),
                    "block_end": st.column_config.TextColumn("Bitiş", disabled=True),
                    
                    "task_type": st.column_config.SelectboxColumn(
                        "Ders (Seçmeli)",
                        options=lesson_options,
                        help="Ders veya aktivite türünü seçin",
                        required=False
                    ),
                    
                    "target_desc": st.column_config.SelectboxColumn(
                        "Konu / Hedef (Seçmeli)",
                        options=topic_options,
                        help="Çalışılacak konuyu listeden seçin",
                        required=False
                    ),
                    
                    "block_type": st.column_config.SelectboxColumn(
                        "Blok Tipi",
                        options=["etut", "mola", "uzun_mola", "ozel_ders"],
                        required=True
                    )
                },
                key="schedule_editor"
            )
            
            if st.button("💾 Değişiklikleri Kaydet"):
                # Orijinal veriyi güncelle
                new_schedule = st.session_state['generated_schedule']
                for idx, row in edited_df.iterrows():
                    new_schedule[idx]['target_desc'] = row['target_desc']
                    new_schedule[idx]['task_type'] = row['task_type']
                    new_schedule[idx]['block_type'] = row['block_type']
                    
                st.session_state['generated_schedule'] = new_schedule
                st.success("Program güncellendi!")
                st.rerun()
                
    st.markdown("---")
    
    # Program Verisi (Session State veya Yeni Oluşturulan)
    schedule_data = st.session_state.get('generated_schedule', [])
    
    if not schedule_data:
        # Eğer session'da yoksa, mevcut schedule.csv'yi (template) veya direk scheduler'dan çekmeyi dene
        # Ama scheduler.generate_weekly_schedule() her çağrıda yeni konu atayabilir mi? Evet.
        # İlk yüklemede belki sadece template göster, veya son kaydedileni göster.
        # Şimdilik: Kullanıcı butona basınca oluşsun.
        st.warning("⚠️ Henüz bir program oluşturmadın. Yukarıdaki butona basarak başlayabilirsin.")
    else:
        # Takvime Ekle Butonu
        exporter = CalendarExporter()
        ics_content = exporter.generate_ics(schedule_data)
        
        col_dl1, col_dl2 = st.columns([1, 1])
        with col_dl1:
            st.download_button(
                label="📅 Takvimine Ekle (.ics İndir)",
                data=ics_content,
                file_name="LGS_Programi.ics",
                mime="text/calendar",
                use_container_width=True,
                help="Bu dosyayı indirip telefonunda veya bilgisayarında açarsan programın takvimine işlenir."
            )
        
        # Programı Görselleştirme
        df = pd.DataFrame(schedule_data)
        
        # Gün Bazlı Gösterim (Tabs)
        days_map = {
            "Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba", 
            "Thursday": "Perşembe", "Friday": "Cuma", "Saturday": "Cumartesi", "Sunday": "Pazar"
        }
        
        # Sıralama için
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        tabs = st.tabs([days_map[d] for d in day_order])
        
        for i, day_eng in enumerate(day_order):
            with tabs[i]:
                day_blocks = df[df['day_of_week'] == day_eng]
                
                if day_blocks.empty:
                    st.info("Bu gün için plan yok.")
                else:
                    for _, block in day_blocks.iterrows():
                        # Kart tasarımı
                        if block['block_type'] == 'etut':
                            border_color = "#2E86AB" # Mavi
                            bg_color = "#E3F2FD"
                            icon = "📚"
                        elif block['block_type'] == 'mola' or block['block_type'] == 'uzun_mola':
                            border_color = "#FFC107" # Sarı
                            bg_color = "#FFF3CD"
                            icon = "☕"
                        else:
                            border_color = "#CED4DA"
                            bg_color = "#F8F9FA"
                            icon = "⏰"
                            
                        st.markdown(f"""
                        <div style='
                            background-color: {bg_color};
                            border-left: 5px solid {border_color};
                            padding: 1rem;
                            border-radius: 8px;
                            margin-bottom: 0.8rem;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                        '>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <strong style='font-size: 1.1rem; color: #2B2D42;'>{icon} {block['target_desc']}</strong>
                                    <br>
                                    <span style='font-size: 0.9rem; color: #6C757D;'>{block.get('task_type', '')}</span>
                                </div>
                                <div style='text-align: right;'>
                                    <span style='font-weight: bold; color: {border_color};'>{block['block_start']} - {block['block_end']}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
