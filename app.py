"""
LGS-Zeka Platform - Ana Uygulama
AI destekli LGS hazırlık ve deneme takip sistemi
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path

# Proje kök dizinini Python path'e ekle
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Gamification sistemi
from utils.gamification import get_gamification_manager
from utils.config_manager import get_config_manager
from utils.event_logger import get_event_logger

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="LGS-Zeka | AI Destekli LGS Hazırlık Platformu",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/lgs-zeka',
        'Report a bug': "https://github.com/your-repo/lgs-zeka/issues",
        'About': "# LGS-Zeka\nAI destekli LGS hazırlık platformu"
    }
)

# Custom CSS
def load_custom_css():
    """Özel CSS stillerini yükler."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Genel Tipografi */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: #2B2D42;
        }
        
        /* Ana container */
        .main {
            padding: 0rem 1rem;
            background-color: #FAFAFB;
        }
        
        /* Başlıklar */
        h1 {
            color: #2E86AB; /* Derin Okyanus */
            font-weight: 700;
        }
        
        h2 {
            color: #F25F5C; /* Soft Mercan */
            font-weight: 600;
        }
        
        h3 {
            color: #2E86AB;
            font-weight: 500;
        }
        
        /* Metrikler */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #2E86AB;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #EFEFEF;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }
        
        /* Primary Butonlar */
        .stButton>button {
            background-color: #F25F5C;
            color: white;
            border-radius: 12px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 6px rgba(242, 95, 92, 0.2);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #D1495B;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(242, 95, 92, 0.3);
        }
        
        /* Secondary/Ghost Butonlar (Varsayılan Streamlit butonları) */
        button[kind="secondary"] {
            background-color: transparent;
            border: 2px solid #E0E0E0;
            color: #6C757D;
        }
        
        /* Kartlar (Card Design) */
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            border: 1px solid #F0F0F0;
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        }
        
        /* Expander Özelleştirme */
        .streamlit-expanderHeader {
            background-color: #F8F9FA;
            border-radius: 8px;
            color: #2B2D42;
            font-weight: 500;
        }
        
        /* Başarı mesajları */
        .success-message {
            background-color: #E3F2EF;
            color: #2D6A4F;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #70C1B3;
        }
        
        /* Uyarı mesajları */
        .warning-message {
            background-color: #FFF9E6;
            color: #856404;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #FFE066;
        }
        
        /* Tab Tasarımı */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 600;
            color: #8D99AE;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: transparent;
            color: #2E86AB;
            border-bottom: 2px solid #2E86AB;
        }
        </style>
    """, unsafe_allow_html=True)


def show_welcome_page():
    """Hoş geldiniz sayfasını gösterir."""
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3rem; margin-bottom: 1rem;'>
                🎓 LGS-Zeka'ya Hoş Geldiniz!
            </h1>
            <p style='font-size: 1.2rem; color: #6C757D; margin-bottom: 2rem;'>
                AI destekli LGS hazırlık platformunuz
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Özellikler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='card' style='text-align: center;'>
                <h2>📊 Akıllı Analiz</h2>
                <p>Deneme sonuçlarınızı detaylı analiz edin, 
                güçlü ve zayıf yönlerinizi keşfedin.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='card' style='text-align: center;'>
                <h2>🤖 AI Koç</h2>
                <p>Kişiselleştirilmiş çalışma önerileri ve 
                motivasyon desteği alın.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='card' style='text-align: center;'>
                <h2>🔍 Soru Analizi</h2>
                <p>Yapamadığınız soruları AI ile analiz edin, 
                çözüm adımlarını öğrenin.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Başlangıç bilgileri
    st.info("""
        👈 **Başlamak için** sol menüden bir sayfa seçin:
        
        - **📊 Dashboard**: Genel performans analizi ve grafikler
        - **🤖 AI Koç**: Kişiselleştirilmiş çalışma koçu
        - **🔍 Soru Analizi**: Soru görseli yükleyip AI analizi alın
    """)
    
    # İstatistikler (örnek)
    st.markdown("### 📈 Platform İstatistikleri")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Öğrenci", "1,234", "+12%")
    with col2:
        st.metric("Analiz Edilen Soru", "45,678", "+23%")
    with col3:
        st.metric("Ortalama Net Artışı", "+15.3", "+2.1")
    with col4:
        st.metric("Başarı Oranı", "%87", "+5%")


def main():
    """Ana uygulama fonksiyonu."""
    
    # Custom CSS yükle
    load_custom_css()
    
    # Gamification manager başlat
    gm = get_gamification_manager()
    gm.update_streak()
    
    # Diğer manager'ları başlat
    from utils.mastery_manager import get_mastery_manager
    get_mastery_manager()
    
    from utils.open_loop_manager import get_open_loop_manager
    get_open_loop_manager()
    
    # Config ve Logger başlat
    config = get_config_manager()
    logger = get_event_logger()
    
    # Uygulama başlangıcını logla
    if 'app_started' not in st.session_state:
        logger.log_event("app_start", "current_user")
        st.session_state.app_started = True
    
    # Navigasyon yönlendirmesi (Sayfalar arası geçiş için)
    if 'redirect_to' in st.session_state:
        # Widget oluşturulmadan önce state'i güncelle
        st.session_state['main_menu'] = st.session_state['redirect_to']
        del st.session_state['redirect_to']
    
    # Menü seçeneklerini flaglere göre belirle
    menu_options = ["Ana Sayfa"]
    menu_icons = ["house"]
    
    if config.get_feature("enable_mini_exam", True):
        menu_options.append("Mini Deneme")
        menu_icons.append("pencil-square")
    
    if config.get_feature("enable_learning_mode"):
        menu_options.append("Öğren")
        menu_icons.append("book")
        
    if config.get_feature("enable_dashboard"):
        menu_options.append("Dashboard")
        menu_icons.append("graph-up")
        
    if config.get_feature("enable_ai_coach"):
        menu_options.append("AI Koç")
        menu_icons.append("robot")
        
    if config.get_feature("enable_question_analysis"):
        menu_options.append("Soru Analizi")
        menu_icons.append("search")
        
    if config.get_feature("enable_admin_panel", False):
        menu_options.append("Admin PDF")
        menu_icons.append("file-earmark-pdf")
    
    menu_options.append("Ayarlar")
    menu_icons.append("gear")
    
    # Sidebar navigasyon
    with st.sidebar:
        # Navigasyon menüsü (En üstte)
        # Navigasyon menüsü (En üstte)
        selected = option_menu(
            menu_title="Menü",
            options=menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
            key="main_menu",  # Programatik navigasyon için key ekledik
            styles={
                "container": {"padding": "0!important", "background-color": "#F8F9FA"},
                "icon": {"color": "#FF6B6B", "font-size": "1.2rem"},
                "nav-link": {
                    "font-size": "1rem",
                    "text-align": "left",
                    "margin": "0.2rem 0",
                    "padding": "0.8rem 1rem",
                    "--hover-color": "#E9ECEF",
                },
                "nav-link-selected": {
                    "background-color": "#FF6B6B",
                    "color": "white",
                    "font-weight": "600",
                },
            },
        )
        
        # Gamification stats (Menü altında)
        gm.render_sidebar_stats()
        
        # Açık Döngüler Panosu
        from utils.open_loop_manager import render_open_loops_sidebar
        render_open_loops_sidebar()
        
        st.markdown("---")
        # Kullanıcı bilgisi ve Hızlı Bakış (Expander içinde)
        with st.expander("👤 Profil ve İstatistikler", expanded=False):
            # Dinamik veri çekme
            from utils.db_manager import get_db_manager
            db = get_db_manager()
            user = db.get_current_user()
            user_name = user.get('name', 'Öğrenci')
            target_score = float(user.get('target_score', 450) or 450)
            
            # Son sınav sonucu
            exams_df = db.fetch_data("exams")
            if not exams_df.empty and 'score' in exams_df.columns:
                exams_df = exams_df.sort_values('exam_date', ascending=False) if 'exam_date' in exams_df.columns else exams_df
                last_score = float(exams_df.iloc[0]['score']) if len(exams_df) > 0 else 0.0
                prev_score = float(exams_df.iloc[1]['score']) if len(exams_df) > 1 else last_score
                score_delta = last_score - prev_score
                distance_to_target = target_score - last_score
            else:
                last_score = 0.0
                score_delta = 0.0
                distance_to_target = target_score
            
            st.markdown(f"""
                <div style='padding: 0.5rem; background-color: white; border-radius: 8px; margin-bottom: 1rem;'>
                    <p style='margin: 0; font-weight: 600;'>{user_name}</p>
                    <p style='margin: 0; color: #6C757D; font-size: 0.85rem;'>🎯 Hedef: {target_score} puan</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.metric("Son Deneme", f"{last_score:.1f}", f"{score_delta:+.1f}" if score_delta != 0 else None)
            st.metric("Hedef Mesafe", f"{distance_to_target:.0f}", f"{-score_delta:+.1f}" if score_delta != 0 else None)
    
    # Sayfa yönlendirme
    if selected == "Ana Sayfa":
        # show_welcome_page() yerine direkt Bugün içeriği
        try:
            from pages import bugun
            bugun.show()
        except ImportError as e:
            st.error(f"Sayfa yüklenemedi: {e}")
        
    elif selected == "Mini Deneme":
        try:
            from pages import mini_deneme
            mini_deneme.show()
        except ImportError as e:
            st.error(f"Sayfa yüklenemedi: {e}")

    elif selected == "Öğren":
        try:
            from pages import ogren
            ogren.show()
        except ImportError as e:
            st.error(f"Sayfa yüklenemedi: {e}")
    
    elif selected == "Dashboard":
        try:
            from pages import dashboard
            dashboard.show()
        except ImportError as e:
            st.error(f"Dashboard sayfası yüklenemedi: {e}")
    
    elif selected == "AI Koç":
        try:
            from pages import ai_koc
            ai_koc.show()
        except ImportError:
            st.warning("🤖 AI Koç sayfası henüz hazırlanıyor...")
            st.info("Bu sayfa Faz 4'te geliştirilecektir.")
    
    elif selected == "Soru Analizi":
        try:
            from pages import soru_analiz
            soru_analiz.show()
        except ImportError:
            st.warning("🔍 Soru Analizi sayfası henüz hazırlanıyor...")
            st.info("Bu sayfa Faz 2'de geliştirilecektir.")
    
    elif selected == "Admin PDF":
        try:
            from pages import admin_pdf
            admin_pdf.show()
        except ImportError as e:
            st.error(f"Admin sayfası yüklenemedi: {e}")

    elif selected == "Ayarlar":
        try:
            from pages import ayarlar
            ayarlar.show()
        except ImportError as e:
            st.error(f"Ayarlar sayfası yüklenemedi: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div class='footer'>
            <p>© 2024 LGS-Zeka | AI Destekli LGS Hazırlık Platformu</p>
            <p style='font-size: 0.8rem;'>
                Powered by Streamlit & Google Gemini AI
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
