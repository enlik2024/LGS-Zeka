"""
Soru Analizi Sayfası - UX Revizyonu
AI destekli soru görseli analizi, sekmeli arayüz, gamification
"""

import streamlit as st
from PIL import Image
import io
from datetime import datetime
from typing import Optional, Dict, Any
import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Yeni modüller
from utils.gemini_helper import get_gemini_helper, get_difficulty_badge
from utils.gamification import get_gamification_manager
from components.mermaid_renderer import render_mermaid, create_solution_flowchart
from components.socratic_chat import show_socratic_chat
from components.error_tagger import show_error_tagger
from utils.db_manager import get_db_manager
from utils.event_logger import get_event_logger


def show():
    """Soru Analizi sayfasını gösterir (UX Revizyonu)."""
    
    # Gamification manager
    gm = get_gamification_manager()
    gm.update_streak()
    
    # DB Manager (Always init)
    db = get_db_manager()
    
    # Sayfa başlığı
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #FF6B6B;'>🔍 Soru Analizi</h1>
            <p style='color: #6C757D; font-size: 1.1rem;'>
                AI ile soru görselini analiz edin, çözüm adımlarını öğrenin
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Session state başlatma - Supabase'den geçmişi yükle
    if 'analysis_history' not in st.session_state:
        db = get_db_manager()
        history_df = db.load_analysis_history()
        if not history_df.empty:
            # Supabase alan isimlerini UI'ın beklediği Türkçe isimlere map et
            import ast
            records = history_df.to_dict('records')
            mapped_records = []
            for r in records:
                # solution_steps string olarak geliyorsa listeye çevir
                solution_steps = r.get('solution_steps', '')
                if isinstance(solution_steps, str) and solution_steps.startswith('['):
                    try:
                        solution_steps = ast.literal_eval(solution_steps)
                    except:
                        pass  # Parse edilemezse string olarak bırak
                
                mapped_records.append({
                    'konu': r.get('topic', 'Bilinmiyor'),
                    'alt_konu': r.get('subtopic', ''),
                    'zorluk_seviyesi': int(r.get('difficulty_level', 3)) if r.get('difficulty_level') else 3,
                    'timestamp': r.get('created_at', ''),
                    'soru_metni': r.get('question_text', ''),
                    'cozum_adimlari': solution_steps,
                    'dogru_cevap': r.get('final_answer', ''),
                })
            st.session_state.analysis_history = mapped_records
        else:
            st.session_state.analysis_history = []
    
    # Sidebar - Ayarlar
    with st.sidebar:
        st.markdown("### ⚙️ Analiz Ayarları")
        
        model_type = st.radio(
            "AI Model",
            options=["flash", "pro"],
            format_func=lambda x: "⚡ Flash (Hızlı)" if x == "flash" else "🎯 Pro (Yüksek Kalite)",
            help="Flash: Hızlı ve ekonomik\nPro: Daha detaylı analiz"
        )
        
        save_to_db = st.checkbox(
            "Analizi kaydet",
            value=True,
            help="Analiz sonuçlarını veritabanına kaydet"
        )
        
        # Beta Modu Toggle
        from utils.config_manager import get_config
        config = get_config()
        beta_enabled = config.is_feature_enabled("beta_mode_enabled", False)
        
        if beta_enabled:
            beta_mode = st.toggle(
                "🧪 Beta Modu (DeepTutor)",
                value=False,
                help="Adım adım çözüm + Perplexity doğrulaması"
            )
            st.session_state.beta_mode = beta_mode
        else:
            beta_mode = False
            st.session_state.beta_mode = False
        
        st.markdown("---")
        
        # İstatistikler
        st.markdown("### 📊 İstatistikler")
        st.metric("Bu Oturumda Analiz", len(st.session_state.analysis_history))
        
        if st.session_state.analysis_history:
            avg_difficulty = sum(
                h.get('zorluk_seviyesi', 0) 
                for h in st.session_state.analysis_history
            ) / len(st.session_state.analysis_history)
            st.metric("Ortalama Zorluk", f"{avg_difficulty:.1f}/5")
    
    # Ana içerik - Asimetrik sütunlar (30% - 70%)
    col1, col2 = st.columns([3, 7])
    
    with col1:
        # Sticky container için CSS
        st.markdown("""
        <style>
        [data-testid="column"]:first-child {
            position: sticky;
            top: 3rem;
            height: fit-content;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📤 Soru Yükle")
        
        # Görsel yükleme seçenekleri - Kompakt
        upload_method = st.radio(
            "Yöntem",
            options=["📁 Dosya", "📷 Kamera"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        uploaded_image = None
        
        if upload_method == "📁 Dosya":
            uploaded_file = st.file_uploader(
                "Görsel seç",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed"
            )
            
            if uploaded_file:
                uploaded_image = Image.open(uploaded_file)
        
        else:  # Kamera
            camera_image = st.camera_input("Fotoğraf çek", label_visibility="collapsed")
            
            if camera_image:
                uploaded_image = Image.open(camera_image)
        
        # Çoklu Soru Seçimi (K4)
        has_multiple_questions = st.checkbox("Bu görselde birden fazla soru var", 
                                           help="Eğer sayfada birden çok soru varsa, bunları sırayla analiz etmek için işaretleyin.")
        
        # Görsel önizleme - Kompakt
        if uploaded_image:
            st.image(
                uploaded_image,
                use_container_width=True
            )
            
            # Görsel bilgileri - Küçük
            st.caption(f"📐 {uploaded_image.size[0]}×{uploaded_image.size[1]} px")
            
            # K3: Yeni yükleme kontrolü (Image Hash)
            # Görsel değiştiyse mevcut analizi sıfırla
            import hashlib
            img_bytes = uploaded_image.tobytes()
            img_hash = hashlib.md5(img_bytes).hexdigest()
            
            if 'last_image_hash' not in st.session_state:
                st.session_state.last_image_hash = None
            
            if st.session_state.last_image_hash != img_hash:
                # Görsel değişmiş! Analizi sıfırla
                st.session_state.current_analysis = None
                st.session_state.last_image_hash = img_hash
                st.session_state.current_question_index = 1 # K4: İndeksi sıfırla
                st.toast("Yeni görsel algılandı, analiz için hazır.", icon="🆕")
                # Rerun gerekebilir ama butona basınca zaten işleyecek

        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Analiz butonu - Büyük ve belirgin
        analyze_button = st.button(
            "🤖 Analiz Et",
            type="primary",
            disabled=uploaded_image is None,
            use_container_width=True,
            key="analyze_btn"
        )
        
        # Yardım mesajı
        if not uploaded_image:
            st.info("👆 Önce bir soru görseli yükle", icon="💡")
    
    with col2:
        # Mevcut analiz varsa göster
        # Mevcut analiz varsa göster
        if 'current_analysis' in st.session_state and st.session_state.current_analysis:
            # Görüntüyü bulmaya çalış 
            # K4-B: Batch İlerleme Sistemi (Yerel) - ÜSTE TAŞINDI
            batch_results = st.session_state.get('batch_results', [])
            current_batch_idx = st.session_state.get('current_batch_index', 0)
            
            # Çoklu soru varsa navigasyon göster (ÜST KONUM)
            if batch_results and len(batch_results) > 1:
                # Progress Bar
                progress = (current_batch_idx + 1) / len(batch_results)
                st.progress(progress)
                
                col_prev, col_info, col_next = st.columns([1, 2, 1])
                
                with col_prev:
                    if current_batch_idx > 0:
                        if st.button("⬅️ Önceki", key="prev_q_top", use_container_width=True):
                            st.session_state.current_batch_index -= 1
                            st.session_state.current_analysis = batch_results[current_batch_idx - 1]
                            st.rerun()
                
                with col_info:
                    st.markdown(
                        f"""
                        <div style='text-align: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 15px;'>
                            <h4 style='margin:0; color:#4B4B4B'>Soru {current_batch_idx + 1} / {len(batch_results)}</h4>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                with col_next:
                    if current_batch_idx < len(batch_results) - 1:
                        if st.button("Sonraki ➡️", key="next_q_top", type="primary", use_container_width=True):
                            st.session_state.current_batch_index += 1
                            st.session_state.current_analysis = batch_results[current_batch_idx + 1]
                            st.rerun()

            elif has_multiple_questions and not batch_results:
                 # Manuel Mod Header
                 current_idx = st.session_state.get('current_question_index', 1)
                 st.info(f"📍 Şu an manuel modda **{current_idx}. Soru** analiz ediliyor.")

            # Görüntüyü bulmaya çalış 
            render_tabbed_results(st.session_state.current_analysis, uploaded_image)
            
            # Eski manuel sistem (Fallback) - Sadece manuel mod için altta buton kalsın
            if has_multiple_questions and not batch_results:
                current_idx = st.session_state.get('current_question_index', 1)
                st.markdown("---")
                if st.button("➡️ Sonraki Soruyu Analiz Et", type="primary", use_container_width=True):
                     st.session_state.current_question_index = current_idx + 1
                     st.session_state.current_analysis = None
                     st.session_state.auto_analyze = True
                     st.rerun()

        elif (analyze_button or st.session_state.get('auto_analyze', False)) and uploaded_image:
            # Auto analyze flag'ini sıfırla
            if 'auto_analyze' in st.session_state:
                del st.session_state.auto_analyze
                
            # AI analizi
            try:
                gemini = get_gemini_helper()
                
                # ÇOKLU SORU MODU (Enterprise Batch)
                if has_multiple_questions:
                    # Log event
                    logger = get_event_logger()
                    logger.log_event("batch_analysis_start", "current_user", {"model": model_type})

                    # Batch analizi çağır
                    results = gemini.analyze_image_batch(
                        uploaded_image,
                        model_type=model_type
                    )
                    
                    # Sonuç kontrolü
                    has_error = False
                    if results and len(results) > 0:
                        first_res = results[0]
                        if "error" in first_res:
                            has_error = True
                            st.error(f"⚠️ Toplu analizde sorun oluştu: {first_res['error']}")
                            st.info("Sistem otomatik olarak tekli manuel moda geçiyor...")
                            
                            # Fallback: Tekli moda geç
                            st.session_state.batch_results = []
                            # İlk soruyu tekli analiz etmeyi dene
                            q_idx = st.session_state.get('current_question_index', 1)
                            result = gemini.analyze_question_image(
                                uploaded_image,
                                model_type=model_type,
                                question_index=q_idx
                            )
                            st.session_state.current_analysis = result

                        else:
                            # Başarılı Batch
                            st.session_state.batch_results = results
                            st.session_state.current_batch_index = 0
                            st.session_state.current_analysis = results[0]
                            
                            gm.add_xp(20, f"🚀 {len(results)} soru tek seferde analiz edildi!")
                            st.toast(f"{len(results)} soru bulundu ve analiz edildi!", icon="✅")
                            
                            # Supabase'e kaydet
                            for res in results:
                                db.save_analysis_session({
                                    "student_id": "pilot_ogrenci_01",
                                    "question_text": res.get("soru_metni", ""),
                                    "solution_steps": str(res.get("cozum_adimlari", [])),
                                    "final_answer": res.get("dogru_cevap", ""),
                                    "difficulty_level": str(res.get("zorluk", 3)),
                                    "topic": res.get("konu", "Bilinmiyor"),
                                    "subtopic": res.get("alt_konu", "")
                                })
                    else:
                        st.error("AI hiçbir soru bulamadı.")
                        has_error = True

                else:
                    # Klasik Tekli Mod veya Beta Modu
                    q_idx = st.session_state.get('current_question_index', 1)
                    
                    # Log event
                    logger = get_event_logger()
                    logger.log_event("question_analysis_start", "current_user", {
                        "model": model_type,
                        "question_index": q_idx,
                        "beta_mode": beta_mode
                    })
                    
                    if beta_mode:
                        # ===== BETA MODU: Scaffolding + Perplexity =====
                        from utils.llm_adapter import get_llm_adapter
                        llm = get_llm_adapter()
                        
                        # Görsel bytes'a çevir
                        img_buffer = io.BytesIO()
                        uploaded_image.save(img_buffer, format="PNG")
                        img_bytes = img_buffer.getvalue()
                        
                        with st.spinner("🧪 Beta Modu: Adım adım çözüm hazırlanıyor..."):
                            result = llm.generate_beta_scaffolded_analysis(
                                question_text="Görseldeki soruyu çöz.",
                                image_data=img_bytes
                            )
                        
                        # Beta sonucunu session'a kaydet
                        st.session_state.beta_result = result
                        st.session_state.visible_step = 1  # Adım sayacını sıfırla
                        
                        # Beta sonucunu normal analiz formatına dönüştür (sekmeli UI için)
                        if isinstance(result, dict) and result.get("steps"):
                            steps_text = result.get("steps", [])
                            st.session_state.current_analysis = {
                                'konu': result.get("topic", "Bilinmiyor"),
                                'alt_konu': result.get("subtopic", ""),
                                'zorluk_seviyesi': result.get("difficulty", 3),
                                'soru_metni': '',
                                'cozum_adimlari': steps_text,
                                'dogru_cevap': result.get("final_answer", ""),
                                'ipucu': '',
                                'beta_mode': True,
                                'verification': result.get('verification', {}),
                            }
                            
                            # Analiz geçmişine ekle
                            st.session_state.analysis_history.append(st.session_state.current_analysis)
                            
                            # Veritabanına kaydet
                            if save_to_db:
                                db.save_analysis_session({
                                    "student_id": "pilot_ogrenci_01",
                                    "question_text": "",
                                    "solution_steps": str(steps_text),
                                    "final_answer": result.get("final_answer", ""),
                                    "difficulty_level": str(result.get("difficulty", 3)),
                                    "topic": result.get("topic", "Bilinmiyor"),
                                    "subtopic": result.get("subtopic", "")
                                })
                            
                            gm.add_xp(15, "🧪 Beta analizi tamamlandı!")
                            st.rerun()  # Sekmeli UI'ı göstermek için rerun
                        
                        # Fallback - inline UI göster (eskisi gibi)
                        if isinstance(result, dict) and result.get("steps"):
                            # CSS stilleri ekle
                            st.markdown("""
                            <style>
                            .beta-header {
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                padding: 1rem 1.5rem;
                                border-radius: 12px;
                                margin-bottom: 1rem;
                                font-weight: 600;
                            }
                            .step-card {
                                background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
                                border-left: 4px solid;
                                border-radius: 8px;
                                padding: 1rem;
                                margin-bottom: 0.75rem;
                                transition: transform 0.2s;
                            }
                            .step-card:hover {
                                transform: translateX(5px);
                            }
                            .step-1 { border-color: #4CAF50; }
                            .step-2 { border-color: #2196F3; }
                            .step-3 { border-color: #FF9800; }
                            .step-4 { border-color: #9C27B0; }
                            .step-5 { border-color: #E91E63; }
                            .step-badge {
                                display: inline-block;
                                width: 28px;
                                height: 28px;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                border-radius: 50%;
                                text-align: center;
                                line-height: 28px;
                                font-weight: bold;
                                margin-right: 10px;
                            }
                            .topic-badge {
                                display: inline-block;
                                background: #e3f2fd;
                                color: #1565c0;
                                padding: 4px 12px;
                                border-radius: 20px;
                                font-size: 0.85rem;
                                margin-right: 8px;
                            }
                            .difficulty-badge {
                                display: inline-block;
                                background: #fff3e0;
                                color: #e65100;
                                padding: 4px 12px;
                                border-radius: 20px;
                                font-size: 0.85rem;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Header
                            st.markdown('<div class="beta-header">🧬 LGS-Zeka Asistanı Çözüm Adımları</div>', unsafe_allow_html=True)
                            
                            # Konu ve Zorluk badge'leri
                            topic = result.get("topic", "Genel")
                            difficulty = result.get("difficulty", 3)
                            diff_text = {1: "Kolay", 2: "Kolay-Orta", 3: "Orta", 4: "Orta-Zor", 5: "Zor"}.get(difficulty, "Orta")
                            
                            st.markdown(f'''
                            <div style="margin-bottom: 1rem;">
                                <span class="topic-badge">📚 {topic}</span>
                                <span class="difficulty-badge">⚡ {diff_text}</span>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                            # Adımları expander ile göster (Basit ve stabil)
                            steps = result.get("steps", [])
                            total_steps = len(steps)
                            
                            # İkon seti
                            icons = ["🔍", "📐", "✏️", "🔢", "✅"]
                            
                            for i, step in enumerate(steps):
                                icon = icons[i % len(icons)]
                                step_num = i + 1
                                
                                # Dinamik başlık
                                if i == 0:
                                    title = f"{icon} Adım {step_num}: Analiz"
                                elif i == total_steps - 1:
                                    title = f"{icon} Adım {step_num}: Sonuç"
                                else:
                                    title = f"{icon} Adım {step_num}: İşlem"
                                
                                # İlk adım açık, diğerleri kapalı
                                with st.expander(title, expanded=(i == 0)):
                                    st.markdown(f"""
                                    <div style="padding: 0.5rem; border-left: 3px solid {'#4CAF50' if i == 0 else '#2196F3' if i < total_steps-1 else '#FF9800'}; margin-left: 0.5rem;">
                                        {step}
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Güven skoru
                            st.write("---")
                            confidence = result.get("confidence", 0)
                            col_conf, col_answer = st.columns([3, 1])
                            
                            with col_conf:
                                st.progress(confidence / 100)
                                st.caption(f"AI Güven Skoru: %{confidence}")
                                
                                # Perplexity doğrulaması
                                verification = result.get("verification", {})
                                v_status = verification.get("verification_status", "unavailable")
                                if v_status == "confirmed":
                                    st.success("✅ Çözüm denetçi tarafından doğrulandı")
                                elif v_status == "disputed":
                                    critic_note = verification.get('critic_note', '')
                                    suggested = verification.get('suggested_answer', '')
                                    
                                    st.warning(f"⚠️ Denetçi farklı düşünüyor: {critic_note[:150]}")
                                    
                                    # Denetçinin önerdiği cevabı göster
                                    if suggested and suggested.strip():
                                        st.error(f"🔍 Denetçi Önerisi: **{suggested}**")
                                # Hata durumunu gösterme (unavailable, parse_error vb.)
                            
                            with col_answer:
                                # Spoiler Koruması: Gemini cevabını popover ile gizle
                                with st.popover("Cevabı Gör 👁️"):
                                    gemini_answer = result.get('final_answer', 'Cevap bulunamadı')
                                    st.markdown(f"### Gemini: {gemini_answer}")
                                    
                                    # Eğer denetçi farklı cevap önerdiyse onu da göster
                                    verification = result.get("verification", {})
                                    suggested = verification.get('suggested_answer', '')
                                    if suggested and suggested.strip() and verification.get("verification_status") == "disputed":
                                        st.markdown("---")
                                        st.markdown(f"### 🔍 Denetçi: {suggested}")
                            
                            gm.add_xp(15, "🧪 Beta analizi tamamlandı!")
                        else:
                            # Fallback
                            st.warning("Beta modu düz metin döndürdü:")
                            st.markdown(result.get("final_answer", str(result)))
                    else:
                        # Normal analiz (Eski usul)
                        result = gemini.analyze_question_image(
                            uploaded_image,
                            model_type=model_type,
                            question_index=q_idx
                        )
                        
                        if "error" in result:
                            st.error(f"❌ Analiz hatası: {result['error']}")
                            # Debug: Ham yanıtı göster
                            if "ham_yanit" in result:
                                with st.expander("🔍 Debug: AI Ham Yanıtı", expanded=True):
                                    st.code(result["ham_yanit"][:2000], language="json")
                        else:
                            # Başarılı tekli analiz
                            gm.add_xp(10, "Soru analizi tamamlandı! 🎯")
                            st.session_state.batch_results = [] # Temizle
                            st.session_state.current_analysis = result
                
                # Ortak Kayıt İşlemleri (Eğer current_analysis set edildiyse)
                if st.session_state.get('current_analysis'):
                    current_res = st.session_state.current_analysis
                    
                    # ID ve Timestamp
                    if 'question_id' not in current_res:
                        current_res['question_id'] = f"q_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    current_res['timestamp'] = datetime.now().isoformat()
                    
                    # Geçmişe ekle
                    st.session_state.analysis_history.append(current_res)
                    
                    # DB Kayıt
                    if save_to_db:
                        save_analysis_to_db(current_res, uploaded_image)
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {str(e)}")
                st.exception(e)
        
        else:
            # Placeholder - Modern ve öğrenci dostu
            st.markdown("""
            <div style='
                text-align: center;
                padding: 4rem 2rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                color: white;
            '>
                <h2 style='margin: 0; color: white;'>🚀 Hazır mısın?</h2>
                <p style='font-size: 1.2rem; margin: 1rem 0; color: white;'>
                    Soldan bir soru görseli yükle ve AI ile analiz et!
                </p>
                <div style='
                    background: rgba(255,255,255,0.2);
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin-top: 2rem;
                '>
                    <p style='margin: 0.5rem 0; color: white;'>📁 Dosya yükle veya 📷 Fotoğraf çek</p>
                    <p style='margin: 0.5rem 0; color: white;'>🤖 AI analiz eder</p>
                    <p style='margin: 0.5rem 0; color: white;'>🎯 Adım adım çözüm + Hoca desteği!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Geçmiş analizler
    st.markdown("---")
    st.markdown("### 📚 Analiz Geçmişi")
    
    if st.session_state.analysis_history:
        # Filtreleme
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            filter_topic = st.multiselect(
                "Konuya Göre Filtrele",
                options=list(set(h.get('konu', 'Bilinmiyor') for h in st.session_state.analysis_history))
            )
        
        with col2:
            filter_difficulty = st.multiselect(
                "Zorluk Seviyesi",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{'⭐' * x}"
            )
        
        with col3:
            if st.button("🗑️ Geçmişi Temizle"):
                st.session_state.analysis_history = []
                st.rerun()
        
        # Filtrelenmiş sonuçlar
        filtered_history = st.session_state.analysis_history
        
        if filter_topic:
            filtered_history = [h for h in filtered_history if h.get('konu') in filter_topic]
        
        if filter_difficulty:
            filtered_history = [h for h in filtered_history if h.get('zorluk_seviyesi') in filter_difficulty]
        
        # Sonuçları göster
        for i, analysis in enumerate(reversed(filtered_history)):
            with st.expander(
                f"📄 {analysis.get('konu', 'Bilinmiyor')} - "
                f"{analysis.get('alt_konu', '')} "
                f"({analysis.get('timestamp', 'Zaman bilinmiyor')})"
            ):
                display_analysis_results(analysis, compact=True)
    
    else:
        st.info("Henüz analiz geçmişi yok. İlk sorunuzu yükleyin!")


def render_tabbed_results(result: Dict[str, Any], image: Optional[Image.Image]):
    """
    Analiz sonuçlarını sekmeli yapıda gösterir.
    
    Args:
        result: Analiz sonucu
        image: Soru görseli
    """
    # Üst kısım: Havuza ekleme butonu
    render_save_to_pool_button(result, image)
    
    # Sekmeli yapı
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Hızlı Çözüm",
        "🧠 Detaylı Analiz",
        "🎓 Hoca Modu",
        "🎯 Benzer Soru",
        "📝 Notlarım"
    ])
    
    with tab1:
        render_quick_solution(result)
    
    with tab2:
        render_detailed_analysis(result)
    
    with tab3:
        render_teacher_mode(result)
        
    with tab4:
        render_similar_question_tab(result)
        
    with tab5:
        render_user_notes(result)

    # Alt kısım - Hata etiketleme
    st.markdown("---")
    show_error_tagger(
        result.get('question_id', 'unknown'),
        {
            'konu': result.get('konu', 'Bilinmiyor'),
            'zorluk': result.get('zorluk', 'Orta')
        }
    )
    
    # Debug: Ham Yanıt Görüntüleyici (Hata durumunda)
    if "ham_yanit" in result:
        with st.expander("🛠️ Geliştirici: Ham AI Yanıtı (Debug)", expanded=False):
            st.warning("Bu alan hata ayıklama amaçlıdır. AI'dan gelen ham metni gösterir.")
            st.code(result["ham_yanit"], language="text")


def render_similar_question_tab(result: Dict[str, Any]):
    """
    Benzer soru (JIT Learning) sekmesi.
    """
    st.markdown("""
    <div style='
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    '>
        <h4 style='margin:0; color: #1565C0;'>🔄 Pekiştirme Zamanı!</h4>
        <p style='margin:0;'>Bu konuyu tam oturtmak için benzer bir soru çözmek ister misin?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # State key
    variant_key = f"variant_{result.get('question_id', 'temp')}"
    
    if variant_key not in st.session_state:
        if st.button("🚀 Benzer Soru Üret", type="primary", use_container_width=True):
            gemini = get_gemini_helper()
            
            variant_result = gemini.generate_variant(
                question_text=result.get('soru_metni', ''),
                topic=result.get('konu', ''),
                difficulty=result.get('zorluk_seviyesi', 3)
            )
            
            if "error" not in variant_result:
                st.session_state[variant_key] = variant_result
                st.rerun()
            else:
                st.error("Soru üretilemedi.")
    
    else:
        # Soruyu göster
        variant = st.session_state[variant_key]
        
        st.markdown(f"**❓ Soru:** {variant.get('soru_metni')}")
        
        # Seçenekler
        options = variant.get('secenekler', {})
        correct_opt = variant.get('dogru_cevap', '').strip().upper()
        
        # Kullanıcı cevabı
        user_answer = st.radio(
            "Cevabınız:",
            options=list(options.keys()),
            format_func=lambda x: f"{x}) {options[x]}"
        )
        
        if st.button("✅ Cevabı Kontrol Et", use_container_width=True):
            if user_answer == correct_opt:
                st.balloons()
                st.success(f"Tebrikler! Doğru cevap: {correct_opt}")
                
                # XP Ödülü
                from utils.gamification import get_gamification_manager
                gm = get_gamification_manager()
                gm.add_xp(15, "Ekstra soru çözümü! 💪")
                
            else:
                st.error(f"Maalesef yanlış. Doğru cevap: {correct_opt}")
            
            # Çözümü göster
            with st.expander("📘 Çözüm Açıklaması", expanded=True):
                cozum_list = variant.get('cozum_adimlari', [])
                if isinstance(cozum_list, list):
                    for step in cozum_list:
                        st.info(step)
                else:
                    st.info(str(cozum_list))
        
        # Yeni soru butonu
        if st.button("🔄 Başka Soru Üret"):
            del st.session_state[variant_key]
            st.rerun()


def render_save_to_pool_button(result: Dict[str, Any], image: Optional[Image.Image]):
    """
    Analiz sonucunu soru havuzuna ekleme butonu (K6).
    """
    st.markdown("### 📥 Soru Havuzu İşlemleri")
    
    # Zaten eklendi mi kontrolü
    is_added = result.get('is_added_to_pool', False)
    
    if is_added:
        st.success("✅ Bu soru havuza eklendi.")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
             st.info("Bu soruyu soru havuzuna ekleyerek denemelerde kullanabilirsiniz.")
        with col2:
            if st.button("📥 Havuza Ekle", type="primary", use_container_width=True):
                if image:
                    success = save_question_to_pool(result, image)
                    if success:
                        result['is_added_to_pool'] = True
                        st.rerun()
                        
        if st.button("🔄 Tekrar Kontrol Et", help="AI sonucundan memnun değilseniz tekrar analiz edin."):
            st.session_state.current_analysis = None
            st.session_state.auto_analyze = True  # Yeniden analiz tetikle
            st.rerun()


def render_quick_solution(result: Dict[str, Any]):
    """Hızlı çözüm sekmesi."""
    # Doğru cevap - Büyük gösterim
    dogru_cevap = result.get('dogru_cevap', '?')
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    '>
        <p style='color: white; margin: 0; font-size: 1rem; opacity: 0.9;'>✅ DOĞRU CEVAP</p>
        <h1 style='color: white; margin: 0.5rem 0; font-size: 4rem;'>{dogru_cevap}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sesli anlat butonu
    col_audio, col_spacer = st.columns([1, 3])
    with col_audio:
        if st.button("🔊 Sesli Oku", key="audio_quick_answer", help="Cevabı sesli dinle"):
            try:
                from utils.audio_service import get_audio_service
                audio_service = get_audio_service()
                
                # Cevap ve özeti birleştir
                ozet = result.get('ipucu', result.get('ozet', ''))
                text_to_read = f"Doğru cevap {dogru_cevap}. {ozet}"
                
                with st.spinner("🎙️ Ses oluşturuluyor..."):
                    audio_data = audio_service.speak_text(text_to_read)
                    
                    if audio_data:
                        st.session_state['quick_audio'] = audio_data
                        st.toast("✅ Ses hazır!", icon="🔊")
                    else:
                        st.error("❌ Ses oluşturulamadı.")
            except Exception as e:
                st.error(f"Ses hatası: {e}")
                
    with col_spacer:
        # Konu Çalış Butonu - Tek Tıkla Öğrenme
        if st.button("📚 Bu Konuyu Çalış", help="İlgili konuyu öğrenme moduna geç", use_container_width=True):
            st.session_state['redirect_to'] = "Öğren"  # Yeni güvenli yönlendirme
            st.session_state['learning_topic'] = result.get('konu')
            st.session_state['learning_subtopic'] = result.get('alt_konu')
            st.session_state['learning_lesson'] = result.get('ders')
            st.rerun()
    
    # Eğer ses varsa oynat
    if 'quick_audio' in st.session_state and st.session_state.quick_audio:
        st.audio(st.session_state.quick_audio, format="audio/mp3")
    
    # Özet mantık
    ozet = result.get('ozet', result.get('ipucu', ''))
    if ozet:
        st.markdown("#### 📌 Özet Mantık")
        st.info(ozet)
    
    # Metrikler
    col1, col2 = st.columns(2)
    
    with col1:
        tahmini_sure = result.get('tahmini_sure', 'Bilinmiyor')
        st.metric("⏱️ Tahmini Süre", tahmini_sure)
    
    with col2:
        zorluk = result.get('zorluk_seviyesi', 3)
        st.metric("⭐ Zorluk", f"{zorluk}/5")


def render_detailed_analysis(result: Dict[str, Any]):
    """Detaylı analiz sekmesi."""
    
    # Beta Mode analiz sonucu varsa özel DeepTutor UI göster
    if result.get('beta_mode', False):
        st.markdown("### 🧪 DeepTutor - Beta Analiz Sonuçları")
        
        # Verification bilgisi
        verification = result.get('verification', {})
        v_status = verification.get("verification_status", "unavailable")
        
        if v_status == "confirmed":
            st.success("✅ Çözüm denetçi tarafından doğrulandı")
        elif v_status == "disputed":
            critic_note = verification.get('critic_note', '')
            suggested = verification.get('suggested_answer', '')
            st.warning(f"⚠️ Denetçi farklı düşünüyor: {critic_note[:150]}")
            if suggested and suggested.strip():
                st.error(f"🔍 Denetçi Önerisi: **{suggested}**")
        
        # Çözüm adımları
        steps = result.get('cozum_adimlari', [])
        if steps and isinstance(steps, list):
            st.markdown("#### 📝 Çözüm Adımları")
            icons = ["🔍", "📐", "✏️", "🔢", "✅"]
            for i, step in enumerate(steps):
                icon = icons[i % len(icons)]
                with st.expander(f"{icon} Adım {i+1}", expanded=(i==0)):
                    if isinstance(step, dict):
                        st.markdown(step.get('content', str(step)))
                    else:
                        st.markdown(str(step))
        
        # Cevap popover
        with st.popover("🎯 Doğru Cevabı Gör"):
            st.markdown(f"### {result.get('dogru_cevap', 'Cevap bulunamadı')}")
            if v_status == "disputed":
                suggested = verification.get('suggested_answer', '')
                if suggested:
                    st.markdown("---")
                    st.markdown(f"### 🔍 Denetçi: {suggested}")
        
        return
    
    # Normal detaylı analiz
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**📚 Konu:** {result.get('konu', 'Bilinmiyor')}")
        if result.get('alt_konu'):
            st.markdown(f"**📌 Alt Konu:** {result.get('alt_konu')}")
    
    with col2:
        difficulty = result.get('zorluk_seviyesi', 3)
        st.markdown(
            f"**Zorluk:** {get_difficulty_badge(difficulty)}",
            unsafe_allow_html=True
        )
    
    # Soru metni
    soru_metni = result.get('soru_metni', '')
    if soru_metni:
        with st.expander("📖 Soru Metni", expanded=False):
            st.markdown(soru_metni)
    
    # Çözüm adımları
    cozum_adimlari = result.get('cozum_adimlari', [])
    
    if cozum_adimlari:
        # Başlık ve sesli anlatım butonu
        col_title, col_audio = st.columns([3, 1])
        
        with col_title:
            st.markdown("#### ✅ Çözüm Adımları")
        
        with col_audio:
            if st.button("🔊 Sesli Anlat", key="audio_narrate_solution", help="Çözümü sesli dinle"):
                try:
                    from utils.audio_service import get_audio_service
                    audio_service = get_audio_service()
                    
                    with st.spinner("🎙️ Ses oluşturuluyor..."):
                        audio_data = audio_service.narrate_solution(cozum_adimlari)
                        
                        if audio_data:
                            st.session_state['solution_audio'] = audio_data
                            st.toast("✅ Ses hazır!", icon="🔊")
                        else:
                            st.error("❌ Ses oluşturulamadı.")
                except Exception as e:
                    st.error(f"Ses hatası: {e}")
        
        # Eğer ses varsa oynat
        if 'solution_audio' in st.session_state and st.session_state.solution_audio:
            st.audio(st.session_state.solution_audio, format="audio/mp3")
        
        # Adımları göster
        for i, adim in enumerate(cozum_adimlari, 1):
            st.markdown(f"**Adım {i}:**")
            st.info(adim)
    
    # Mermaid diyagramı (varsa)
    mermaid_diagram = result.get('mermaid_diagram', '')
    if mermaid_diagram:
        st.markdown("#### 📊 Görsel Akış")
        try:
            render_mermaid(mermaid_diagram, height=400)
        except:
            # Fallback: Adımlardan diyagram oluştur
            if cozum_adimlari:
                fallback_diagram = create_solution_flowchart(cozum_adimlari)
                render_mermaid(fallback_diagram, height=400)
    
    # Benzer konular
    benzer_konular = result.get('benzer_konular', [])
    if benzer_konular:
        with st.expander("🔗 Benzer Konular"):
            for konu in benzer_konular:
                st.markdown(f"• {konu}")


def render_teacher_mode(result: Dict[str, Any]):
    """Hoca modu sekmesi."""
    st.markdown("""
    <div style='
        background-color: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    '>
        <h3 style='margin: 0 0 0.5rem 0;'>👨‍🏫 Öğretmen Desteği</h3>
        <p style='margin: 0;'>
            Bu konuyu tam olarak anlamak için benimle sohbet edebilirsin!
            Sana sorular soracağım, sen de düşünerek cevap vereceksin. 🤔
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Konu özeti
    konu = result.get('konu', 'Bu konu')
    zorluk = result.get('zorluk_seviyesi', 3)
    
    st.markdown(f"""
    **📚 Konu:** {konu}  
    **⭐ Zorluk:** {zorluk}/5
    """)
    
    # Öğretmen butonu
    if st.button(
        "🎯 Bu Konuyu Bana Öğret",
        type="primary",
        use_container_width=True,
        key="teacher_button"
    ):
        st.session_state.teacher_mode_active = True
        
    if st.session_state.get("teacher_mode_active", False):
        # Modal chat aç
        show_socratic_chat({
            "question_id": result.get('question_id'),
            "konu": result.get('konu', 'Bilinmiyor'),
            "zorluk": f"{result.get('zorluk_seviyesi', 3)}/5",
            "dogru_cevap": result.get('dogru_cevap', ''),
            "ipucu": result.get('ipucu', ''),
            "soru_metni": result.get('soru_metni', ''),
            "cozum_adimlari": result.get('cozum_adimlari', [])
        }, state_key="teacher_mode_active")
    
    # Motivasyon mesajı
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    '>
        <h4 style='margin: 0; color: white;'>💪 Sen Yaparsın!</h4>
        <p style='margin: 0.5rem 0 0 0; color: white;'>
            Her soru bir adım daha yaklaştırıyor seni hedefe! 🎯
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_user_notes(result: Dict[str, Any]):
    """Kullanıcı notları sekmesi (K3)."""
    st.markdown("### 📝 Soru Notları")
    st.markdown("Bu soruyla ilgili hatırlatmalar veya notlar ekleyin.")
    
    current_note = result.get('user_note', '')
    
    new_note = st.text_area(
        "Notunuz:",
        value=current_note,
        height=150,
        placeholder="Örn: Bu soru tipini sınavdan önce tekrar etmeliyim..."
    )
    
    if st.button("💾 Notu Kaydet", use_container_width=True):
        if new_note != current_note:
            # Session state güncelle
            result['user_note'] = new_note
            st.success("Not kaydedildi!")
            
            # İleride DB güncellemesi de yapılabilir:
            # db.update_analysis_note(result['question_id'], new_note)



def display_analysis_results(result: Dict[str, Any], compact: bool = False):
    """
    Analiz sonuçlarını görüntüler.
    
    Args:
        result: Analiz sonucu dictionary
        compact: Kompakt görünüm (geçmiş için)
    """
    
    # Konu ve zorluk
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**📚 Konu:** {result.get('konu', 'Bilinmiyor')}")
        if result.get('alt_konu'):
            st.markdown(f"**📌 Alt Konu:** {result.get('alt_konu')}")
    
    with col2:
        difficulty = result.get('zorluk_seviyesi', 3)
        st.markdown(
            f"**Zorluk:** {get_difficulty_badge(difficulty)}",
            unsafe_allow_html=True
        )
    
    # Soru metni
    if not compact:
        with st.expander("📖 Soru Metni", expanded=True):
            st.markdown(result.get('soru_metni', 'Metin okunamadı'))
    
    # Çözüm adımları
    steps = result.get('cozum_adimlari', [])
    if steps:
        with st.expander("✅ Çözüm Adımları", expanded=not compact):
            for i, step in enumerate(steps, 1):
                st.markdown(f"**Adım {i}:**")
                st.info(step)
    
    # Doğru cevap
    if result.get('dogru_cevap'):
        st.success(f"**✓ Doğru Cevap:** {result.get('dogru_cevap')}")
    
    # İpucu
    if result.get('ipucu'):
        with st.expander("💡 İpucu"):
            st.warning(result.get('ipucu'))
    
    # Ek bilgiler
    if not compact:
        col1, col2 = st.columns(2)
        
        with col1:
            if result.get('tahmini_sure'):
                st.metric("⏱️ Tahmini Süre", result.get('tahmini_sure'))
        
        with col2:
            if result.get('model_used'):
                model_label = "⚡ Flash" if result.get('model_used') == "flash" else "🎯 Pro"
                st.metric("🤖 Kullanılan Model", model_label)
        
        # Benzer konular
        if result.get('benzer_konular'):
            with st.expander("🔗 Benzer Konular"):
                for topic in result.get('benzer_konular', []):
                    st.markdown(f"- {topic}")
        
        # Sık yapılan hatalar
        if result.get('hatali_yaklasimlar'):
            with st.expander("⚠️ Sık Yapılan Hatalar"):
                for mistake in result.get('hatali_yaklasimlar', []):
                    st.markdown(f"- {mistake}")


def save_question_to_pool(result: Dict[str, Any], image: Image.Image) -> bool:
    """
    Analizi soru havuzuna (questions.csv) ekler (K6).
    """
    try:
        import os
        
        # 1. Görseli Kaydet
        # Klasör: assets/questions/
        base_dir = Path("assets/questions")
        base_dir.mkdir(parents=True, exist_ok=True)
        
        # Dosya adı: question_id.png
        q_id = result.get('question_id', f"ai_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        filename = f"{q_id}.png"
        file_path = base_dir / filename
        
        # Resmi kaydet
        image.save(file_path, format="PNG")
        
        # 2. Veriyi Hazırla
        # Seçenekleri JSON formatına çevir (Varsayılan boş şıklar veya analizden gelirse onu kullan)
        # Analiz şu an şıkları ayırmıyor, o yüzden standart bir yapı kullanalım veya boş bırakalım.
        # Manuel düzenleme gerektirebilir.
        options = {
            "A": "",
            "B": "",
            "C": "",
            "D": ""
        }
        
        # Doğru cevabı formatla
        correct_opt = result.get('dogru_cevap', '').strip().upper()
        if len(correct_opt) > 1:
            # Eğer cevap "A şıkkı" gibi uzunsa sadece ilk harfi al
             correct_opt = correct_opt[0] if correct_opt[0] in ['A', 'B', 'C', 'D'] else ''
        
        import json
        
        question_data = {
            "question_id": q_id,
            "question_text": result.get('soru_metni', ''), # Soru metni (OCR)
            "options_json": json.dumps(options),
            "correct_option": correct_opt,
            "lesson": "Matematik", # TODO: AI bunu tespit etmeli veya kullanıcı seçmeli (şimdilik Mat varsayılan)
            "topic": result.get('konu', 'Genel'),
            "subtopic": result.get('alt_konu', ''),
            "difficulty_label": result.get('zorluk_seviyesi', 3),
            "question_type": "mcq",
            "question_origin": "ai_captured",
            "origin_detail": "soru_analiz_upload",
            "active": True,
            "created_at": datetime.now().isoformat(),
            
            # Görsel alanları (Kritik)
            "has_figure": True,
            "figure_path": str(file_path).replace("\\", "/"), # Windows path fix
            "figure_type": "scanned",
            "figure_policy": "no_variant", # Varyant üretme, resmi kullan
            "has_figure_final": True
        }
        
        # 3. DB'ye Ekle
        db = get_db_manager()
        # questions sheet'ine ekle (append=True)
        # db.add_data fonksiyonu dict kabul ediyor mu? Evet.
        # Ancak db.add_data genellikle 'append' mantığıyla çalışır.
        
        # questions tablosu (csv) için doğrudan add_data metodunu kullanalım
        # Sheet adı 'Questions' (büyük harf duyarlı olabilir, db_manager kontrol edilmeli)
        # Genelde sheet isimleri db_manager'da tanımlı.
        
        success = db.add_data("questions", question_data)
        
        if success:
            st.toast("Soru havuza eklendi! 🚀", icon="✅")
            return True
        else:
            st.error("Veritabanına eklenirken hata oluştu.")
            return False
            
    except Exception as e:
        st.error(f"Kayıt hatası: {str(e)}")
        return False


def save_analysis_to_db(result: Dict[str, Any], image: Image.Image):
    """
    Analiz sonucunu veritabanına kaydeder.
    
    Args:
        result: Analiz sonucu
        image: Soru görseli
    """
    try:
        db = get_db_manager()
        
        # Supabase analysis_sessions şemasına uygun data
        data = {
            "student_id": "pilot_ogrenci_01",
            "question_text": result.get('soru_metni', ''),
            "solution_steps": str(result.get('cozum_adimlari', [])),
            "final_answer": result.get('dogru_cevap', ''),
            "difficulty_level": str(result.get('zorluk_seviyesi', 3)),
            "topic": result.get('konu', 'Bilinmiyor'),
            "subtopic": result.get('alt_konu', '')
        }
        
        # Doğru fonksiyonu kullan: save_analysis_session
        success = db.save_analysis_session(data)
        
        if success:
            st.toast("💾 Analiz veritabanına kaydedildi", icon="✅")
            
    except Exception as e:
        st.error(f"Kayıt hatası: {e}")


# Sayfa çağrıldığında
if __name__ == "__main__":
    show()
