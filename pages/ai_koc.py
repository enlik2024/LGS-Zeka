"""
AI Koç Sayfası
Kişiselleştirilmiş AI destekli LGS koçu ve motivasyon desteği
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from utils.gemini_helper import get_gemini_helper
from utils.db_manager import get_db_manager
from utils.scoring import get_lgs_scoring
from utils.event_logger import get_event_logger


def show():
    """AI Koç sayfasını gösterir."""
    
    # Sayfa başlığı
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #FF6B6B;'>🤖 Sanal LGS Koçu</h1>
            <p style='color: #6C757D; font-size: 1.1rem;'>
                Kişiselleştirilmiş AI desteği ile LGS yolculuğunuzda yanınızdayım
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Session state başlatma
    initialize_session_state()
    
    # Sidebar - Koç ayarları
    with st.sidebar:
        show_coach_settings()
    
    # Öğrenci bağlamını yükle
    student_context = load_student_context()
    
    # Ana içerik - 2 sütun
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat arayüzü
        show_chat_interface(student_context)
    
    with col2:
        # Öğrenci profili ve öneriler
        show_student_profile(student_context)
    
    # Hızlı eylemler
    st.markdown("---")
    show_quick_actions(student_context)


def initialize_session_state():
    """Session state değişkenlerini başlatır."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'coach_personality' not in st.session_state:
        st.session_state.coach_personality = "Destekleyici"
    
    if 'show_context' not in st.session_state:
        st.session_state.show_context = True
    
    if 'chat_model' not in st.session_state:
        st.session_state.chat_model = "flash"


def show_coach_settings():
    """Koç ayarlarını gösterir."""
    st.markdown("### ⚙️ Koç Ayarları")
    
    # Koç kişiliği
    personality = st.selectbox(
        "Koç Kişiliği",
        options=["Destekleyici", "Motive Edici", "Analitik", "Arkadaş Canlısı"],
        index=["Destekleyici", "Motive Edici", "Analitik", "Arkadaş Canlısı"].index(
            st.session_state.coach_personality
        ),
        help="AI koçunuzun konuşma tarzını belirler"
    )
    st.session_state.coach_personality = personality
    
    # Model seçimi
    model = st.radio(
        "AI Model",
        options=["flash", "pro"],
        format_func=lambda x: "⚡ Flash (Hızlı)" if x == "flash" else "🎯 Pro (Detaylı)",
        index=0 if st.session_state.chat_model == "flash" else 1
    )
    st.session_state.chat_model = model
    
    # Bağlam gösterimi
    show_context = st.checkbox(
        "Öğrenci bağlamını kullan",
        value=st.session_state.show_context,
        help="AI'nın performansınızı bilmesini sağlar"
    )
    st.session_state.show_context = show_context
    
    st.markdown("---")
    
    # Chat geçmişi yönetimi
    st.markdown("### 💬 Geçmiş")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Temizle", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        message_count = len(st.session_state.chat_history)
        st.metric("Mesaj", message_count)
    
    st.markdown("---")
    
    # Hızlı istatistikler
    st.markdown("### 📊 Özet")
    
    try:
        db = get_db_manager()
        df = db.fetch_data("deneme_sonuclari")
        
        if not df.empty:
            scoring = get_lgs_scoring()
            result = scoring.calculate_from_dataframe(df)
            
            st.metric("LGS Puanı", f"{result['lgs_puani']:.0f}")
            st.metric("Toplam Net", f"{result['toplam_net']:.1f}")
            
            if result['en_zayif_ders']:
                st.warning(f"📚 Geliştirilmeli: {result['en_zayif_ders']}")
    except:
        pass


def load_student_context() -> Dict[str, Any]:
    """Öğrenci bağlamını yükler."""
    context = {
        "loaded": False,
        "lgs_puani": 0,
        "toplam_net": 0,
        "en_iyi_ders": None,
        "en_zayif_ders": None,
        "zayif_konular": [],
        "son_denemeler": [],
        "hedef_puan": 450
    }
    
    if not st.session_state.show_context:
        return context
    
    try:
        # Veritabanından veri çek
        db = get_db_manager()
        df = db.fetch_data("deneme_sonuclari")
        
        if df.empty:
            return context
        
        # Puanlama hesapla
        scoring = get_lgs_scoring()
        result = scoring.calculate_from_dataframe(df)
        
        context.update({
            "loaded": True,
            "lgs_puani": result['lgs_puani'],
            "toplam_net": result['toplam_net'],
            "ortalama_net": result['ortalama_net'],
            "en_iyi_ders": result['en_iyi_ders'],
            "en_zayif_ders": result['en_zayif_ders'],
            "toplam_deneme": result['toplam_deneme'],
            "ders_netleri": result['ders_netleri']
        })
        
        # Zayıf konular (en çok yanlış yapılan)
        if 'Konu' in df.columns and 'Yanlis' in df.columns:
            zayif_konular = df.groupby('Konu')['Yanlis'].sum().nlargest(5)
            context['zayif_konular'] = zayif_konular.index.tolist()
        
        # Son 5 deneme
        if 'Tarih' in df.columns:
            son_denemeler = df.groupby('Tarih')['Net'].sum().tail(5)
            context['son_denemeler'] = son_denemeler.tolist()
        
        return context
        
    except Exception as e:
        st.error(f"Bağlam yüklenemedi: {str(e)}")
        return context


def build_system_prompt(personality: str, context: Dict[str, Any]) -> str:
    """Sistem promptunu oluşturur."""
    
    # Kişilik tanımları
    personalities = {
        "Destekleyici": """Sen destekleyici ve anlayışlı bir LGS koçusun. 
        Öğrencilere sabırlı yaklaşır, zorluklarını anlar ve çözüm odaklı öneriler sunarsın.
        Her zaman pozitif bir dil kullanır, motivasyonlarını yüksek tutarsın.""",
        
        "Motive Edici": """Sen enerjik ve motive edici bir LGS koçusun.
        Öğrencileri hedeflerine ulaşmaları için sürekli cesaretlendirir, başarı hikayelerinden örnekler verirsin.
        Coşkulu bir dil kullanır, her küçük ilerlemeyi kutlarsın.""",
        
        "Analitik": """Sen analitik ve detay odaklı bir LGS koçusun.
        Verileri inceler, sayısal analizler yapar, somut öneriler sunarsın.
        Objektif bir dil kullanır, performans metriklerine odaklanırsın.""",
        
        "Arkadaş Canlısı": """Sen samimi ve arkadaş canlısı bir LGS koçusun.
        Öğrencilerle rahat bir dil kullanır, onları anlar, empati kurarsın.
        Sıcak ve içten bir üslup kullanır, güven verirsin."""
    }
    
    base_prompt = personalities.get(personality, personalities["Destekleyici"])
    
    # Bağlam ekleme
    if context['loaded']:
        context_info = f"""

ÖĞRENCİ BAĞLAMI:
- Tahmini LGS Puanı: {context['lgs_puani']:.0f}
- Toplam Net: {context['toplam_net']:.1f}
- Ortalama Net: {context.get('ortalama_net', 0):.1f}
- En İyi Ders: {context['en_iyi_ders']}
- Geliştirilmesi Gereken Ders: {context['en_zayif_ders']}
- Toplam Deneme: {context.get('toplam_deneme', 0)}
"""
        
        if context['zayif_konular']:
            context_info += f"\n- Zayıf Konular: {', '.join(context['zayif_konular'][:3])}"
        
        base_prompt += context_info
    
    base_prompt += """

GÖREVLER:
1. Öğrencinin sorularını yanıtla
2. Çalışma stratejileri öner
3. Motivasyon desteği sağla
4. Konu bazlı öneriler ver
5. Zaman yönetimi konusunda yardımcı ol

ÖNEMLİ:
- Kısa ve öz yanıtlar ver (max 3-4 paragraf)
- Emoji kullan ama aşırıya kaçma
- Öğrenciye "sen" diye hitap et
- Somut ve uygulanabilir öneriler sun
- Pozitif ve destekleyici ol
"""
    
    return base_prompt


def show_chat_interface(context: Dict[str, Any]):
    """Chat arayüzünü gösterir."""
    st.markdown("### 💬 Sohbet")
    
    # Chat geçmişini göster
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_history:
            # İlk karşılama mesajı
            with st.chat_message("assistant", avatar="🤖"):
                greeting = get_greeting_message(context)
                st.markdown(greeting)
        else:
            # Geçmiş mesajları göster
            for message in st.session_state.chat_history:
                avatar = "👤" if message["role"] == "user" else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input(
        "Mesajınızı yazın... (örn: 'Matematik çalışma planı öner')",
        key="chat_input"
    )
    
    if user_input:
        # Kullanıcı mesajını ekle
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # AI yanıtı al
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            
            try:
                # Log chat event
                logger = get_event_logger()
                logger.log_event("coach_chat", "current_user", {"message_len": len(user_input)})
                
                # Gemini helper
                gemini = get_gemini_helper()
                
                # System prompt
                system_prompt = build_system_prompt(
                    st.session_state.coach_personality,
                    context
                )
                
                # Chat geçmişini hazırla
                chat_context = {
                    "system_prompt": system_prompt,
                    "personality": st.session_state.coach_personality,
                    "student_data": context if context['loaded'] else None
                }
                
                # Streaming yanıt
                full_response = ""
                
                response_stream = gemini.chat(
                    user_input,
                    context=chat_context,
                    model_type=st.session_state.chat_model,
                    stream=True
                )
                
                # Stream'i göster
                for chunk in response_stream:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")
                
                # Final yanıt
                response_placeholder.markdown(full_response)
                
                # Yanıtı kaydet
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                error_msg = f"Üzgünüm, bir hata oluştu: {str(e)}"
                response_placeholder.error(error_msg)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().isoformat()
                })
        
        st.rerun()


def get_greeting_message(context: Dict[str, Any]) -> str:
    """Karşılama mesajını oluşturur."""
    
    if context['loaded']:
        greeting = f"""
Merhaba! 👋 Ben senin sanal LGS koçunum.

📊 **Durumun:**
- Tahmini LGS Puanın: **{context['lgs_puani']:.0f}**
- Toplam Net: **{context['toplam_net']:.1f}**
"""
        
        if context['en_iyi_ders']:
            greeting += f"- En İyi Dersin: **{context['en_iyi_ders']}** 💪\n"
        
        if context['en_zayif_ders']:
            greeting += f"- Geliştirilmesi Gereken: **{context['en_zayif_ders']}** 📚\n"
        
        greeting += """
Sana nasıl yardımcı olabilirim? Çalışma planı, motivasyon desteği, konu önerileri... Ne istersen! 🚀
"""
    else:
        greeting = """
Merhaba! 👋 Ben senin sanal LGS koçunum.

Sana LGS yolculuğunda yardımcı olmak için buradayım. Sorularını sorabilir, çalışma önerileri alabilir, motivasyon desteği isteyebilirsin.

Hadi başlayalım! 🚀
"""
    
    return greeting


def show_student_profile(context: Dict[str, Any]):
    """Öğrenci profilini gösterir."""
    st.markdown("### 👤 Profilim")
    
    if not context['loaded']:
        st.info("📭 Henüz deneme verisi yok. Dashboard'dan veri ekleyin.")
        return
    
    # Performans özeti
    with st.container():
        st.markdown("#### 📊 Performans")
        
        lgs_score = context['lgs_puani']
        scoring = get_lgs_scoring()
        level, color, emoji = scoring.get_performance_level(lgs_score)
        
        st.markdown(f"""
        <div style='
            background-color: {color}20;
            border-left: 4px solid {color};
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        '>
            <h3 style='margin: 0; color: {color};'>{emoji} {level}</h3>
            <p style='margin: 0.5rem 0 0 0;'>LGS Puanı: {lgs_score:.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Güçlü ve zayıf yönler
    st.markdown("#### 💪 Güçlü Yönler")
    if context['en_iyi_ders']:
        st.success(f"✓ {context['en_iyi_ders']}")
    
    st.markdown("#### 📚 Gelişim Alanları")
    if context['en_zayif_ders']:
        st.warning(f"→ {context['en_zayif_ders']}")
    
    if context['zayif_konular']:
        with st.expander("🔍 Zayıf Konular"):
            for konu in context['zayif_konular'][:5]:
                st.markdown(f"- {konu}")
    
    # Son performans
    if context['son_denemeler']:
        st.markdown("#### 📈 Son Denemeler")
        
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=context['son_denemeler'],
            mode='lines+markers',
            line=dict(color='#FF6B6B', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            height=150,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis=dict(title="Net"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)


def show_quick_actions(context: Dict[str, Any]):
    """Hızlı eylem butonlarını gösterir."""
    st.markdown("### ⚡ Hızlı Sorular")
    
    quick_questions = [
        "📚 Matematik için çalışma planı öner",
        "💪 Motivasyon desteği ver",
        "⏰ Zaman yönetimi önerileri",
        "🎯 Hedefime nasıl ulaşırım?",
        "📖 Kaynak önerileri",
        "🧠 Etkili çalışma teknikleri"
    ]
    
    # Bağlama göre özelleştirilmiş sorular
    if context['loaded'] and context['en_zayif_ders']:
        quick_questions.insert(0, f"📈 {context['en_zayif_ders']} nasıl geliştirebilirim?")
    
    # 3 sütun
    cols = st.columns(3)
    
    for i, question in enumerate(quick_questions[:6]):
        with cols[i % 3]:
            if st.button(question, use_container_width=True, key=f"quick_{i}"):
                # Soruyu chat'e ekle
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question.split(" ", 1)[1],  # Emoji'yi kaldır
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()


# Sayfa çağrıldığında
if __name__ == "__main__":
    show()
