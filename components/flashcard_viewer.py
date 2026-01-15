"""
Flashcard Viewer Component
Bilgi kartları gösterimi ve etkileşimi
"""

import streamlit as st
from typing import List, Dict
from datetime import datetime


def show_flashcard_session(flashcards: List[Dict[str, str]], topic: str = ""):
    """
    Flashcard oturumu göster.
    
    Args:
        flashcards: [{"front": "Soru", "back": "Cevap"}, ...]
        topic: Konu başlığı
    """
    if not flashcards:
        st.info("Bu konu için henüz bilgi kartı oluşturulmadı.")
        return
    
    # Session state başlatma
    if 'flashcard_index' not in st.session_state:
        st.session_state.flashcard_index = 0
    if 'flashcard_flipped' not in st.session_state:
        st.session_state.flashcard_flipped = False
    if 'flashcard_stats' not in st.session_state:
        st.session_state.flashcard_stats = {
            'total': len(flashcards),
            'reviewed': 0,
            'known': 0,
            'learning': 0
        }
    
    # Başlık
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: #667eea;'>🎴 Bilgi Kartları</h2>
        {f"<p style='color: #6C757D;'>{topic}</p>" if topic else ""}
    </div>
    """, unsafe_allow_html=True)
    
    # İlerleme
    current_index = st.session_state.flashcard_index
    total = len(flashcards)
    
    progress = (current_index + 1) / total
    st.progress(progress, text=f"Kart {current_index + 1} / {total}")
    
    # Mevcut kart
    current_card = flashcards[current_index]
    
    # Kart gösterimi
    render_flashcard(
        current_card,
        st.session_state.flashcard_flipped
    )
    
    # Kontrol butonları
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_index > 0:
            if st.button("⬅️ Önceki", use_container_width=True):
                st.session_state.flashcard_index -= 1
                st.session_state.flashcard_flipped = False
                st.rerun()
    
    with col2:
        if not st.session_state.flashcard_flipped:
            if st.button("🔄 Cevabı Göster", type="primary", use_container_width=True):
                st.session_state.flashcard_flipped = True
                st.rerun()
        else:
            # Bilgi durumu butonları
            st.markdown("**Bu kartı biliyor musun?**")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("✅ Biliyorum", use_container_width=True, type="primary"):
                    st.session_state.flashcard_stats['known'] += 1
                    st.session_state.flashcard_stats['reviewed'] += 1
                    next_card()
            
            with col_b:
                if st.button("📚 Öğreniyorum", use_container_width=True):
                    st.session_state.flashcard_stats['learning'] += 1
                    st.session_state.flashcard_stats['reviewed'] += 1
                    next_card()
    
    with col3:
        if current_index < total - 1:
            if st.button("Sonraki ➡️", use_container_width=True):
                next_card()
        else:
            if st.button("🏁 Bitir", use_container_width=True, type="primary"):
                show_flashcard_summary()
    
    # İstatistikler
    st.markdown("---")
    show_flashcard_stats()


def render_flashcard(card: Dict[str, str], flipped: bool):
    """
    Tek bir flashcard göster.
    
    Args:
        card: {"front": "Soru", "back": "Cevap"}
        flipped: Kartın arka yüzü gösteriliyor mu?
    """
    # 3D flip efekti için CSS
    st.markdown("""
    <style>
    .flashcard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        min-height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        color: white;
        font-size: 1.3rem;
        font-weight: 500;
        line-height: 1.6;
    }
    
    .flashcard:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    .flashcard-back {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
    }
    
    .flashcard-label {
        position: absolute;
        top: 1rem;
        left: 1.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not flipped:
        # Ön yüz (Soru)
        st.markdown(f"""
        <div class='flashcard' style='position: relative;'>
            <div class='flashcard-label'>❓ SORU</div>
            <div>{card.get('front', 'Soru yok')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Arka yüz (Cevap)
        st.markdown(f"""
        <div class='flashcard flashcard-back' style='position: relative;'>
            <div class='flashcard-label'>✅ CEVAP</div>
            <div>{card.get('back', 'Cevap yok')}</div>
        </div>
        """, unsafe_allow_html=True)


def next_card():
    """Sonraki karta geç."""
    st.session_state.flashcard_index += 1
    st.session_state.flashcard_flipped = False
    st.rerun()


def show_flashcard_stats():
    """Flashcard istatistikleri göster."""
    stats = st.session_state.flashcard_stats
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📚 Toplam", stats['total'])
    
    with col2:
        st.metric("✅ Biliyorum", stats['known'])
    
    with col3:
        st.metric("📖 Öğreniyorum", stats['learning'])


def show_flashcard_summary():
    """Oturum özeti göster."""
    stats = st.session_state.flashcard_stats
    
    # Başarı oranı
    if stats['reviewed'] > 0:
        success_rate = (stats['known'] / stats['reviewed']) * 100
    else:
        success_rate = 0
    
    st.balloons()
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    '>
        <h2 style='margin: 0; color: white;'>🎉 Tebrikler!</h2>
        <p style='margin: 1rem 0 0 0; font-size: 1.2rem;'>
            {stats['reviewed']} kartı tamamladın!
        </p>
        <p style='margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: bold;'>
            Başarı Oranı: %{int(success_rate)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # XP ver
    from utils.gamification import get_gamification_manager
    gm = get_gamification_manager()
    
    xp_earned = stats['reviewed'] * 10
    gm.add_xp(xp_earned, f"Bilgi kartları tamamlandı! 🎴")
    
    # Sıfırla butonu
    if st.button("🔄 Tekrar Başla", use_container_width=True):
        st.session_state.flashcard_index = 0
        st.session_state.flashcard_flipped = False
        st.session_state.flashcard_stats = {
            'total': stats['total'],
            'reviewed': 0,
            'known': 0,
            'learning': 0
        }
        st.rerun()


def create_flashcards_from_topic(topic: str, content: str) -> List[Dict[str, str]]:
    """
    Konu içeriğinden flashcard'lar oluştur.
    
    Args:
        topic: Konu başlığı
        content: Konu içeriği
        
    Returns:
        Flashcard listesi
    """
    # Bu fonksiyon AI ile flashcard üretebilir
    # Şimdilik basit bir örnek döndürelim
    
    return [
        {
            "front": f"{topic} konusunda önemli bir kavram nedir?",
            "back": "Bu konu için AI tarafından oluşturulacak..."
        }
    ]
