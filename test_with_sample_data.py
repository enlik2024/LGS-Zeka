"""
Test Verisi ile Uygulama Başlatıcı
Google Sheets bağlantısı olmadan test etmek için
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Proje kök dizinini ekle
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))


def create_sample_data():
    """Örnek test verisi oluşturur."""
    
    # Örnek deneme sonuçları
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    dersler = ["Matematik", "Fen Bilimleri", "Türkçe", "Sosyal Bilgiler", "İngilizce"]
    konular = {
        "Matematik": ["Üslü İfadeler", "Köklü Sayılar", "Denklemler", "Olasılık"],
        "Fen Bilimleri": ["Kuvvet", "Basınç", "DNA", "Madde"],
        "Türkçe": ["Cümlede Anlam", "Yazım Kuralları", "Sözcükte Anlam"],
        "Sosyal Bilgiler": ["İlk Türk Devletleri", "Coğrafya"],
        "İngilizce": ["Tense-Yapılar", "Vocabulary"]
    }
    
    for i in range(40):
        ders = dersler[i % len(dersler)]
        konu = konular[ders][i % len(konular[ders])]
        
        dogru = 5 + (i % 15)
        yanlis = 0 + (i % 5)
        bos = 0 + (i % 3)
        net = dogru - (yanlis / 3.0)
        
        data.append({
            'Tarih': base_date + timedelta(days=i),
            'Ders': ders,
            'Konu': konu,
            'Dogru': dogru,
            'Yanlis': yanlis,
            'Bos': bos,
            'Net': round(net, 2),
            'Gorsel_URL': ''
        })
    
    return pd.DataFrame(data)


# Session state'e test verisi ekle
if 'test_data' not in st.session_state:
    st.session_state.test_data = create_sample_data()

# Ana uygulama
st.set_page_config(
    page_title="LGS-Zeka (Test Modu)",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 LGS-Zeka Platform (Test Modu)")
st.info("⚠️ Test modu: Örnek verilerle çalışıyor. Google Sheets bağlantısı gerekmiyor.")

# Menü
menu = st.sidebar.radio(
    "Menü",
    ["Ana Sayfa", "Dashboard", "Soru Analizi", "AI Koç"]
)

if menu == "Ana Sayfa":
    st.markdown("""
    ## 🎉 Hoş Geldiniz!
    
    Bu test modunda platformun tüm özelliklerini deneyebilirsiniz.
    
    ### ✅ Kullanılabilir Özellikler:
    - **Dashboard**: Performans analizi ve grafikler
    - **Soru Analizi**: AI destekli soru çözümü (Gemini API gerekli)
    - **AI Koç**: Kişiselleştirilmiş chatbot (Gemini API gerekli)
    
    ### 📊 Test Verisi:
    - 40 deneme sonucu
    - 5 farklı ders
    - Son 30 gün
    
    Sol menüden bir sayfa seçin!
    """)

elif menu == "Dashboard":
    st.markdown("## 📊 Dashboard")
    
    # Test verisini kullan
    df = st.session_state.test_data
    
    # Basit metrikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Net", f"{df['Net'].sum():.1f}")
    
    with col2:
        st.metric("Ortalama Net", f"{df['Net'].mean():.1f}")
    
    with col3:
        st.metric("Toplam Deneme", len(df['Tarih'].unique()))
    
    with col4:
        en_iyi = df.groupby('Ders')['Net'].sum().idxmax()
        st.metric("En İyi Ders", en_iyi)
    
    # Veri tablosu
    st.markdown("### 📋 Deneme Sonuçları")
    st.dataframe(df, use_container_width=True)
    
    # Basit grafik
    st.markdown("### 📈 Ders Bazlı Toplam Net")
    ders_net = df.groupby('Ders')['Net'].sum().sort_values(ascending=False)
    st.bar_chart(ders_net)

elif menu == "Soru Analizi":
    st.markdown("## 🔍 Soru Analizi")
    st.warning("⚠️ Bu özellik için Gemini API key gerekli. `secrets.toml` dosyasını yapılandırın.")
    
    uploaded_file = st.file_uploader("Soru görseli yükleyin", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Yüklenen Görsel", width=400)
        st.info("💡 Gerçek uygulamada AI analizi burada görünecek.")

elif menu == "AI Koç":
    st.markdown("## 🤖 AI Koç")
    st.warning("⚠️ Bu özellik için Gemini API key gerekli. `secrets.toml` dosyasını yapılandırın.")
    
    # Basit chat arayüzü
    user_input = st.chat_input("Mesajınızı yazın...")
    
    if user_input:
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write("💡 Gerçek uygulamada AI yanıtı burada görünecek.")

st.sidebar.markdown("---")
st.sidebar.info("""
**Test Modu Aktif**

Google Sheets bağlantısı kurmak için:
1. Google Cloud Console'da Service Account oluşturun
2. JSON key indirin
3. `secrets.toml` dosyasını yapılandırın
4. `streamlit run app.py` ile gerçek uygulamayı başlatın
""")
