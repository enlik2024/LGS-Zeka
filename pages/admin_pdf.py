"""
Admin PDF -> Fiş Üretim Sayfası
"""

import streamlit as st
import pandas as pd
from utils.db_manager import get_db_manager
from utils.content_ingest_engine import get_content_ingest_engine
from utils.llm_adapter import get_llm_adapter

def show():
    st.header("📄 PDF'den İçerik Fişi Üret (Fast-Track)")
    
    db = get_db_manager()
    ingest = get_content_ingest_engine()
    llm = get_llm_adapter()
    
    # 1. Müfredat Seçimi ve Ekleme
    with st.expander("➕ Yeni Konu/Alt Konu Ekle", expanded=False):
        # Mevcut müfredatı yükle
        curriculum_df = db.load_curriculum_map()
        existing_lessons = curriculum_df['lesson'].unique().tolist() if not curriculum_df.empty else []
        
        c1, c2, c3 = st.columns(3)
        
        # Ders Seçimi
        lesson_options = ["➕ Yeni Ders Ekle"] + existing_lessons
        selected_new_lesson = c1.selectbox("Ders Seç/Ekle", lesson_options)
        
        if selected_new_lesson == "➕ Yeni Ders Ekle":
            new_lesson = c1.text_input("Yeni Ders Adı", key="new_lesson_input")
        else:
            new_lesson = selected_new_lesson
            
        # Konu Seçimi
        topic_options = ["➕ Yeni Konu Ekle"]
        if new_lesson and new_lesson != "➕ Yeni Ders Ekle":
            existing_topics = curriculum_df[curriculum_df['lesson'] == new_lesson]['topic'].unique().tolist()
            topic_options += existing_topics
            
        selected_new_topic = c2.selectbox("Konu Seç/Ekle", topic_options)
        
        if selected_new_topic == "➕ Yeni Konu Ekle":
            new_topic = c2.text_input("Yeni Konu Adı", key="new_topic_input")
        else:
            new_topic = selected_new_topic
            
        # Alt Konu (Genelde hep yeni olur ama yine de listeyelim)
        subtopic_options = ["➕ Yeni Alt Konu Ekle"]
        if new_lesson and new_topic and new_lesson != "➕ Yeni Ders Ekle" and new_topic != "➕ Yeni Konu Ekle":
             existing_subtopics = curriculum_df[
                (curriculum_df['lesson'] == new_lesson) & 
                (curriculum_df['topic'] == new_topic)
            ]['subtopic'].unique().tolist()
             subtopic_options += existing_subtopics
             
        selected_new_subtopic = c3.selectbox("Alt Konu Seç/Ekle", subtopic_options)
        
        if selected_new_subtopic == "➕ Yeni Alt Konu Ekle":
            new_subtopic = c3.text_input("Yeni Alt Konu Adı", key="new_subtopic_input")
        else:
            new_subtopic = selected_new_subtopic
        
        if st.button("Müfredata Ekle"):
            if new_lesson and new_topic and new_subtopic:
                if db.add_curriculum_item(new_lesson, new_topic, new_subtopic):
                    st.success(f"✅ {new_lesson} > {new_topic} > {new_subtopic} eklendi!")
                    st.rerun()
                else:
                    st.warning("Bu kayıt zaten var veya eklenemedi.")
            else:
                st.error("Lütfen tüm alanları doldurun.")

    curriculum_df = db.load_curriculum_map()
    if curriculum_df.empty:
        st.warning("Curriculum Map boş! Önce veri yükleyin veya yukarıdan ekleyin.")
        # return # Return etmeyelim, belki ekleme yapacak
        
    lessons = curriculum_df['lesson'].unique() if not curriculum_df.empty else []
    selected_lesson = st.selectbox("Ders", lessons)
    
    topics = []
    if selected_lesson:
        topics = curriculum_df[curriculum_df['lesson'] == selected_lesson]['topic'].unique()
    selected_topic = st.selectbox("Konu", topics)
    
    subtopics = []
    if selected_lesson and selected_topic:
        subtopics = curriculum_df[
            (curriculum_df['lesson'] == selected_lesson) & 
            (curriculum_df['topic'] == selected_topic)
        ]['subtopic'].unique()
    selected_subtopic = st.selectbox("Alt Konu", subtopics)
    
    # --- MOD SEÇİMİ ---
    st.markdown("### İşlem Modu")
    mode = st.radio("Ne Üretmek İstiyorsun?", ["Konu Fişi (Content)", "Soru Bankası (Question)"], index=0)
    
    # Yayınevi Seçimi (Manuel Giriş)
    publisher = st.text_input("Yayınevi / Kaynak Adı", value="Uploaded PDF", help="Örn: Hız Yayınları, MEB, Çanta Yayınları")
    
    # Kaynak Tipi
    source_type = st.radio(
        "İçerik Tipi", 
        ["publisher_original", "ai_variant_of_publisher", "ai_generated"], 
        index=0, 
        format_func=lambda x: {
            "publisher_original": "Publisher (Orijinal - Değiştirmeden Al)",
            "ai_variant_of_publisher": "AI Variant (Yayınevi Varyantı)",
            "ai_generated": "AI Generated (Sıfırdan Üret)"
        }[x],
        help="Publisher: Birebir al. AI Variant: Benzerini üret. AI Generated: Sıfırdan üret."
    )

    # 2. Dosya Yükleme (PDF veya Görsel)
    uploaded_file = st.file_uploader("İçerik Yükle (PDF veya Resim)", type=["pdf", "png", "jpg", "jpeg", "webp"])
    
    # Dosya tipine göre arayüz
    is_pdf = uploaded_file is not None and uploaded_file.type == "application/pdf"
    
    if is_pdf:
        page_range = st.text_input("Sayfa Aralığı (Örn: 12-15)", "1-1")
    else:
        # Resimse sayfa aralığına gerek yok
        page_range = None
    
    if uploaded_file and st.button("🚀 Analiz Et ve Üret"):
        with st.spinner("AI İçeriği Analiz Ediyor..."):
            images = []
            
            if is_pdf:
                # A) PDF ise Sayfaları resme çevir
                pages = ingest.parse_page_range(page_range)
                if not pages:
                    return
                    
                images = ingest.pdf_pages_to_images(uploaded_file.read(), pages)
                st.info(f"{len(images)} sayfa işlendi. Gemini'ye gönderiliyor...")
            else:
                # B) Resim ise direkt kullan
                images = [uploaded_file.read()]
                st.info("Görsel işlendi. Gemini'ye gönderiliyor...")
                
            if not images:
                st.error("Görsel verisi oluşturulamadı.")
                return
            
            # B) LLM'e Gönder (Moda Göre)
            if "Konu Fişi" in mode:
                # --- KONU FİŞİ MODU ---
                result = llm.generate_content_fiches_from_images(
                    images, 
                    selected_lesson, 
                    selected_topic, 
                    selected_subtopic,
                    publisher=publisher,
                    source_type=source_type
                )
                
                # C) DB'ye Yaz (Draft)
                meta = {
                    "lesson": selected_lesson, 
                    "topic": selected_topic, 
                    "subtopic": selected_subtopic,
                    "publisher": publisher,
                    "source_type": source_type,
                    "derivation_ref": "PDF Upload"
                }
                rows = ingest.build_fiche_rows_from_llm_output(result, meta)
                
                if rows:
                    if db.append_content_rows(rows):
                        st.success(f"{len(rows)} adet fiş taslağı oluşturuldu! 'Taslak Fişler' bölümünden inceleyip onaylayın.")
                    else:
                        st.error("Veritabanına kayıt başarısız.")
                else:
                    st.warning("Fiş üretilemedi veya format hatası.")
                    
            else:
                # --- SORU BANKASI MODU ---
                result = llm.generate_questions_from_images(
                    images,
                    selected_lesson,
                    selected_topic,
                    selected_subtopic,
                    publisher=publisher,
                    source_type=source_type
                )
                
                questions = result.get("questions", [])
                if questions:
                    # AI ile Şekil Analizi (Phase I)
                    progress_bar = st.progress(0)
                    for idx, q in enumerate(questions):
                        # 1. Heuristik Kontrol
                        keywords = ["grafik", "tablo", "şekil", "görsel", "yukarıdaki", "yandaki", "aşağıdaki"]
                        text_lower = q.get("text", "").lower()
                        heuristic_match = any(k in text_lower for k in keywords)
                        
                        # 2. AI Sınıflandırma
                        ai_result = llm.classify_has_figure(
                            q.get("text", ""), 
                            q.get("options", {}), 
                            images[0] if images else None
                        )
                        
                        # Sonuçları soru objesine ekle
                        q["has_figure_ai"] = ai_result.get("has_figure", False) or heuristic_match
                        q["figure_type_ai"] = ai_result.get("figure_type", "none")
                        q["figure_confidence"] = ai_result.get("confidence", 0.0)
                        q["ai_reason"] = ai_result.get("reason", "")
                        
                        progress_bar.progress((idx + 1) / len(questions))
                    
                    progress_bar.empty()
                    
                    # Session State'e at (Review için)
                    st.session_state.extracted_questions = questions
                    # Görseli de sakla (ilk görseli referans alıyoruz şimdilik)
                    if images:
                        st.session_state.current_source_image = images[0]
                    
                    st.success(f"✅ {len(questions)} adet soru ayrıştırıldı ve analiz edildi! Aşağıdan inceleyip kaydedin.")
                else:
                    st.warning("⚠️ Soru bulunamadı veya ayrıştırılamadı.")

    # --- SORU İNCELEME VE KAYIT (DRAFT) ---
    if "extracted_questions" in st.session_state and st.session_state.extracted_questions:
        st.markdown("---")
        st.subheader("📋 Soru İnceleme ve Kayıt")
        
        # Form ile sarmalayalım
        with st.form("question_review_form"):
            updated_questions = []
            
            for i, q in enumerate(st.session_state.extracted_questions):
                st.markdown(f"#### Soru {i+1}")
                col_text, col_meta = st.columns([3, 1])
                
                with col_text:
                    # Metin düzenleme imkanı
                    new_text = st.text_area("Soru Metni", value=q.get('text', ''), height=100, key=f"q_text_{i}")
                    q['text'] = new_text
                    st.json(q.get('options', {}))
                    
                with col_meta:
                    st.write(f"**Cevap:** {q.get('correct_answer')}")
                    st.write(f"**Zorluk:** {q.get('difficulty')}")
                    
                    # Şekil İşaretleme (AI Önerili)
                    ai_suggestion = q.get("has_figure_ai", False)
                    confidence = q.get("figure_confidence", 0.0)
                    
                    if ai_suggestion:
                        st.caption(f"🤖 AI Önerisi: **Şekilli** (%{int(confidence*100)})")
                    else:
                        st.caption(f"🤖 AI Önerisi: Şekilsiz (%{int(confidence*100)})")
                        
                    has_figure = st.checkbox("Şekilli Soru?", value=ai_suggestion, key=f"has_fig_{i}")
                    q['has_figure_final'] = has_figure # Final karar
                    
                    if has_figure:
                        fig_type = st.selectbox(
                            "Şekil Tipi", 
                            ["chart", "geometry", "schematic", "table_graph_combo", "decorative"],
                            key=f"fig_type_{i}"
                        )
                        q['figure_type'] = fig_type
                        q['figure_policy'] = "no_variant" # Pilot kuralı: Şekilli ise varyant yok
                    else:
                        q['figure_type'] = "none"
                        q['figure_policy'] = "no_variant" # Default
                
                st.markdown("---")
                updated_questions.append(q)
            
            # Kaydet Butonu
            if st.form_submit_button("💾 Seçilenleri Veritabanına Kaydet"):
                count = 0
                import json
                from datetime import datetime
                import os
                
                # Resim Kayıt Klasörü
                figures_dir = "assets/figures"
                os.makedirs(figures_dir, exist_ok=True)
                
                for q in updated_questions:
                    # Boş soruları atla
                    if not q.get('text') or not q.get('text').strip():
                        continue
                        
                    # Görsel Kaydı (Eğer şekilli ise)
                    fig_path = ""
                    if q.get('has_figure') and "current_source_image" in st.session_state:
                        # Tüm sayfayı kaydet (MVP)
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        img_filename = f"fig_{timestamp}_{count}.png"
                        full_path = os.path.join(figures_dir, img_filename)
                        
                        try:
                            with open(full_path, "wb") as f:
                                f.write(st.session_state.current_source_image)
                            fig_path = full_path
                        except Exception as e:
                            st.error(f"Görsel kayıt hatası: {e}")

                    q_data = {
                        "question_id": f"q_{datetime.now().strftime('%Y%m%d%H%M%S')}_{count}",
                        "lesson": selected_lesson,
                        "topic": selected_topic,
                        "subtopic": selected_subtopic,
                        "difficulty_label": q.get("difficulty", 3),
                        "question_origin": "publisher" if source_type == "publisher_original" else ("meb" if "MEB" in publisher.upper() else source_type),
                        "origin_detail": publisher,
                        "text": q.get("text", ""),
                        "options_json": json.dumps(q.get("options", {}), ensure_ascii=False),
                        "correct_answer": q.get("correct_answer", ""),
                        "active": True,
                        "created_at": datetime.now().isoformat(),
                        # Yeni Alanlar
                        # Yeni Alanlar (AI + Final)
                        "has_figure": q.get('has_figure_final', False), # Backward compatibility
                        "has_figure_final": q.get('has_figure_final', False),
                        "has_figure_ai": q.get('has_figure_ai', False),
                        "figure_type_ai": q.get('figure_type_ai', 'none'),
                        "figure_confidence": q.get('figure_confidence', 0.0),
                        
                        "figure_type": q.get('figure_type', 'none'),
                        "figure_policy": q.get('figure_policy', 'no_variant'),
                        "figure_path": fig_path
                    }
                    db.add_data("questions", q_data)
                    count += 1
                
                st.success(f"✅ {count} soru başarıyla kaydedildi!")
                # Temizle
                del st.session_state.extracted_questions
                if "current_source_image" in st.session_state:
                    del st.session_state.current_source_image
                st.rerun()
                
    st.markdown("---")
    
    # 3. Taslak Onaylama
    st.subheader("📝 Taslak Fişler (Onay Bekleyen)")
    content_df = db.load_content()
    
    if not content_df.empty:
        drafts = content_df[
            (content_df['status'] == 'draft') &
            (content_df['subtopic'] == selected_subtopic)
        ]
        
        if drafts.empty:
            st.info("Bu alt konuda onay bekleyen taslak yok.")
        else:
            for idx, row in drafts.iterrows():
                with st.expander(f"Fiş: {row.get('content_type')} - {row.get('content_id')}"):
                    st.json(row.to_dict())
                    col1, col2 = st.columns(2)
                    if col1.button("✅ Onayla", key=f"app_{idx}"):
                        db.update_content_status(row['content_id'], "approved", {"active": True})
                        st.rerun()
                    if col2.button("❌ Reddet", key=f"rej_{idx}"):
                        db.update_content_status(row['content_id'], "rejected", {"active": False})
                        st.rerun()

if __name__ == "__main__":
    show()
