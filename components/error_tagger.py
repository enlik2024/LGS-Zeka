"""
Hata Etiketleme Komponenti
Öğrencilerin yaptığı hataları kategorize etme ve analiz etme
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional


# Hata kategorileri
ERROR_CATEGORIES = {
    "🧮 Hesap Hatası": {
        "description": "Matematiksel işlem yanlışı",
        "color": "#FF6B6B",
        "tips": [
            "İşlemleri adım adım yap",
            "Hesap makinesini kontrol et",
            "Sonucu tekrar hesapla"
        ]
    },
    "📖 Kavram Karışıklığı": {
        "description": "Temel kavramları karıştırma",
        "color": "#FFA500",
        "tips": [
            "Kavramları tekrar gözden geçir",
            "Örneklerle pekiştir",
            "Benzer kavramları karşılaştır"
        ]
    },
    "⏰ Zaman Yönetimi": {
        "description": "Soruyu çözememe (zaman)",
        "color": "#9B59B6",
        "tips": [
            "Kolay sorulardan başla",
            "Zaman sınırı koy",
            "Pratik yap"
        ]
    },
    "🎯 Dikkat Eksikliği": {
        "description": "Soruyu yanlış okuma",
        "color": "#3498DB",
        "tips": [
            "Soruyu iki kez oku",
            "Anahtar kelimeleri işaretle",
            "Sakin ol ve odaklan"
        ]
    },
    "📊 Grafik Okuma": {
        "description": "Grafik/tablo yorumlama hatası",
        "color": "#1ABC9C",
        "tips": [
            "Eksenleri kontrol et",
            "Birimi kontrol et",
            "Verileri dikkatlice oku"
        ]
    },
    "🔢 Birim Hatası": {
        "description": "Birim dönüşümü yanlışı",
        "color": "#E74C3C",
        "tips": [
            "Birimleri yaz",
            "Dönüşüm tablosunu kullan",
            "Sonucu kontrol et"
        ]
    },
    "📝 Formül Hatası": {
        "description": "Yanlış formül kullanma",
        "color": "#F39C12",
        "tips": [
            "Formülü ezberle",
            "Hangi durumda kullanılır öğren",
            "Örnek çöz"
        ]
    },
    "🤔 Mantık Hatası": {
        "description": "Mantıksal çıkarım yanlışı",
        "color": "#8E44AD",
        "tips": [
            "Adım adım düşün",
            "Sebep-sonuç ilişkisi kur",
            "Benzer örneklere bak"
        ]
    }
}


def show_error_tagger(question_id: str, question_context: Optional[Dict] = None):
    """
    Hata etiketleme arayüzü.
    
    Args:
        question_id: Soru ID'si
        question_context: Soru bağlamı (konu, zorluk, vb.)
    """
    st.markdown("### 🏷️ Hata Analizi")
    st.markdown("""
    <p style='color: #6C757D; font-size: 0.9rem;'>
        Bu soruyu yaparken hangi tür hata yaptın? 
        Hatalarını analiz etmek, gelişmene yardımcı olur! 💪
    </p>
    """, unsafe_allow_html=True)
    
    # Etiket seçimi
    selected_errors = st.pills(
        "Hata Türleri",
        options=list(ERROR_CATEGORIES.keys()),
        selection_mode="multi",
        key=f"error_tags_{question_id}",
        help="Birden fazla seçebilirsin"
    )
    
    # Seçilen hatalar için ipuçları göster
    if selected_errors:
        st.markdown("#### 💡 İpuçları")
        
        for error in selected_errors:
            error_data = ERROR_CATEGORIES[error]
            
            with st.expander(f"{error} - Nasıl Önlerim?"):
                st.markdown(f"**{error_data['description']}**")
                st.markdown("**Öneriler:**")
                for tip in error_data['tips']:
                    st.markdown(f"• {tip}")
        
        # Not ekleme
        error_note = st.text_area(
            "📝 Ek Not (Opsiyonel)",
            placeholder="Örn: Kök 2'yi yanlış hesapladım, formülü karıştırdım...",
            key=f"error_note_{question_id}",
            height=80
        )
        
        # Kaydet butonu
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("💾 Hata Analizini Kaydet", 
                        type="primary", 
                        use_container_width=True,
                        key=f"save_errors_{question_id}"):
                # Hataları kaydet
                save_error_tags(
                    question_id, 
                    selected_errors, 
                    error_note,
                    question_context
                )
                st.success("✅ Hata analizi kaydedildi!")
                
                # XP ver
                from utils.gamification import get_gamification_manager
                gm = get_gamification_manager()
                gm.add_xp(5, "Hata analizi yaptın! 🎯")
        
        with col2:
            if st.button("🔄 Temizle", key=f"clear_errors_{question_id}"):
                st.rerun()


def save_error_tags(
    question_id: str, 
    errors: List[str], 
    note: str = "",
    context: Optional[Dict] = None
):
    """
    Hata etiketlerini kaydet.
    
    Args:
        question_id: Soru ID'si
        errors: Seçilen hata kategorileri
        note: Kullanıcı notu
        context: Soru bağlamı
    """
    if 'error_history' not in st.session_state:
        st.session_state.error_history = []
    
    error_entry = {
        "question_id": question_id,
        "errors": errors,
        "note": note,
        "timestamp": datetime.now().isoformat(),
        "context": context or {}
    }
    
    st.session_state.error_history.append(error_entry)


def get_error_statistics() -> Dict:
    """
    Hata istatistiklerini hesapla.
    
    Returns:
        İstatistik dictionary'si
    """
    if 'error_history' not in st.session_state or not st.session_state.error_history:
        return {
            "total_errors": 0,
            "most_common": None,
            "by_category": {}
        }
    
    # Hata sayılarını hesapla
    error_counts = {}
    for entry in st.session_state.error_history:
        for error in entry['errors']:
            error_counts[error] = error_counts.get(error, 0) + 1
    
    # En yaygın hata
    most_common = max(error_counts.items(), key=lambda x: x[1]) if error_counts else None
    
    return {
        "total_errors": len(st.session_state.error_history),
        "most_common": most_common,
        "by_category": error_counts
    }


def render_error_statistics():
    """Hata istatistiklerini görselleştir."""
    stats = get_error_statistics()
    
    if stats['total_errors'] == 0:
        st.info("📊 Henüz hata analizi yok. İlk analizini yap!")
        return
    
    st.markdown("### 📊 Hata Analizi İstatistikleri")
    
    # Özet metrikler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Toplam Analiz", stats['total_errors'])
    
    with col2:
        if stats['most_common']:
            st.metric("En Yaygın Hata", stats['most_common'][0].split()[1])
    
    with col3:
        unique_errors = len(stats['by_category'])
        st.metric("Farklı Hata Türü", unique_errors)
    
    # Kategori bazlı grafik
    if stats['by_category']:
        st.markdown("#### Hata Dağılımı")
        
        import plotly.graph_objects as go
        
        # Verileri hazırla
        categories = list(stats['by_category'].keys())
        counts = list(stats['by_category'].values())
        colors = [ERROR_CATEGORIES[cat]['color'] for cat in categories]
        
        # Bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=counts,
                marker_color=colors,
                text=counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis_title="Hata Türü",
            yaxis_title="Sayı",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Öneriler
        if stats['most_common']:
            most_common_error = stats['most_common'][0]
            error_data = ERROR_CATEGORIES[most_common_error]
            
            st.markdown(f"""
            <div style='
                background-color: {error_data['color']}20;
                border-left: 4px solid {error_data['color']};
                padding: 1rem;
                border-radius: 5px;
                margin: 1rem 0;
            '>
                <h4 style='margin: 0;'>💡 En Çok Yaptığın Hata: {most_common_error}</h4>
                <p style='margin: 0.5rem 0 0 0;'>{error_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Bu hatayı önlemek için:**")
            for tip in error_data['tips']:
                st.markdown(f"• {tip}")


def get_error_insights(subject: Optional[str] = None) -> Dict:
    """
    Ders bazlı hata içgörüleri.
    
    Args:
        subject: Ders adı (None ise tüm dersler)
        
    Returns:
        İçgörü dictionary'si
    """
    if 'error_history' not in st.session_state:
        return {}
    
    # Ders filtreleme
    filtered_errors = st.session_state.error_history
    if subject:
        filtered_errors = [
            e for e in filtered_errors 
            if e.get('context', {}).get('konu', '').startswith(subject)
        ]
    
    if not filtered_errors:
        return {}
    
    # Analiz
    error_counts = {}
    for entry in filtered_errors:
        for error in entry['errors']:
            error_counts[error] = error_counts.get(error, 0) + 1
    
    # En yaygın 3 hata
    top_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "total": len(filtered_errors),
        "top_errors": top_errors,
        "improvement_areas": [error[0] for error in top_errors]
    }


def export_error_history() -> str:
    """
    Hata geçmişini CSV formatında export et.
    
    Returns:
        CSV string
    """
    if 'error_history' not in st.session_state:
        return ""
    
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Tarih', 'Soru ID', 'Hata Türleri', 'Not', 'Konu'])
    
    # Data
    for entry in st.session_state.error_history:
        writer.writerow([
            entry['timestamp'],
            entry['question_id'],
            ', '.join(entry['errors']),
            entry['note'],
            entry.get('context', {}).get('konu', '')
        ])
    
    return output.getvalue()
