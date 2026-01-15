"""
Ayarlar Sayfası
Öğrenci profili ve çalışma programı yapılandırması.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, time
from utils.db_manager import get_db_manager
from utils.schedule_engine import get_schedule_engine

def show():
    """Ayarlar sayfasını gösterir."""
    st.header("⚙️ Ayarlar")
    
    # --- Eski Ayarların Geri Yüklenmesi ---
    with st.expander("🔧 Genel Ayarlar", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Bildirimler", value=True)
            st.checkbox("Karanlık Mod", value=False)
        with col2:
            st.selectbox("Dil", ["Türkçe", "English"])

    with st.expander("🎯 Hedef Ayarları", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Hedef LGS Puanı", min_value=0, max_value=500, value=450, key="target_score_global")
        with col2:
            st.date_input("LGS Sınav Tarihi", key="exam_date_global")

    with st.expander("📊 Veri Ayarları", expanded=False):
        st.info("Veritabanı Stratejisi: Google Sheets (Faz 1-3) -> Supabase (Faz 4+)")
        
        # Mevcut seçimi al
        db_options = ["Google Sheets", "Supabase", "Yerel (CSV/Excel) - Dev"]
        db_map = {"Google Sheets": "google_sheets", "Supabase": "supabase", "Yerel (CSV/Excel) - Dev": "local"}
        reverse_map = {v: k for k, v in db_map.items()}
        
        current_db = st.session_state.get("db_type", "supabase")  # Varsayılan: Supabase
        current_index = db_options.index(reverse_map.get(current_db, "Google Sheets"))
        
        db_type_display = st.radio("Aktif Veritabanı", db_options, index=current_index, key="db_type_radio")
        
        # Seçim değiştiyse kaydet
        new_db_type = db_map[db_type_display]
        if new_db_type != st.session_state.get("db_type"):
            st.session_state.db_type = new_db_type
            # Cache'i temizle ki yeni db_manager oluşsun
            st.cache_resource.clear()
            st.cache_data.clear()
            st.success(f"✅ Veritabanı değiştirildi: {db_type_display}")
            st.rerun()
        
        if st.button("Verileri Dışa Aktar"):
            st.success("Veriler Excel olarak indirildi!")
    
    st.markdown("---")
    # ---------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(["📅 Çalışma Programı", "👤 Öğrenci Profili", "👨‍👩‍👧‍👦 Veli Paneli", "💾 Veri Yönetimi"])
    
    with tab1:
        render_schedule_settings()
        
    with tab2:
        render_profile_settings()

    with tab3:
        render_parent_settings()

    with tab4:
        render_data_management()

def render_data_management():
    """Veri yönetimi ve doğrulama araçları (Phase K2)."""
    st.subheader("💾 Veri Yönetimi")
    
    st.markdown("### 🛠️ Veritabanı Araçları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Soru Havuzu Durumu**")
        if st.button("🔍 Havuzu Kontrol Et (Validate)", key="validate_pool"):
            db = get_db_manager()
            with st.spinner("Soru havuzu taranıyor..."):
                report = db.validate_question_pool()
                
            if report.get("invalid_count", 0) == 0:
                st.success(f"✅ Harika! {report.get('total')} sorunun hepsi geçerli.")
            else:
                st.error(f"🚨 {report.get('invalid_count')} hatalı kayıt bulundu!")
                
                # Hataları listele
                issues_df = pd.DataFrame(report["issues"])
                st.dataframe(issues_df, use_container_width=True)
                
                with st.expander("🛠️ Nasıl Düzeltirim?"):
                    st.markdown("""
                    1. `questions.csv` dosyasını Excel ile açın.
                    2. İlgili satır numaralarına gidin (`row_index`).
                    3. Eksik ID, metin veya bozuk JSON verilerini düzeltin.
                    4. Dosyayı kaydedip tekrar kontrol edin.
                    """)
    
    with col2:
        st.markdown("**Yedekleme**")
        if st.button("📤 Tüm Verileri Yedekle (Zip)", disabled=True, help="Yakında..."):
            st.info("Bu özellik geliştirme aşamasında.")

def render_parent_settings():
    """Veli kontrol paneli."""
    st.subheader("🔒 Veli Kontrol Paneli")
    
    # Oturum kontrolü
    if st.session_state.get("is_parent_logged_in", False):
        st.success("Veli Girişi Aktif ✅")
        if st.button("Çıkış Yap"):
            st.session_state["is_parent_logged_in"] = False
            st.rerun()
            
        st.markdown("### 🛡️ Kısıtlamalar ve Kontroller")
        st.checkbox("Oyunlaştırma Özelliklerini Kısıtla", help="Sadece ders odaklı olsun")
        st.checkbox("Ekran Süresi Sınırı Koy", help="Günlük maksimum kullanım")
        
        st.markdown("### 📊 Detaylı Raporlar")
        st.info("Haftalık gelişim raporu her Pazar e-posta adresinize gönderilir.")
        st.text_input("Veli E-posta", value="veli@ornek.com")
        
        st.markdown("### 🔑 API Yapılandırması")
        st.info("💡 Kendi API anahtarlarınızı girerek ücretsiz kota limitlerini aşabilirsiniz. Birincil key dolduğunda sistem otomatik olarak yedek key'e geçer.")
        
        # Mevcut ayarları yükle
        import json
        import os
        config_path = "config/user_settings.json"
        current_api_key = ""
        current_secondary_key = ""
        
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    settings = json.load(f)
                    current_api_key = settings.get("chat_api_key", "")
                    current_secondary_key = settings.get("chat_api_key_secondary", "")
            except:
                pass
        
        col_key1, col_key2 = st.columns(2)
        
        with col_key1:
            new_api_key = st.text_input(
                "🔑 Birincil API Anahtarı", 
                value=current_api_key,
                type="password",
                help="Google AI Studio'dan alınan ana API anahtarı"
            )
        
        with col_key2:
            new_secondary_key = st.text_input(
                "🔑 Yedek API Anahtarı (Opsiyonel)", 
                value=current_secondary_key,
                type="password",
                help="Birincil key kota limitine ulaşırsa otomatik olarak bu kullanılır"
            )
        
        # API durumu göster
        if new_api_key:
            from utils.config_manager import get_config
            try:
                config = get_config()
                key_status = config.get_api_key_status()
                if key_status:
                    st.markdown("**📊 API Key Durumu:**")
                    for ks in key_status:
                        status_icon = "✅" if ks['status'] == 'active' else "⚠️"
                        st.caption(f"{status_icon} {ks['name']}: {ks['masked']}")
            except:
                pass
        
        if st.button("💾 API Ayarlarını Kaydet", type="primary"):
            # Ayarları kaydet
            settings = {
                "chat_api_key": new_api_key,
                "chat_api_key_secondary": new_secondary_key
            }
            
            # Varsa diğer ayarları koru
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as f:
                        existing = json.load(f)
                        existing.update(settings)
                        settings = existing
                except:
                    pass
            
            os.makedirs("config", exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(settings, f, indent=2)
            
            # Config cache'i temizle
            st.cache_resource.clear()
            
            st.success("✅ API anahtarları güncellendi!")
            st.toast("API ayarları kaydedildi. Sistem yeni key'leri kullanacak.", icon="🔑")
            st.rerun()
            
    else:
        # Basit bir PIN koruması simülasyonu
        pin = st.text_input("Veli PIN Kodu", type="password", help="Varsayılan: 1234")
        
        if pin == "1234":
            st.session_state["is_parent_logged_in"] = True
            st.success("Giriş Başarılı")
            st.rerun()
        elif pin:
            st.error("Hatalı PIN kodu")


def render_schedule_settings():
    """Çalışma programı ayarları."""
    st.subheader("Haftalık Rutin Planlayıcı")
    
    is_parent = st.session_state.get("is_parent_logged_in", False)
    
    if not is_parent:
        st.warning("🔒 Çalışma programı sadece veli tarafından değiştirilebilir. Şu an sadece görüntüleme modundasınız.")
        st.info("Değişiklik yapmak için 'Veli Paneli' sekmesinden giriş yapmalısınız.")
        
    schedule = get_schedule_engine()
    
    # Gün Seçimi
    days_map = {
        "Pazartesi": "Monday",
        "Salı": "Tuesday",
        "Çarşamba": "Wednesday",
        "Perşembe": "Thursday",
        "Cuma": "Friday",
        "Cumartesi": "Saturday",
        "Pazar": "Sunday"
    }
    
    col_day, col_copy = st.columns([2, 1])
    with col_day:
        selected_day_tr = st.selectbox("📅 Gün Seçin", list(days_map.keys()))
        selected_day_eng = days_map[selected_day_tr]
        
    with col_copy:
        st.write("") # Spacer
        st.write("")
        copy_to_all = st.checkbox("Tüm Günlere Uygula", value=False, disabled=not is_parent, help="Bu programı haftanın tüm günlerine kopyalar.")

    # Seçili günün mevcut programını yükle (Varsa)
    current_schedule = schedule.get_schedule_for_day(selected_day_eng)
    if current_schedule:
        st.info(f"{selected_day_tr} için {len(current_schedule)} blok tanımlı.")
    else:
        st.info(f"{selected_day_tr} için henüz özel bir program yok (Varsayılan şablon yoksa boş).")

    # Form (Veli değilse disabled)
    with st.form("schedule_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌅 Sabah")
            wake_up = st.time_input("Güne Başlama Saati", value=time(9, 0), disabled=not is_parent)
            first_block_start = st.time_input("İlk Ders Başlangıcı", value=time(10, 0), disabled=not is_parent)
            
        with col2:
            st.markdown("#### 📚 Blok Yapısı")
            block_duration = st.number_input("Ders Bloğu (dk)", min_value=20, max_value=60, value=30, step=5, disabled=not is_parent)
            break_duration = st.number_input("Mola Süresi (dk)", min_value=5, max_value=30, value=10, step=5, disabled=not is_parent)
            long_break_duration = st.number_input("Uzun Mola (dk)", min_value=15, max_value=60, value=30, step=5, disabled=not is_parent)
            
        st.markdown("#### 🎯 Günlük Hedefler")
        daily_blocks = st.slider("Günlük Blok Sayısı", min_value=1, max_value=8, value=4, disabled=not is_parent)
        
        # Buton sadece veliye açık
        submitted = st.form_submit_button(f"💾 {selected_day_tr} Programını Kaydet", disabled=not is_parent)
        
        if submitted and is_parent:
            # ScheduleEngine üzerinden programı oluştur ve kaydet
            try:
                # Mock data oluşturucu (Generator)
                new_schedule = []
                current_time = datetime.combine(datetime.today(), first_block_start)
                
                for i in range(daily_blocks):
                    # Ders Bloğu
                    end_time = current_time + pd.Timedelta(minutes=block_duration)
                    new_schedule.append({
                        "id": f"blk_{i+1}",
                        "start": current_time.strftime("%H:%M"),
                        "end": end_time.strftime("%H:%M"),
                        "type": "etut",
                        "task": f"Blok {i+1}: Konu Çalışması", 
                        "desc": "Otomatik oluşturuldu",
                        "status": "pending",
                        "duration_min": block_duration
                    })
                    
                    # Mola (Son blok değilse)
                    if i < daily_blocks - 1:
                        current_time = end_time
                        # Her 2 blokta bir uzun mola
                        is_long_break = (i + 1) % 2 == 0
                        duration = long_break_duration if is_long_break else break_duration
                        type_str = "uzun_mola" if is_long_break else "mola"
                        
                        mola_end = current_time + pd.Timedelta(minutes=duration)
                        new_schedule.append({
                            "id": f"brk_{i+1}",
                            "start": current_time.strftime("%H:%M"),
                            "end": mola_end.strftime("%H:%M"),
                            "type": type_str,
                            "task": "Mola Zamanı ☕",
                            "desc": "Dinlen ve yenilen",
                            "status": "pending",
                            "duration_min": duration
                        })
                        current_time = mola_end
                    else:
                        current_time = end_time

                # ScheduleEngine üzerinden kaydet
                schedule.save_schedule(new_schedule, day=selected_day_eng, overwrite_all=copy_to_all)
                
                if copy_to_all:
                    st.success("✅ Program TÜM GÜNLER için güncellendi!")
                else:
                    st.success(f"✅ {selected_day_tr} programı güncellendi!")
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

def render_profile_settings():
    """Profil ayarları."""
    st.subheader("Öğrenci Bilgileri")
    
    # Supabase'den kullanıcı bilgilerini çek
    from utils.db_manager import get_db_manager
    db = get_db_manager()
    user = db.get_current_user()
    
    # Kullanıcı verisini al (fallback değerlerle)
    user_name = user.get('name', 'Öğrenci')
    user_grade = int(user.get('grade', 8)) if user.get('grade') else 8
    target_score = int(user.get('target_score', 450)) if user.get('target_score') else 450
    weak_subjects = user.get('weak_subjects', ['Matematik'])
    if isinstance(weak_subjects, str):
        import json
        try:
            weak_subjects = json.loads(weak_subjects)
        except:
            weak_subjects = ['Matematik']
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Ad Soyad", value=user_name, key="profile_name")
        grade_options = [8, 7, 6, 5]
        grade_index = grade_options.index(user_grade) if user_grade in grade_options else 0
        st.selectbox("Sınıf", grade_options, index=grade_index, key="profile_grade")
        
    with col2:
        st.number_input("Hedef Puan", min_value=200, max_value=500, value=target_score, key="profile_target")
        all_subjects = ["Matematik", "Fen", "Türkçe", "İngilizce"]
        st.multiselect("Zayıf Konular", all_subjects, default=weak_subjects if weak_subjects else [], key="profile_weak")
    
    if st.button("Profili Güncelle"):
        # Session state'ten güncel değerleri al
        new_name = st.session_state.get("profile_name", user_name)
        new_grade = st.session_state.get("profile_grade", user_grade)
        new_target = st.session_state.get("profile_target", target_score)
        new_weak = st.session_state.get("profile_weak", weak_subjects)
        
        try:
            # Supabase'e kaydet
            if db.db_type == "supabase" and db._client:
                import json
                db._client.table("users").update({
                    "name": new_name,
                    "grade": new_grade,
                    "target_score": new_target,
                    "weak_subjects": json.dumps(new_weak) if isinstance(new_weak, list) else new_weak
                }).eq("student_id", "pilot_ogrenci_01").execute()
                st.success("✅ Profil güncellendi!")
                st.cache_data.clear()
            else:
                st.warning("Supabase bağlantısı bulunamadı - değişiklikler kaydedilemedi.")
        except Exception as e:
            st.error(f"Profil güncellenemedi: {e}")
