"""
Mini Deneme Sayfası
Sabit ve adaptif deneme sınavı arayüzü.
"""

import streamlit as st
import sys
from pathlib import Path
import time

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.exam_engine import get_exam_engine
from utils.gamification import get_gamification_manager

def show():
    """Mini Deneme sayfasını gösterir."""
    
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #FF6B6B;'>📝 Mini Deneme</h1>
            <p style='color: #6C757D; font-size: 1.1rem;'>
                Kendini dene, eksiklerini gör.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    engine = get_exam_engine()
    gm = get_gamification_manager()
    
    # Session state yönetimi
    if 'active_exam' not in st.session_state:
        st.session_state.active_exam = None
    if 'exam_answers' not in st.session_state:
        st.session_state.exam_answers = {}
    if 'exam_submitted' not in st.session_state:
        st.session_state.exam_submitted = False
        
    # Eğer aktif sınav yoksa -> Seçim Ekranı
    if not st.session_state.active_exam:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #4ECDC4 0%, #556270 100%);
                padding: 1.5rem;
                border-radius: 15px;
                color: white;
                height: 100%;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            '>
                <h2 style='color: white; margin: 0;'>🎲 Konu Tarama</h2>
                <p style='color: white; opacity: 0.9; margin-top: 0.5rem;'>
                    Seçtiğin dersten rastgele 10 soru ile kendini dene.
                </p>
                <div style='margin-top: 1rem; font-size: 3rem;'>📚</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Sınav Tipi ve Modu Seçimi
            type_col, mode_col = st.columns(2)
            with type_col:
                exam_type = st.radio("Sınav Tipi", ["Standart (Konu Tarama)", "Adaptif (Kişiye Özel)"], horizontal=True)
            with mode_col:
                exam_mode = st.radio("Sınav Modu", ["Online", "Kağıt (Çıktı)"], horizontal=True)
            
            st.markdown("---")
            
            # Ders ve Konu Seçimi (Sadece Standart Modda)
            lesson = "Karma"
            topic = "Tümü"
            
            if exam_type == "Standart (Konu Tarama)":
                from utils.db_manager import get_db_manager
                db = get_db_manager()
                curriculum = db.load_curriculum_map()
                
                lesson = st.selectbox("Ders Seç", ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "İngilizce", "Din Kültürü"])
                
                topics = ["Tümü"]
                if not curriculum.empty and lesson:
                    lesson_topics = curriculum[curriculum['lesson'] == lesson]['topic'].unique().tolist()
                    topics += lesson_topics
                    
                topic = st.selectbox("Konu Seç", topics)
            else:
                st.info("🧠 **Adaptif Mod:** Yapay zeka senin eksiklerini analiz etti ve sana özel bir deneme hazırlayacak.")
            
            # Soru Sayısı ve Süre Ayarı
            num_questions = st.slider("Soru Sayısı", min_value=5, max_value=20, value=10, step=5)
            
            # Süre Hesaplama (LGS Standartları)
            # Sözel: 75 dk / 50 soru = 1.5 dk/soru
            # Sayısal: 80 dk / 40 soru = 2.0 dk/soru
            is_numerical = lesson in ["Matematik", "Fen Bilimleri", "Karma"]
            time_per_question = 2.0 if is_numerical else 1.5
            total_duration_min = int(num_questions * time_per_question)
            
            st.info(f"⏱️ Sınav Süresi: **{total_duration_min} dakika** ({time_per_question} dk/soru)")
            
            btn_text = "Başlat (Standart)" if "Standart" in exam_type else "Başlat (Adaptif)"
            if st.button(btn_text, type="primary", use_container_width=True):
                with st.spinner("Sınav hazırlanıyor..."):
                    if "Standart" in exam_type:
                        exam = engine.create_fixed_exam(lesson, topic=topic if topic != "Tümü" else None, num_questions=num_questions)
                    else:
                        # Adaptif Sınav Oluştur
                        exam = engine.create_adaptive_exam(student_id="pilot_ogrenci_01", num_questions=num_questions)
                        
                    if exam:
                        # Süre bilgisini exam objesine ekle
                        exam['duration_min'] = total_duration_min
                        exam['start_time'] = time.time()
                        exam['mode_preference'] = exam_mode
                        
                    st.session_state.active_exam = exam
                    st.session_state.exam_answers = {}
                    st.session_state.exam_submitted = False
                    # Online ise hemen başlat, Kağıt ise bekle
                    st.session_state.exam_started = (exam_mode == "Online")
                    st.rerun()
                    
    # Sınav Ekranı
    else:
        exam = st.session_state.active_exam
        mode = exam.get('mode_preference', 'Online') # Default Online
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"📑 {exam['title']} ({mode} Modu)")
            
            # Kağıt Modu için Başlat Butonu
            if mode == "Kağıt (Çıktı)" and not st.session_state.get('exam_started', False) and not st.session_state.exam_submitted:
                st.info("Sınavı kağıda çözmek için önce çıktı alabilirsin. Süreyi başlatmak için butona bas.")
                if st.button("🚀 Süreyi Başlat", type="primary"):
                    st.session_state.exam_started = True
                    exam['start_time'] = time.time()
                    st.rerun()

        with col2:
            if not st.session_state.exam_submitted:
                # Süre Gösterimi
                # Online: Her zaman çalışır
                # Kağıt: Sadece başlatıldıysa çalışır
                
                is_timer_active = (mode == "Online") or st.session_state.get('exam_started', False)
                
                if is_timer_active:
                    if 'start_time' in exam and 'duration_min' in exam:
                        elapsed_sec = time.time() - exam['start_time']
                        total_sec = exam['duration_min'] * 60
                        remaining_sec = max(0, total_sec - elapsed_sec)
                        
                        mins = int(remaining_sec // 60)
                        secs = int(remaining_sec % 60)
                        
                        # Renkli Uyarı
                        color = "green"
                        if remaining_sec < 60: color = "red"
                        elif remaining_sec < 300: color = "orange"
                        
                        st.markdown(f"⏱️ **Kalan:** <span style='color:{color}; font-size:1.2em;'>{mins}:{secs:02d}</span>", unsafe_allow_html=True)
                        
                        # Süre bittiyse otomatik bitir
                        if remaining_sec <= 0:
                            st.warning("Süre doldu! Sınav otomatik sonlandırılıyor...")
                            st.session_state.exam_submitted = True
                            st.rerun()
                    else:
                        st.markdown("⏱️ **Süre:** Limitsiz")
                else:
                    st.markdown("⏱️ **Süre:** *Başlatılmadı*")
            
        st.progress(len(st.session_state.exam_answers) / len(exam['questions']))
        
        # Sidebar Kontrolleri
        with st.sidebar:
            st.markdown("### ⚙️ Sınav İşlemleri")
            
            # Yazdırma Butonu (Sadece Kağıt Modunda)
            if mode == "Kağıt (Çıktı)":
                import streamlit.components.v1 as components
                if st.button("🖨️ Çıktı Al (Yazdır)", type="primary", use_container_width=True):
                    js = "<script>window.parent.print()</script>"
                    components.html(js, height=0, width=0)
                st.info("💡 'Çıktı Al'a bastıktan sonra yazıcı ayarlarından 'Arka Plan Grafikleri'ni açmayı unutmayın.")
            
            st.markdown("---")
            
            # Sınavı Bitir (Sidebar)
            if not st.session_state.exam_submitted:
                if st.button("🏁 Sınavı Bitir", type="primary", use_container_width=True, key="finish_sidebar"):
                    st.session_state.exam_submitted = True
                    st.rerun()
            else:
                if st.button("🔄 Yeni Sınav", use_container_width=True, key="new_sidebar"):
                    st.session_state.active_exam = None
                    st.session_state.exam_answers = {}
                    st.session_state.exam_submitted = False
                    if 'exam_started' in st.session_state: del st.session_state.exam_started
                    st.rerun()
        
        # --- MODA GÖRE GÖSTERİM ---
        if mode == "Kağıt (Çıktı)":
            # Optik Form CSS ve YAZDIRMA CSS (GÜNCELLENDİ - V4)
            st.markdown("""
            <style>
            /* --- OPTİK FORM STİLLERİ --- */
            
            div[role="radiogroup"] {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                width: 100%;
            }
            
            div[role="radiogroup"] label {
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0 2px;
                cursor: pointer;
                position: relative;
            }

            div[role="radiogroup"] label > div:first-child {
                display: none !important;
            }
            
            div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
                width: 35px !important;
                height: 35px !important;
                border: 2px solid #E57373 !important;
                border-radius: 50% !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                transition: all 0.2s ease-in-out;
                background-color: white;
            }
            
            div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
                margin: 0 !important;
                padding: 0 !important;
                font-weight: bold !important;
                color: #E57373 !important;
                font-size: 16px !important;
            }
            
            /* --- SEÇİLİ DURUM (CHECKED) --- */
            /* Hem data-checked hem aria-checked desteği */
            div[role="radiogroup"] label[data-checked="true"] div[data-testid="stMarkdownContainer"],
            div[role="radiogroup"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] {
                background-color: #E57373 !important;
                border-color: #E57373 !important;
                box-shadow: 0 0 5px rgba(229, 115, 115, 0.5);
            }
            
            div[role="radiogroup"] label[data-checked="true"] div[data-testid="stMarkdownContainer"] p,
            div[role="radiogroup"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
                color: white !important;
            }
            
            div[role="radiogroup"] label:hover div[data-testid="stMarkdownContainer"] {
                border-color: #D32F2F !important;
                background-color: #FFEBEE;
            }

            /* --- YAZDIRMA (PRINT) STİLLERİ --- */
            @media print {
                /* 1. Genel Gizlemeler */
                [data-testid="stSidebar"], 
                header, 
                footer, 
                .stButton, 
                button, 
                .stApp > header,
                .stProgress,
                .no-print,
                [data-testid="stToolbar"] { /* Toolbar gizle */
                    display: none !important;
                }
                
                /* 2. Blok Düzeni */
                .block-container {
                    padding: 0 !important;
                    margin: 0 !important;
                    max-width: 100% !important;
                }
                
                /* 3. Kolon Yönetimi */
                /* Soru kolonunu (ilk kolon) tam genişlik yap */
                [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) {
                    width: 75% !important; /* Optik form için yer ayır? Hayır, optik ikinci sayfaya gidebilir */
                    flex: 1 !important;
                    max-width: 100% !important;
                }
                
                /* Optik form kolonunu GÖRÜNÜR YAP (Yan yana sığmıyorsa alta insin) */
                [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) {
                    display: block !important;
                    width: 100% !important;
                    page-break-before: always; /* Optik formu yeni sayfaya attır */
                }
                
                /* 4. Metin ve Renkler (ÖNEMLİ) */
                * {
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important; 
                }
                body {
                    font-size: 10pt; /* Biraz daha küçük font */
                    background-color: white;
                }
                
                /* Soru bloklarının bölünmesini engelle */
                p, div {
                    break-inside: avoid;
                }
                
                /* Optik form dairelerinin içini boşalt/doldur (yazıcı dostu) */
                div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
                     border: 2px solid #000 !important; /* Siyah kenarlık */
                     color: #000 !important;
                }
                
                div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
                     color: #000 !important;
                }
            }
            </style>
            """, unsafe_allow_html=True)

            # Yazdırma Butonu (Ana Ekrana Taşıdık)
            col_print, col_dummy = st.columns([1, 4])
            with col_print:
                import streamlit.components.v1 as components
                if st.button("🖨️ Yazdır", type="primary", use_container_width=True, key="print_main"):
                    # window.parent.print() iframe dışındaki ana sayfayı yazdırır.
                    js = "<script>window.parent.print()</script>"
                    components.html(js, height=0, width=0)
            
            st.markdown("---")

            # İki Kolon: Sol (Sorular), Sağ (Optik Form)
            q_col, optik_col = st.columns([2, 1])
            
            with q_col:
                st.markdown("### 📄 Soru Kitapçığı")
                for i, q in enumerate(exam['questions']):
                    st.markdown(f"**{i+1}.** {q['text']}")
                    # Görsel varsa göster
                    if q.get('figure_path'):
                        st.image(q['figure_path'], use_container_width=True)
                    # Seçenekleri sadece metin olarak göster (İşaretlenemez)
                    for opt, val in q['options'].items():
                        st.markdown(f"- **{opt})** {val}")
                    st.markdown("---")
            
            with optik_col:
                st.markdown("### 📝 Optik Form")
                st.info("Cevaplarını buraya kodla.")
                
                # Optik Form Container
                with st.container():
                    for i, q in enumerate(exam['questions']):
                        c_num, c_opt = st.columns([1, 5])
                        c_num.markdown(f"<div style='padding-top: 8px; font-weight: bold; color: #d63384; font-size: 1.1em;'>{i+1}</div>", unsafe_allow_html=True)
                        
                        # Optik Form (Radio Horizontal)
                        current_ans = st.session_state.exam_answers.get(q['question_id'])
                        
                        # Label visibility collapsed yaparsak metin gider, visible yapıp CSS ile gizleyelim mi?
                        # Hayır, CSS ile label içindeki p'yi stilize ediyoruz.
                        # Streamlit'te label_visibility="collapsed" olunca DOM'da label text render edilmiyor olabilir!
                        # Bu yüzden label_visibility="visible" yapıp ana label'ı ("Soru X") CSS ile gizlemeliyiz.
                        
                        selected = c_opt.radio(
                            f"Soru {i+1}", # Bu label CSS ile gizlenecek: div[data-testid="stRadio"] > label { display: none }
                            ["A", "B", "C", "D"],
                            key=f"optik_{i}",
                            horizontal=True,
                            label_visibility="visible", # ÖNEMLİ: Harflerin render edilmesi için visible olmalı
                            index=["A", "B", "C", "D"].index(current_ans) if current_ans else None,
                            disabled=st.session_state.exam_submitted
                        )
                        
                        if selected and not st.session_state.exam_submitted:
                            st.session_state.exam_answers[q['question_id']] = selected
                        
        else:
            # --- ONLINE MOD (Eski Görünüm) ---
            for i, q in enumerate(exam['questions']):
                st.markdown(f"#### Soru {i+1}")
                st.info(q['text'])
                
                # Görsel varsa göster
                if q.get('figure_path'):
                    st.image(q['figure_path'], use_container_width=True)
                
                # Cevap şıkları
                options = list(q['options'].keys())
                labels = [f"{opt}) {q['options'][opt]}" for opt in options]
                
                # Daha önce verilmiş cevap var mı?
                current_ans = st.session_state.exam_answers.get(q['question_id'])
                
                # Radio key unique olmalı
                selected_label = st.radio(
                    f"Cevabınız ({i})", 
                    labels, 
                    index=options.index(current_ans) if current_ans else None,
                    key=f"q_{i}",
                    disabled=st.session_state.exam_submitted,
                    label_visibility="collapsed"
                )
                
                if selected_label and not st.session_state.exam_submitted:
                    selected_opt = selected_label.split(")")[0]
                    st.session_state.exam_answers[q['question_id']] = selected_opt
                
                st.markdown("---")

        # --- SONUÇ GÖSTERİMİ (ORTAK) ---
        if st.session_state.exam_submitted:
             # Sonuçları göster (Moddan bağımsız)
             st.subheader("📊 Sonuçlar")
             
             # Başarı Bildirimi
             st.success("🎉 Sınav tamamlandı! Sonuçlarınız aşağıdadır.")
             
             for i, q in enumerate(exam['questions']):
                correct = q['correct']
                user_ans = st.session_state.exam_answers.get(q['question_id'])
                
                if user_ans == correct:
                    st.success(f"Soru {i+1}: ✅ Doğru! ({correct})")
                else:
                    st.error(f"Soru {i+1}: ❌ Yanlış. Senin cevabın: {user_ans}, Doğru cevap: {correct}")
                    
                    # Wrong-to-Learn Hook
                    from utils.content_engine import get_content_engine
                    ce = get_content_engine()
                    suggestion = ce.suggest_content_for_wrong_question(q['question_id'])
                    
                    if suggestion:
                        with st.expander("💡 Bu konuyu hemen öğrenmek ister misin?"):
                            st.markdown(f"**Konu:** {suggestion['topic']} - {suggestion['subtopic']}")
                            st.markdown(suggestion['content'].get('summary_bullets', ''))
                            st.info("Daha fazlası için 'Öğren' menüsüne git!")

        # Bitir Butonu
        if not st.session_state.exam_submitted:
            if st.button("Sınavı Bitir", type="primary", use_container_width=True):
                st.session_state.exam_submitted = True
                
                # Sonuçları kaydet
                results = engine.save_exam_result(exam, st.session_state.exam_answers)
                
                # Gamification
                gm.add_xp(results['correct'] * 10, f"Sınav tamamlandı! {results['correct']} doğru.")
                
                st.balloons()
                st.rerun()
                
        # Sonuç Ekranı Butonları
        else:
            if st.button("Yeni Sınav", type="primary"):
                st.session_state.active_exam = None
                st.session_state.exam_answers = {}
                st.session_state.exam_submitted = False
                if 'exam_started' in st.session_state: del st.session_state.exam_started
                st.rerun()

if __name__ == "__main__":
    show()
