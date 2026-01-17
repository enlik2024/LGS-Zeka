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
            
            # ⏰ ZAMAN AYARLARI (Ayrı ve Görünür Bölüm)
            with st.expander("⏰ Zaman ve Gün Ayarları", expanded=True):
                st.caption("Programın başlama saatini ve aktif günlerini buradan ayarlayın.")
                
                from datetime import time as dt_time
                col_time1, col_time2 = st.columns(2)
                with col_time1:
                    start_time = st.time_input(
                        "Günlük Başlangıç Saati", 
                        value=dt_time(15, 0),
                        help="Programın her gün hangi saatten başlayacağını belirleyin.",
                        key="schedule_start_time"
                    )
                    
                with col_time2:
                    num_blocks = st.number_input(
                        "Günlük Ders Bloku Sayısı",
                        min_value=3,
                        max_value=8,
                        value=5,
                        help="Her gün kaç ders bloku (mola hariç) olsun?",
                        key="schedule_num_blocks"
                    )
                
                all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                day_labels = {"Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba", 
                              "Thursday": "Perşembe", "Friday": "Cuma", "Saturday": "Cumartesi", "Sunday": "Pazar"}
                
                active_days = st.multiselect(
                    "📅 Aktif Günler",
                    options=all_days,
                    default=all_days,
                    format_func=lambda x: day_labels.get(x, x),
                    help="Programın hangi günlerde oluşturulacağını seçin."
                )
                
                # Ders ve Mola Süreleri
                st.markdown("---")
                st.markdown("##### ⏱️ Ders ve Mola Süreleri")
                
                col_dur1, col_dur2, col_dur3 = st.columns(3)
                with col_dur1:
                    block_duration = st.number_input(
                        "Ders Bloku (dk)",
                        min_value=20,
                        max_value=60,
                        value=30,
                        step=5,
                        help="Her ders blokunun süresi (dakika)",
                        key="schedule_block_duration"
                    )
                    
                with col_dur2:
                    short_break = st.number_input(
                        "Kısa Mola (dk)",
                        min_value=5,
                        max_value=20,
                        value=10,
                        step=5,
                        help="Kısa molalar (her ders arası)",
                        key="schedule_short_break"
                    )
                    
                with col_dur3:
                    long_break = st.number_input(
                        "Uzun Mola / Yemek (dk)",
                        min_value=15,
                        max_value=60,
                        value=30,
                        step=5,
                        help="Uzun molalar (her X derste bir)",
                        key="schedule_long_break"
                    )
                    
                long_break_interval = st.number_input(
                    "🍛 Kaç Derste Bir Uzun Mola?",
                    min_value=1,
                    max_value=8,
                    value=2,
                    help="Örneğin 2 seçerseniz: Ders-Ders-UZUN MOLA-Ders-Ders... şeklinde gider.",
                    key="schedule_long_break_int"
                )
            
            # Veli Kontrol Paneli / Ders Ağırlıkları
            with st.expander("⚙️ Ders Ağırlıkları & Öncelikler (Opsiyonel)", expanded=False):
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
                
                preserve_manual = st.checkbox("🔒 Manuel Ayarlanan Dersleri Koru", value=True, help="Eğer işaretli ise, elle değiştirdiğiniz bloklara (Örn: Özel Ders) dokunulmaz.")
            
            # Akıllı Program Oluştur Butonu
            if st.button("🚀 Akıllı Program Oluştur", type="primary", use_container_width=True):
                with st.spinner("Yapay zeka programını hazırlıyor..."):
                    schedule_data = scheduler.generate_weekly_schedule(
                        custom_weights=custom_weights,
                        topic_weights=topic_weights,
                        preserve_manual=preserve_manual,
                        start_time=start_time,
                        num_blocks=int(num_blocks),
                        active_days=active_days,
                        block_duration=int(block_duration),
                        short_break=int(short_break),
                        long_break=int(long_break),
                        long_break_interval=int(long_break_interval)
                    )
                    # DB'ye kaydet
                    scheduler.save_active_schedule(schedule_data)
                    
                    st.session_state['generated_schedule'] = schedule_data
                    st.success("Program başarıyla güncellendi ve kaydedildi!")
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
            
            # Eksik kolonları varsayılan değerlerle doldur (DB'den yüklendiğinde bazı alanlar eksik olabilir)
            if 'task_type' not in current_df.columns:
                current_df['task_type'] = current_df.get('lesson', 'Genel')
            if 'block_start' not in current_df.columns:
                current_df['block_start'] = current_df.get('block_time', '').str.split(' - ').str[0]
            if 'block_end' not in current_df.columns:
                current_df['block_end'] = current_df.get('block_time', '').str.split(' - ').str[1]
            
            # Gerekli kolonları seç
            edit_df = current_df[['day_of_week', 'block_start', 'block_end', 'target_desc', 'task_type', 'block_type']].copy()
            
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                num_rows="fixed",
                column_config={
                    "day_of_week": st.column_config.TextColumn("Gün", disabled=True),
                    "block_start": st.column_config.TextColumn("Başlangıç (SS:DD)", disabled=False, help="Örn: 14:30"),
                    "block_end": st.column_config.TextColumn("Bitiş (SS:DD)", disabled=False, help="Örn: 15:00"),
                    
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
            
            cascade_updates = st.checkbox("⏳ Saatleri Zincirleme Güncelle", value=False, help="Bir dersin saatini değiştirdiğinizde, sonraki derslerin saatlerini otomatik olarak kaydırır (süreleri koruyarak).")
            
            if st.button("💾 Değişiklikleri Kaydet"):
                # Orijinal veriyi güncelle
                new_schedule = st.session_state['generated_schedule']
                
                # Zincirleme Güncelleme Mantığı (Opsiyonel)
                if cascade_updates:
                    from datetime import datetime, timedelta
                    
                    # Gün bazında gruplayıp işle
                    edited_df['day_sort'] = pd.Categorical(edited_df['day_of_week'], categories=all_days, ordered=True)
                    edited_df = edited_df.sort_values(['day_sort', 'block_start'])
                    
                    # Her gün için ayrı işlem yap
                    for day in all_days:
                        day_mask = edited_df['day_of_week'] == day
                        if not day_mask.any():
                            continue
                            
                        day_indices = edited_df[day_mask].index
                        
                        # İlk bloğun başlangıç zamanını referans al
                        # Sonraki bloklar: Önceki Bitiş -> Yeni Başlangıç
                        prev_end_time = None
                        
                        for idx in day_indices:
                            row = edited_df.loc[idx]
                            
                            current_start_str = row['block_start']
                            current_end_str = row['block_end']
                            
                            try:
                                # Süreyi hesapla (Mevcut satırın süresini koru)
                                t_fmt = "%H:%M"
                                t_start = datetime.strptime(current_start_str, t_fmt)
                                t_end = datetime.strptime(current_end_str, t_fmt)
                                duration = (t_end - t_start).total_seconds() / 60
                                
                                if prev_end_time:
                                    # Başlangıcı önceki bitişe eşitle (Zincirleme)
                                    new_start = prev_end_time
                                    new_end = new_start + timedelta(minutes=duration)
                                    
                                    # DataFrame'i güncelle
                                    edited_df.at[idx, 'block_start'] = new_start.strftime(t_fmt)
                                    edited_df.at[idx, 'block_end'] = new_end.strftime(t_fmt)
                                    
                                    prev_end_time = new_end
                                else:
                                    # İlk blok - Bitiş zamanını referans olarak sakla
                                    prev_end_time = t_end
                                    
                            except Exception as e:
                                print(f"Time Calc Error: {e}")
                                continue

                # Güncellenmiş DataFrame'i kaydet
                for idx, row in edited_df.iterrows():
                    new_schedule[idx]['target_desc'] = row['target_desc']
                    new_schedule[idx]['task_type'] = row['task_type']
                    new_schedule[idx]['block_type'] = row['block_type']
                    # Saatleri de güncelle
                    new_schedule[idx]['block_start'] = row['block_start']
                    new_schedule[idx]['block_end'] = row['block_end']
                    
                st.session_state['generated_schedule'] = new_schedule
                
                
                # DB'ye kaydet
                scheduler.save_active_schedule(new_schedule)
                
                st.success("Program güncellendi ve kaydedildi!")
                st.rerun()
                
    st.markdown("---")
    
    # Program Verisi (Session State veya DB'den)
    if 'generated_schedule' not in st.session_state:
        # DB'den yüklemeyi dene
        loaded_schedule = scheduler.load_active_schedule()
        if loaded_schedule:
             st.session_state['generated_schedule'] = loaded_schedule
    
    schedule_data = st.session_state.get('generated_schedule', [])
    
    if not schedule_data:
        # Eğer session'da ve DB'de yoksa
        st.warning("⚠️ Henüz bir program oluşturmadın. Yukarıdaki butona basarak veya 'Dersleri Seçip' program oluşturabilirsin.")
    else:
        # Takvime Ekle Butonu / Magic Link
        exporter = CalendarExporter()
        ics_content = exporter.generate_ics(schedule_data)
        
        col_dl1, col_dl2 = st.columns([1, 1])
        with col_dl1:
            st.download_button(
                label="📥 Dosya Olarak İndir (.ics)",
                data=ics_content,
                file_name="LGS_Programi.ics",
                mime="text/calendar",
                use_container_width=True,
                help="Manuel ekleme için dosyayı indirir."
            )
            
        with col_dl2:
            # Otomatik Bulut Senkronizasyonu (Magic Link)
            if st.button("🔄 Buluta Yükle & Link Al", type="primary", use_container_width=True, help="Google Takvim'e abone olmak için sabit link oluşturur."):
                with st.spinner("Takvim buluta yükleniyor..."):
                    # Veritabanı yöneticisi üzerinden yükle
                    public_url = scheduler.db.upload_calendar_file(ics_content, "pilot_ogrenci_01")
                    
                    if public_url:
                        st.session_state['calendar_url'] = public_url
                        st.success("Takvim başarıyla senkronize edildi! ☁️")
                    else:
                        st.error("Yükleme başarısız. Supabase Storage ayarlarını kontrol edin.")

        # Eğer link varsa göster
        if st.session_state.get('calendar_url'):
            st.info("👇 Bu linki Google Takvim'de 'URL ile Ekle' kısmına yapıştırın:")
            st.code(st.session_state['calendar_url'], language="text")
            st.caption("Bu link sabittir. Programı her güncellediğinizde 'Buluta Yükle' derseniz takviminiz otomatik güncellenir.")
        
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
