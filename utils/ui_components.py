import streamlit as st
import time
from datetime import datetime, timedelta

def render_block_timer(end_time_str: str):
    """
    Verilen bitiş saatine kadar geri sayım yapan bir sayaç bileşeni.
    
    Args:
        end_time_str (str): "HH:MM" formatında bitiş saati (örn: "15:00")
    """
    
    # Bitiş zamanını datetime objesine çevir
    now = datetime.now()
    try:
        end_time = datetime.strptime(end_time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
    except ValueError:
        st.error(f"Hatalı saat formatı: {end_time_str}")
        return

    # Eğer bitiş saati geçmişse (örn: gece yarısı geçişi), yarına at
    if end_time < now and (now - end_time).total_seconds() > 43200: # 12 saatten fazla fark varsa
         end_time += timedelta(days=1)

    # Kalan saniyeyi hesapla
    remaining_seconds = (end_time - now).total_seconds()
    
    if remaining_seconds <= 0:
        st.success("Süre doldu! 🏁")
        return

    # Timer Container
    timer_placeholder = st.empty()
    
    # JavaScript ile Client-Side Timer (Daha akıcı)
    # Streamlit'in native döngüsü yerine HTML/JS inject ediyoruz.
    # Bu sayede Python thread'i bloklanmaz.
    
    timer_html = f"""
    <div style="
        text-align: center; 
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border: 2px solid #FF6B6B;
        margin: 20px 0;
    ">
        <h3 style="color: #6c757d; margin: 0;">Kalan Süre</h3>
        <div id="countdown" style="
            font-size: 3rem; 
            font-weight: bold; 
            color: #FF6B6B; 
            font-family: monospace;
        ">
            --:--:--
        </div>
        <p style="color: #adb5bd; font-size: 0.9rem; margin-top: 5px;">Hedef: {end_time_str}</p>
    </div>

    <script>
    // Hedef zamanı (Python'dan gelen timestamp)
    var countDownDate = new Date({end_time.timestamp() * 1000}).getTime();

    // Her 1 saniyede bir güncelle
    var x = setInterval(function() {{
        var now = new Date().getTime();
        var distance = countDownDate - now;

        // Saat, dakika, saniye hesapla
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Formatla (0 ekle)
        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        // Elementi güncelle
        var display = hours + ":" + minutes + ":" + seconds;
        var el = document.getElementById("countdown");
        if (el) {{
            el.innerHTML = display;
        }}

        // Süre bittiyse
        if (distance < 0) {{
            clearInterval(x);
            if (el) {{
                el.innerHTML = "SÜRE DOLDU";
                el.style.color = "#28a745";
            }}
        }}
    }}, 1000);
    </script>
    """
    
    st.components.v1.html(timer_html, height=200)
