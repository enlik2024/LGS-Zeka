"""
Öğren Sayfası
Konu anlatımı, Sokratik Tutör ve öğrenme fişleri (Modern Tab Yapısı).
"""

import streamlit as st
import sys
from pathlib import Path
import time

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.curriculum_engine import get_curriculum_engine
from utils.content_engine import get_content_engine
from utils.gamification import get_gamification_manager
from components.flashcard_viewer import show_flashcard_session

def show():
    gm = get_gamification_manager()
    
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0 2rem 0;'>
            <h1 style='color: #2E86AB; font-size: 2.5rem;'>📚 Öğren</h1>
            <p style='color: #8D99AE; font-size: 1.1rem; font-weight: 300;'>
                Eksiklerini kapat, netlerini artır.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    curriculum = get_curriculum_engine()
    content_engine = get_content_engine()
    
    # Context (Bağlam) Kontrolü
    ctx_lesson = st.session_state.get('learning_lesson')
    ctx_topic = st.session_state.get('learning_topic')
    ctx_subtopic = st.session_state.get('learning_subtopic')
    
    # 1. Seçim Alanı (Göz yormayan gri kutu içinde)
    with st.container():
        st.markdown("<div style='background-color: #F8F9FA; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lessons = ["Matematik", "Fen Bilimleri", "Türkçe"]
            lesson_idx = lessons.index(ctx_lesson) if ctx_lesson in lessons else 0
            lesson = st.selectbox("📘 Ders Seç", lessons, index=lesson_idx)
            
        with col2:
            topics = curriculum.get_topics_for_lesson(lesson)
            topic_idx = topics.index(ctx_topic) if ctx_topic in topics else 0
            topic = st.selectbox("📑 Konu Seç", topics, index=topic_idx) if topics else None
            
        with col3:
            subtopics = curriculum.get_subtopics_for_topic(lesson, topic) if topic else []
            subtopic_idx = subtopics.index(ctx_subtopic) if ctx_subtopic in subtopics else 0
            subtopic = st.selectbox("📌 Alt Konu Seç", subtopics, index=subtopic_idx) if subtopics else None
        st.markdown("</div>", unsafe_allow_html=True)
    
    if not subtopic:
        st.info("Lütfen çalışmak istediğin bir alt konu seç.")
        return
    
    # Konu görüntüleme XP'si ve Mastery Tracking
    from utils.mastery_manager import get_mastery_manager
    mastery = get_mastery_manager()
    
    view_key = f"viewed_{lesson}_{topic}_{subtopic}"
    if view_key not in st.session_state:
        st.session_state[view_key] = True
        gm.add_xp(5, f"📖 {subtopic} konusunu görüntüledin")
        mastery.update_mastery(lesson, topic, subtopic, "view")
        
    # 2. İçerik Getir
    packet = content_engine.build_learning_packet("current_user", lesson, topic, subtopic)
    
    if not packet:
        st.warning("Bu konuda henüz içerik bulunamadı. Ancak Sokratik Tutör ile çalışabilirsin.")
    
    content = packet['content'] if packet else {}
    
    # Context Hazırlığı (Sokratik Tutör ve Mermaid için)
    learning_context = ""
    if content:
        c_summary = content.get('summary_bullets', '')
        c_strategy = content.get('strategy_steps', '')
        c_mistakes = content.get('common_mistakes', '')
        learning_context = f"ÖZET BİLGİ:\n{c_summary}\n\nÇÖZÜM STRATEJİSİ:\n{c_strategy}\n\nSIK YAPILAN HATALAR:\n{c_mistakes}"
    
    # 3. Sekmeli Yapı (Tabs) - Radio Button ile (State Korumalı)
    # Bu yöntem, sayfa yenilendiğinde (rerun) kullanıcının kaldığı sekmede kalmasını sağlar.
    
    # CSS ile radio butonlarını tab gibi göster
    st.markdown("""
    <style>
    div[role="radiogroup"] > label > div:first-of-type {
        display: none;
    }
    div[role="radiogroup"] {
        background-color: #f0f2f6;
        padding: 5px;
        border-radius: 10px;
        justify-content: center;
    }
    div[role="radiogroup"] label {
        background-color: transparent;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        margin: 0 5px;
        transition: all 0.3s;
        text-align: center;
    }
    div[role="radiogroup"] label:hover {
        background-color: #e0e2e6;
    }
    div[role="radiogroup"] label[aria-checked="true"] {
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-weight: bold;
        color: #2E86AB;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Varsayılan sekme yönetimi
    active_tab_key = f"active_tab_{lesson}_{topic}_{subtopic}"
    if active_tab_key not in st.session_state:
        st.session_state[active_tab_key] = "📖 Konu Çalış"
    
    # Radio Button
    tabs = ["📖 Konu Çalış", "🎓 Sokratik Tutör", "🃏 Bilgi Kartları"]
    
    # Tab Güvenlik Kontrolü (Eğer eski state'de 'Kavram Haritası' kaldıysa resetle)
    if st.session_state[active_tab_key] not in tabs:
        st.session_state[active_tab_key] = "📖 Konu Çalış"

    selected_tab = st.radio(
        "Mod Seçiniz",
        tabs,
        horizontal=True,
        label_visibility="collapsed",
        key=f"tab_select_{lesson}_{topic}_{subtopic}",
        index=tabs.index(st.session_state[active_tab_key])
    )
    
    # State'i güncelle
    st.session_state[active_tab_key] = selected_tab
    
    # --- TAB 1: KONU ÇALIŞ ---
    if selected_tab == "📖 Konu Çalış":
        if content:
            st.markdown(f"### 📌 {subtopic}")
            
            # Metin Formatlama (HTML içinde <br> kullan)
            def _fmt(text):
                if not text: return ""
                # Literal \n ve gerçek newline karakterlerini <br> yap
                return text.replace('\\n', '<br>').replace('\n', '<br>')

            # Card Tasarımlı İçerikler
            # Özet Bilgi
            with st.container():
                st.markdown(f"""
                <div class='card'>
                    <h3 style='color: #2E86AB; display: flex; align-items: center; gap: 0.5rem;'>
                        📝 Özet Bilgi
                    </h3>
                    <div style='color: #4A4E69; line-height: 1.6;'>
                        {_fmt(content.get('summary_bullets', ''))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                # Çözüm Stratejisi
                st.markdown(f"""
                <div class='card' style='background-color: #E3F2EF; border-left: 5px solid #70C1B3;'>
                    <h3 style='color: #2D6A4F; font-size: 1.1rem;'>🧠 Çözüm Stratejisi</h3>
                    <div style='color: #1B4332; font-size: 0.95rem;'>
                        {_fmt(content.get('strategy_steps', ''))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                # Sık Hatalar
                st.markdown(f"""
                <div class='card' style='background-color: #FFF9E6; border-left: 5px solid #FFE066;'>
                    <h3 style='color: #856404; font-size: 1.1rem;'>⚠️ Dikkat Et</h3>
                    <div style='color: #533F03; font-size: 0.95rem;'>
                        {_fmt(content.get('common_mistakes', ''))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # NotebookLM İçerikleri (Video, Infografik vs.)
            if content.get('source') == 'notebooklm':
                st.markdown("---")
                st.markdown("### 🎬 NotebookLM İçerikleri")
                st.caption("Aşağıdaki içeriklere tıklayarak açabilirsin.")
                
                # Tüm içerikleri getir
                try:
                    from utils.db_manager import get_db_manager
                    import json as json_lib
                    db = get_db_manager()
                    
                    if db.db_type == "supabase" and db._client:
                        # Kazanım ID'sini bul
                        kaz_result = db._client.table('meb_kazanimlar').select('kazanim_id').eq('ders', lesson).eq('curriculum_map_subtopic', subtopic).limit(1).execute()
                        
                        if kaz_result.data:
                            kazanim_id = kaz_result.data[0]['kazanim_id']
                            # Tüm içerikleri getir
                            icerik_result = db._client.table('icerikler').select('*').eq('kazanim_id', kazanim_id).eq('status', 'approved').execute()
                            
                            if icerik_result.data:
                                for icerik in icerik_result.data:
                                    tip = icerik.get('icerik_tipi', 'guide')
                                    baslik = icerik.get('baslik', 'İçerik')
                                    
                                    # İçerik tipine göre ikon
                                    tip_ikonlar = {
                                        'video': '🎬', 'guide': '📝', 'quiz': '❓',
                                        'flashcard': '🃏', 'infographic': '📊', 'audio': '🎧'
                                    }
                                    ikon = tip_ikonlar.get(tip, '📄')
                                    
                                    # ========== VIDEO ==========
                                    if tip == 'video':
                                        with st.expander(f"{ikon} Video: {baslik}", expanded=False):
                                            video_url = icerik.get('video_url')
                                            if video_url:
                                                st.video(video_url)
                                            else:
                                                st.warning("Video bağlantısı bulunamadı.")
                                            
                                            notebook_url = icerik.get('notebook_url')
                                            if notebook_url:
                                                st.link_button("📄 NotebookLM Kaynağına Git", notebook_url)
                                    
                                    # ========== QUIZ ==========
                                    elif tip == 'quiz':
                                        with st.expander(f"{ikon} Quiz: {baslik}", expanded=False):
                                            quiz_json = icerik.get('icerik_json')
                                            if quiz_json:
                                                try:
                                                    quiz_data = json_lib.loads(quiz_json) if isinstance(quiz_json, str) else quiz_json
                                                    questions = quiz_data.get('questions', [])
                                                    
                                                    if questions:
                                                        st.markdown(f"**Toplam {len(questions)} soru**")
                                                        
                                                        for q in questions:
                                                            st.markdown(f"**Soru {q['id']}:** {q['question']}")
                                                            options = q.get('options', {})
                                                            
                                                            selected = st.radio(
                                                                "Cevabınız:", 
                                                                options=[f"{k}) {v}" for k, v in options.items()],
                                                                key=f"quiz_{icerik.get('icerik_id')}_{q['id']}",
                                                                label_visibility="collapsed"
                                                            )
                                                            
                                                            if st.button(f"Cevabı Kontrol Et", key=f"check_{icerik.get('icerik_id')}_{q['id']}"):
                                                                correct = q.get('correct_answer', '')
                                                                if selected and selected.startswith(correct):
                                                                    st.success(f"✅ Doğru! {q.get('explanation', '')}")
                                                                else:
                                                                    st.error(f"❌ Yanlış. Doğru cevap: {correct}. {q.get('explanation', '')}")
                                                            st.markdown("---")
                                                    else:
                                                        st.info("Quiz soruları bulunamadı.")
                                                except Exception as qe:
                                                    st.warning(f"Quiz parse hatası: {qe}")
                                            else:
                                                st.info("Quiz verileri henüz yüklenmedi.")
                                    
                                    # ========== FLASHCARD ==========
                                    elif tip == 'flashcard':
                                        with st.expander(f"{ikon} Flashcard: {baslik}", expanded=False):
                                            st.markdown("Bilgi kartlarını çalışmak için **Bilgi Kartları** sekmesine git.")
                                            if st.button("🃏 Kartlara Git", key=f"goto_flash_{icerik.get('icerik_id')}"):
                                                st.session_state[f"active_tab_{lesson}_{topic}_{subtopic}"] = "🃏 Bilgi Kartları"
                                                st.rerun()
                                    
                                    # ========== INFOGRAPHIC ==========
                                    elif tip == 'infographic':
                                        with st.expander(f"{ikon} İnfografik: {baslik}", expanded=False):
                                            image_path = icerik.get('image_path')
                                            if image_path:
                                                try:
                                                    st.image(image_path, caption=baslik, use_container_width=True)
                                                except Exception as ie:
                                                    st.warning(f"Görsel yüklenemedi: {ie}")
                                            else:
                                                st.info("İnfografik görseli henüz yüklenmedi.")
                                    
                                    # ========== GUIDE / OTHER ==========
                                    else:
                                        with st.expander(f"{ikon} Rehber: {baslik}", expanded=False):
                                            guide_json = icerik.get('icerik_json')
                                            if guide_json:
                                                try:
                                                    guide_data = json_lib.loads(guide_json) if isinstance(guide_json, str) else guide_json
                                                    st.markdown(guide_data.get('content', 'İçerik bulunamadı.'))
                                                except:
                                                    st.markdown(str(guide_json))
                                            else:
                                                notebook_url = icerik.get('notebook_url')
                                                if notebook_url:
                                                    st.markdown(f"[NotebookLM'de Aç]({notebook_url})")
                                                else:
                                                    st.info("Rehber içeriği henüz yüklenmedi.")
                except Exception as e:
                    print(f"NotebookLM content error: {e}")
            
            # Mini Check (Sadece varsa göster)
            check_q = content.get('mini_check_question')
            check_a = content.get('mini_check_answer')
            
            if check_q:
                st.markdown("### ⚡ Hızlı Kontrol")
                with st.container(border=True):
                    st.write(f"**Soru:** {check_q}")
                    if st.button("Cevabı Göster", key="mini_check_btn"):
                        st.success(f"**Cevap:** {check_a}")
                        # Mini test XP
                        test_key = f"minitest_{lesson}_{topic}_{subtopic}"
                        if test_key not in st.session_state:
                            st.session_state[test_key] = True
                            gm.add_xp(10, "✅ Mini test tamamlandı")
        else:
            st.info("İçerik yüklenemedi.")

    # --- TAB 2: SOKRATİK TUTÖR ---
    elif selected_tab == "🎓 Sokratik Tutör":
        # Sokratik Tutör key'in değişmemesi için state koruyoruz
        _render_socratic_section(lesson, topic, subtopic, gm, learning_context)

    # --- TAB 3: FLASHCARDS ---
    elif selected_tab == "🃏 Bilgi Kartları":
        _render_flashcard_section(lesson, topic, subtopic, content, gm)


def _render_socratic_section(lesson, topic, subtopic, gm, learning_context=""):
    """Sokratik Tutör bölümünü render eder."""
    
    # Auto-scroll için anchor
    st.markdown("<div id='socratic-anchor'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2E86AB 0%, #70C1B3 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;'>
        <h3 style='color: white; margin-top: 0;'>🎓 Sokratik Tutör</h3>
        <p style='margin: 0; opacity: 0.9;'>
            Ezberleme, keşfet! Seninle sohbet ederek konuyu derinlemesine anlamana yardımcı olacağım.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tutor_key = f"tutor_active_{lesson}_{topic}_{subtopic}"
    
    if not st.session_state.get(tutor_key, False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Sohbeti Başlat", type="primary", use_container_width=True):
                st.session_state[tutor_key] = True
                st.rerun()
    else:
        try:
            from components.socratic_chat import render_socratic_inline
            
            context = {
                "lesson": lesson,
                "topic": topic,
                "subtopic": subtopic,
                "student_level": "orta"
            }
            
            # Learning Context parametresini gönder
            completed = render_socratic_inline(context, state_key=f"socratic_{lesson}_{topic}_{subtopic}", learning_context=learning_context)
            
            if completed:
                seans_key = f"seans_{lesson}_{topic}_{subtopic}"
                if seans_key not in st.session_state:
                    st.session_state[seans_key] = True
                    gm.add_xp(25, f"🎓 {subtopic} Sokratik seansı tamamlandı!")
                    from utils.mastery_manager import get_mastery_manager
                    get_mastery_manager().update_mastery(lesson, topic, subtopic, "socratic", True)
                    st.balloons()
            
            # Auto-scroll script
            st.components.v1.html("""
                <script>
                    window.parent.document.getElementById('socratic-anchor').scrollIntoView({behavior: 'smooth'});
                </script>
            """, height=0)
                    
        except ImportError:
            st.warning("Sokratik tutör bileşeni hata verdi.")


def _render_flashcard_section(lesson, topic, subtopic, content, gm):
    """Flashcard bölümünü render eder."""
    
    st.markdown(f"### 🃏 {subtopic} - Bilgi Kartları")
    
    # Context
    learning_context = ""
    if content:
        c_summary = content.get('summary_bullets', '')
        c_strategy = content.get('strategy_steps', '')
        learning_context = f"ÖZET:\n{c_summary}\n\nSTRATEJİ:\n{c_strategy}"
    
    if not learning_context:
        st.info("İçerik bulunamadığı için kart oluşturulamadı.")
        return

    # Cache key
    flash_key = f"flashcards_gen_{lesson}_{topic}_{subtopic}"
    
    # 1. Önce Hibrit DB Kontrolü (Bulut + Yerel)
    if flash_key not in st.session_state:
        try:
            from utils.content_engine import get_content_engine
            ce = get_content_engine()
            # load_flashcards hem Supabase hem Local bakar
            saved_cards = ce.load_flashcards(lesson, topic, subtopic)
            if saved_cards:
                st.session_state[flash_key] = saved_cards
                # st.toast("Kartlar veritabanından yüklendi.") 
        except Exception as e:
            print(f"DB Load Error: {e}")

    # 2. Hala yoksa Üret (Generate) ve Kaydet
    if flash_key not in st.session_state:
        with st.spinner("🃏 Yapay Zeka, konu özetinden size özel sorular hazırlıyor..."):
            try:
                from utils.llm_adapter import get_llm_adapter
                llm = get_llm_adapter()
                cards = llm.generate_flashcards(lesson, topic, subtopic, learning_context)
                
                if cards:
                    st.session_state[flash_key] = cards
                    
                    # Veritabanına Kaydet (Hibrit)
                    try:
                        from utils.content_engine import get_content_engine
                        ce = get_content_engine()
                        # save_flashcards hem Supabase hem Local yazar
                        ce.save_flashcards(lesson, topic, subtopic, cards)
                    except Exception as db_err:
                        print(f"DB Save Error: {db_err}")
                        
                else:
                    st.warning("Kart üretilemedi.")
            except Exception as e:
                st.error(f"Hata: {e}")
    
    # Gösterim
    if flash_key in st.session_state and st.session_state[flash_key]:
        from components.flashcard_viewer import show_flashcard_session
        show_flashcard_session(st.session_state[flash_key], topic=subtopic)
        
        st.caption("💡 Kartlar bulut veritabanında saklanmaktadır.")
        if st.button("🔄 Yeni Sorular Getir (Mevcutları Siler)", key="regen_flash"):
            del st.session_state[flash_key]
            # Veritabanından da silmek gerekir mi? Şimdilik sadece session'dan silersek, tekrar üretince üzerine yazarız.
            st.rerun()
    else:
        st.info("Kartlar yüklenemedi.")


if __name__ == "__main__":
    show()

