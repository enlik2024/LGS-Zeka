"""
Sokratik Chat Modal
AI öğretmen ile etkileşimli sohbet penceresi (JSON Tabanlı)
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Optional, List
from utils.socratic_manager import get_socratic_manager
from utils.gemini_helper import get_gemini_helper
from components.mermaid_renderer import render_mermaid
from components.flashcard_viewer import show_flashcard_session
from utils.audio_service import get_audio_service
from utils.event_logger import get_event_logger


# Sokratik öğretmen prompt'u
SOCRATIC_TUTOR_PROMPT = """
Sen bir Sokratik öğretmensin. Öğrenciye cevabı direkt söylemek yerine, 
sorular sorarak düşünmesini sağla ve cevabı kendisinin bulmasına yardımcı ol.

İLKELER:
1. Cevabı asla direkt verme
2. Küçük adımlarla ilerle (scaffolding)
3. Analoji ve örnekler kullan
4. Pozitif ve destekleyici ol
5. Maksimum 2-3 cümle yaz
6. Emoji kullan
"""


@st.dialog("👨‍🏫 Öğretmen ile Sohbet", width="large")
def show_socratic_chat(question_context: Dict, state_key: Optional[str] = None):
    """
    Sokratik öğretim için modal chat penceresi.
    
    Args:
        question_context: Soru bağlamı
            - konu: Soru konusu
            - zorluk: Zorluk seviyesi
            - dogru_cevap: Doğru cevap
            - ipucu: İpucu metni
        state_key: Modal'ın açık kalmasını sağlayan session state anahtarı (varsa kapatırken False yapılır)
    """
    # CSS stil
    st.markdown("""
    <style>
    .chat-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .chat-tip {
        background-color: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 0.8rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(f"""
    <div class='chat-header'>
        <h3 style='margin: 0;'>👨‍🏫 Öğretmen ile Sohbet</h3>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Konu: {question_context.get('konu', 'Bilinmiyor')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Açıklama
    st.markdown("""
    <div class='chat-tip'>
        💡 <strong>Nasıl Çalışır?</strong><br>
        Ben sana sorular soracağım, sen de düşünerek cevap vereceksin.
        Cevabı direkt söylemeyeceğim, birlikte bulacağız! 🤔
    </div>
    """, unsafe_allow_html=True)

    # Otomatik Oku Checkbox
    # Otomatik Oku Checkbox (Chat Key'e bağlı olmalı)
    chat_key = f"socratic_chat_{question_context.get('question_id', 'default')}"
    auto_speak_key = f"auto_speak_{chat_key}"
    auto_speak = st.checkbox("🔊 Hocayı otomatik seslendir", value=False, key=auto_speak_key)
    
    # Hata mesajı varsa göster
    error_key = f"{chat_key}_error"
    if error_key in st.session_state:
        st.error(st.session_state[error_key])
        del st.session_state[error_key]
    
    logger = get_event_logger()
    
    if chat_key not in st.session_state:
        logger.log_event("chat_session_start", "current_user", {
            "topic": question_context.get('konu'),
            "question_id": question_context.get('question_id')
        })
        st.session_state[chat_key] = []
        
        # İlk karşılama mesajı (JSON formatında)
        greeting_json = generate_greeting(question_context)
        greeting_text = greeting_json.get('content', {}).get('message_text', 'Merhaba! 👋')
        
        st.session_state[chat_key].append({
            "role": "assistant",
            "content": greeting_text,
            "json_data": greeting_json,  # JSON'u da sakla
            "timestamp": datetime.now().isoformat()
        })
        
        # İlk mesaj için auto-speak (eğer açıksa)
        if st.session_state.get(f"{state_key}_auto_speak" if state_key else "socratic_auto_speak", False):
            # Buraya da eklenebilir ama genelde kullanıcı açana kadar ilk mesaj geçmiş olur.
            pass

    # Autoplay audio varsa çal ve sil
    autoplay_key = f"{chat_key}_autoplay_audio"
    if autoplay_key in st.session_state:
        st.audio(st.session_state[autoplay_key], format="audio/mp3", autoplay=True)
        del st.session_state[autoplay_key]
    
    # Flashcard modu kontrolü
    if st.session_state.get(f"{chat_key}_mode") == 'flashcard':
        flashcards = st.session_state.get(f"{chat_key}_flashcards", [])
        if flashcards:
            show_flashcard_session(flashcards, question_context.get('konu', ''))
            
            # Geri dön butonu
            if st.button("⬅️ Sohbete Dön", use_container_width=True):
                st.session_state[f"{chat_key}_mode"] = 'chat'
                st.rerun()
            return
    
    # Mesaj geçmişini göster (key ile dinamik render)
    message_count = len(st.session_state[chat_key])
    chat_container = st.container(height=400, key=f"chat_container_{message_count}")
    with chat_container:
        for idx, message in enumerate(st.session_state[chat_key]):
            avatar = "👤" if message["role"] == "user" else "👨‍🏫"
            is_last_message = (idx == len(st.session_state[chat_key]) - 1)
            
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                
                # JSON data varsa (AI yanıtı), ek öğeleri göster
                # Sesli Dinle Butonu (AI mesajları için)
                if message["role"] == "assistant":
                    # Buton ID'si benzersiz olmalı
                    btn_key = f"tts_btn_{idx}_{message.get('timestamp', '0')}"
                    
                    # Yan yana yerleşim için columns (isteğe bağlı, şimdilik altına koyuyoruz)
                    if st.button("🔊 Dinle", key=btn_key, help="Bu mesajı sesli oku"):
                        audio_svc = get_audio_service()
                        with st.spinner("Ses hazırlanıyor..."):
                            audio_data = audio_svc.speak_text(message["content"])
                            if audio_data:
                                st.audio(audio_data, format="audio/mp3", autoplay=True)

                # Sadece son mesajda visual aid ve suggested options göster
                if "json_data" in message and message["role"] == "assistant":
                    json_data = message["json_data"]
                    
                    # Visual aid (Mermaid diyagram) - Sadece son mesajda
                    if is_last_message:
                        visual_aid = json_data.get('visual_aid', {})
                        if visual_aid.get('required', False) and visual_aid.get('code'):
                            st.markdown(f"**📊 {visual_aid.get('caption', 'Görsel')}**")
                            try:
                                mermaid_code = visual_aid.get('code', '').strip()
                                if mermaid_code:
                                    render_mermaid(mermaid_code, height=300)
                            except Exception as e:
                                st.warning(f"⚠️ Diyagram gösterilemedi: {str(e)}")
                        
                        # Suggested options (Hızlı butonlar) - Sadece son mesajda
                        suggested_options = json_data.get('interaction', {}).get('suggested_options', [])
                        if suggested_options:
                            st.markdown("**💡 Öneriler:**")
                            cols = st.columns(len(suggested_options))
                            for opt_idx, option in enumerate(suggested_options):
                                with cols[opt_idx]:
                                    if st.button(option, key=f"opt_{message['timestamp']}_{opt_idx}", use_container_width=True):
                                        handle_user_input(option, chat_key, question_context)
    
    # Hızlı yanıt butonları (ilk mesajda)
    if len(st.session_state[chat_key]) == 1:
        st.markdown("**Hızlı Başlangıç:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🤔 Nereden başlamalıyım?", use_container_width=True):
                handle_user_input(
                    "Nereden başlamalıyım?",
                    chat_key,
                    question_context
                )
        
        with col2:
            if st.button("💡 İpucu ver", use_container_width=True):
                handle_user_input(
                    "Bana bir ipucu verir misin?",
                    chat_key,
                    question_context
                )
        
        with col3:
            if st.button("📚 Konuyu açıkla", use_container_width=True):
                handle_user_input(
                    "Bu konuyu açıklar mısın?",
                    chat_key,
                    question_context
                )
    
    # Kullanıcı girişi
    user_input = st.chat_input(
        "Cevabını yaz veya soru sor...",
        key=f"chat_input_{chat_key}"
    )
    
    if user_input:
        handle_user_input(user_input, chat_key, question_context)
    
    # Alt butonlar
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("✅ Anladım, Teşekkürler!", 
                    type="primary", 
                    use_container_width=True):
            # XP ver
            from utils.gamification import get_gamification_manager
            gm = get_gamification_manager()
            gm.add_xp(50, "Öğretmen ile sohbet tamamlandı! 🎓")
            
            # Geçmişi temizle
            del st.session_state[chat_key]
            
            # State key varsa False yap (Modalı kapat)
            if state_key and state_key in st.session_state:
                st.session_state[state_key] = False
                
            st.success("🎉 Harika bir sohbetti!")
            st.rerun()  # Modal kapanacak
    
    with col2:
        if st.button("🔄 Yeniden Başla", use_container_width=True):
            del st.session_state[chat_key]
            st.rerun()  # Yeniden başlat
    
    with col3:
        # Mesaj sayısı
        msg_count = len([m for m in st.session_state[chat_key] if m["role"] == "user"])
        st.metric("💬", msg_count)


def generate_greeting(context: Dict) -> Dict:
    """
    Karşılama mesajı oluştur (JSON formatında).
    
    Args:
        context: Soru bağlamı
        
    Returns:
        JSON formatında karşılama mesajı
    """
    konu = context.get('konu', 'bu konu')
    zorluk = context.get('zorluk', 'Orta')
    
    greetings = [
        f"Selam! 👋\n\nBu soruyu birlikte çözelim mi? **{konu}** konusunda sana yardımcı olacağım.\n\nHazırsan başlayalım! 🚀",
        f"Merhaba! 😊\n\n**{konu}** konusunda takıldın mı? Sorun değil, birlikte hallederiz!\n\nNe düşünüyorsun, nereden başlayalım?",
        f"Hey! 🌟\n\nBu soru **{zorluk}** seviyede ama sen yaparsın! **{konu}** konusunu birlikte inceleyelim.\n\nİlk adımı atmaya hazır mısın?"
    ]
    
    import random
    greeting_text = random.choice(greetings)
    
    # JSON formatında döndür
    return {
        "ui_mode": "dialog",
        "content": {
            "message_text": greeting_text,
            "voice_tone": "friendly"
        },
        "visual_aid": {
            "required": False
        },
        "interaction": {
            "suggested_options": []
        },
        "gamification": {
            "xp_award": 0,
            "streak_bonus": False
        }
    }


def handle_user_input(user_input: str, chat_key: str, context: Dict):
    """
    Kullanıcı girişini işle ve AI yanıtı al (JSON Tabanlı).
    
    Args:
        user_input: Kullanıcı mesajı
        chat_key: Chat session key
        context: Soru bağlamı
    """
    # Kullanıcı mesajını ekle
    st.session_state[chat_key].append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # AI yanıtı al (JSON formatında) - Spinner ile
    with st.spinner("Düşünüyorum... 🤔"):
        sm = get_socratic_manager()
        json_response = sm.get_socratic_response(
            user_input,
            context,
            st.session_state[chat_key]
        )
    
    # JSON yanıt kontrolü
    if not json_response or not isinstance(json_response, dict):
        st.error("AI'dan geçerli bir yanıt alınamadı")
        return
    
    # UI mode'a göre işle
    ui_mode = json_response.get('ui_mode', 'dialog')
    
    if ui_mode == 'flashcard_session':
        # Flashcard moduna geç
        flashcards = json_response.get('learning_artifacts', {}).get('flashcards', [])
        if flashcards:
            st.session_state[f"{chat_key}_flashcards"] = flashcards
            st.session_state[f"{chat_key}_mode"] = 'flashcard'
    
    # Ana mesajı kaydet
    content = json_response.get('content', {})
    message_text = content.get('message_text', 'Yanıt alınamadı')
    
    st.session_state[chat_key].append({
        "role": "assistant",
        "content": message_text,
        "json_data": json_response,  # Tam JSON'u sakla
        "timestamp": datetime.now().isoformat()
    })
    
    # Otomatik okuma isteği (State'e kaydet)
    if st.session_state.get(f"auto_speak_{chat_key}", False):
        try:
            from utils.audio_service import get_audio_service
            audio_svc = get_audio_service()
            audio_data = audio_svc.speak_text(message_text)
            if audio_data:
                st.session_state[f"{chat_key}_autoplay_audio"] = audio_data
        except Exception as e:
            print(f"Auto speak error: {e}")
    
    # Doğru cevap kontrolü
    if check_if_correct_answer(user_input, context):
        st.balloons()
        
        # XP Ver (Sadece bir kere verilmeli, bu yüzden key kontrolü yap)
        reward_key = f"{chat_key}_reward_given"
        if not st.session_state.get(reward_key, False):
            from utils.gamification import get_gamification_manager
            gm = get_gamification_manager()
            gm.add_xp(25, "Doğru cevabı buldun! 🌟")
            st.session_state[reward_key] = True
        
        st.session_state[chat_key].append({
            "role": "assistant",
            "content": "🎉 **Mükemmel!** Doğru cevabı buldun! Harika bir iş çıkardın! 🌟",
            "timestamp": datetime.now().isoformat()
        })
        
    # UI'ı güncellemek için yeniden başlat
    st.rerun()


def get_socratic_response(
    user_message: str,
    chat_history: List[Dict],
    context: Dict
) -> str:
    """
    Sokratik öğretim yanıtı al.
    
    Args:
        user_message: Kullanıcı mesajı
        chat_history: Chat geçmişi
        context: Soru bağlamı
        
    Returns:
        AI yanıtı
    """
    gemini_key = None
    try:
        import json
        import os
        config_path = "config/user_settings.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                settings = json.load(f)
                gemini_key = settings.get("chat_api_key")
    except:
        pass

    # Gemini helper'ı (varsa) özel key ile başlat
    gemini = get_gemini_helper(api_key=gemini_key)
    
    # Sistem promptu oluştur
    system_prompt = f"""
    {SOCRATIC_TUTOR_PROMPT}
    
    SORU BAĞLAMI:
    Konu: {context.get('konu', 'Bilinmiyor')}
    Zorluk: {context.get('zorluk', 'Orta')}
    Doğru Cevap: {context.get('dogru_cevap', 'Bilinmiyor')} (Bunu öğrenciye söyleme!)
    
    SORU METNİ:
    {context.get('soru_metni', 'Metin yok')}
    
    ÇÖZÜM ADIMLARI (Referans için):
    {context.get('cozum_adimlari', [])}
    
    CHAT GEÇMİŞİ:
    {format_chat_history(chat_history[-5:])}  # Son 5 mesaj
    
    ÖĞRENCİ MESAJI: {user_message}
    
    ÖNEMLİ: 
    - Maksimum 2-3 cümle yaz
    - Bir emoji kullan
    - Soru sor, cevap verme
    - Pozitif ve destekleyici ol
    """
    
    # Yanıt al (streaming olmadan, modal içinde sorun çıkarabilir)
    response = gemini.chat(
        system_prompt,
        model_type="flash",
        stream=False
    )
    
    return response


def format_chat_history(history: List[Dict]) -> str:
    """Chat geçmişini formatla."""
    formatted = []
    for msg in history:
        role = "Öğrenci" if msg["role"] == "user" else "Öğretmen"
        formatted.append(f"{role}: {msg['content']}")
    return "\\n".join(formatted)


def check_if_correct_answer(user_input: str, context: Dict) -> bool:
    """
    Kullanıcının doğru cevabı bulup bulmadığını kontrol et.
    
    Args:
        user_input: Kullanıcı girişi
        context: Soru bağlamı
        
    Returns:
        True ise doğru cevap
    """
    dogru_cevap = str(context.get('dogru_cevap', '')).lower().strip()
    user_input_clean = user_input.lower().strip()
    
    import re
    
    # Şık kontrolü (A, B, C, D)
    if len(dogru_cevap) == 1 and dogru_cevap.isalpha():
        # Regex ile tam kelime eşleşmesi ara (örn: "A", "A.", "Cevap A", "A şıkkı")
        # \\b sınır belirteci, harfin tek başına veya kelime sınırında olmasını sağlar
        pattern = f"\\b{dogru_cevap}\\b"
        if re.search(pattern, user_input_clean):
            return True
            
    # Eğer cevap metin ise (örn: "12")
    elif dogru_cevap in user_input_clean:
        # Yine de çok kısa cevaplar için dikkatli ol
        if len(dogru_cevap) > 1:
            return True
            
    return False


def get_conversation_summary(chat_history: List[Dict]) -> Dict:
    """
    Sohbet özetini çıkar.
    
    Args:
        chat_history: Chat geçmişi
        
    Returns:
        Özet dictionary
    """
    user_messages = [m for m in chat_history if m["role"] == "user"]
    assistant_messages = [m for m in chat_history if m["role"] == "assistant"]
    
    return {
        "total_messages": len(chat_history),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages),
        "duration": calculate_duration(chat_history),
        "topics_discussed": extract_topics(chat_history)
    }


def calculate_duration(chat_history: List[Dict]) -> str:
    """Sohbet süresini hesapla."""
    if len(chat_history) < 2:
        return "0 dakika"
    
    from datetime import datetime
    
    start = datetime.fromisoformat(chat_history[0]["timestamp"])
    end = datetime.fromisoformat(chat_history[-1]["timestamp"])
    
    duration = (end - start).total_seconds() / 60
    return f"{int(duration)} dakika"


def extract_topics(chat_history: List[Dict]) -> List[str]:
    """Konuşulan konuları çıkar (basit keyword extraction)."""
    # Bu basitleştirilmiş bir versiyon
    # Gerçek uygulamada NLP kullanılabilir
    keywords = []
    for msg in chat_history:
        content = msg["content"].lower()
        # Basit keyword'ler
        if "mevsim" in content:
            keywords.append("Mevsimler")
        if "yarım küre" in content:
            keywords.append("Yarım Küreler")
        if "gündönümü" in content:
            keywords.append("Gündönümü")
    
    return list(set(keywords))


def render_socratic_inline(context: Dict, state_key: str = "socratic_inline", learning_context: str = "") -> bool:
    """
    Sokratik öğretim için inline (non-modal) chat penceresi.
    
    Args:
        context: Soru bağlamı
        state_key: Session key
        learning_context: PDF'ten gelen içerik özeti (Summary/Strategy/Mistakes)
    """
    # Chat geçmişini başlat
    chat_key = f"inline_chat_{state_key}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        # İlk karşılama mesajı
        greeting = _get_inline_greeting(context)
        st.session_state[chat_key].append({
            "role": "assistant",
            "content": greeting,
            "timestamp": datetime.now().isoformat()
        })
    
    # Chat container
    with st.container(border=True):
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 0.8rem; border-radius: 8px; margin-bottom: 1rem;'>
            <span style='color: white; font-weight: bold;'>
                🎓 {context.get('subtopic', 'Konu')} - Sokratik Tutör
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Mesaj geçmişi göster
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])
        
        # Seans tamamlandı mı kontrol
        completed_key = f"completed_{state_key}"
        if st.session_state.get(completed_key, False):
            st.success("✅ Seans tamamlandı! Harika iş çıkardın!")
            if st.button("🔄 Yeni Seans", key=f"restart_{state_key}"):
                del st.session_state[chat_key]
                del st.session_state[completed_key]
                st.rerun()
            return True
        
        # Kullanıcı girişi
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.chat_input(f"{context.get('subtopic', 'Konu')} hakkında soru sor...", key=f"input_{state_key}")
        with col2:
            if st.button("✅ Bitir", key=f"done_{state_key}"):
                st.session_state[completed_key] = True
                st.rerun()
                return True
        
        if user_input:
            # Kullanıcı mesajını ekle
            st.session_state[chat_key].append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })
            
            # AI yanıtı al
            with st.spinner("Düşünüyorum..."):
                response = _get_inline_response(user_input, st.session_state[chat_key], context, learning_context)
                st.session_state[chat_key].append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
            
            st.rerun()
    
    return False


def _get_inline_greeting(context: Dict) -> str:
    """Inline tutör için karşılama mesajı."""
    subtopic = context.get('subtopic', 'bu konu')
    return f"""Merhaba! 👋 

Ben senin Sokratik tutörünüm. **{subtopic}** konusunda sana yardımcı olacağım.

Cevapları doğrudan vermeyeceğim, sorularla seni doğru cevaba yönlendireceğim.

**Hazırsan takıldığın yeri sor veya 'Konuyu anlat' de!**"""


def _get_inline_response(user_input: str, chat_history: List[Dict], context: Dict, learning_context: str = "") -> str:
    """Inline tutör için AI yanıtı."""
    from utils.llm_adapter import get_llm_adapter
    from components.socratic_chat import SOCRATIC_TUTOR_PROMPT
    
    lesson = context.get('lesson', 'Genel')
    topic = context.get('topic', 'Genel')
    subtopic = context.get('subtopic', 'Genel')
    
    # Learning Context varsa prompta ekle
    context_injection = ""
    if learning_context:
        context_injection = f"""
        ÖĞRENME İÇERİĞİ (PDF ÖZETİ):
        Bu bilgileri öğrenciye öğretirken referans al, ancak doğrudan kopyalayıp yapıştırma.
        {learning_context}
        """
    
    # System prompt
    system_prompt = f"""{SOCRATIC_TUTOR_PROMPT}

ŞU AN ÖĞRETTİĞİN KONU:
- Ders: {lesson}
- Konu: {topic}  
- Alt Konu: {subtopic}

{context_injection}

ÖNCEKİ KONUŞMA:
{format_chat_history(chat_history[-6:])}

GÖREV: Öğrencinin mesajına Sokratik yöntemle (soru sorarak) yanıt ver.
"""
    
    try:
        llm = get_llm_adapter()
        response = llm.generate(user_input, system_prompt=system_prompt)
        return response
    except Exception as e:
        return f"Bir hata oluştu: {str(e)}. Lütfen tekrar dene."

