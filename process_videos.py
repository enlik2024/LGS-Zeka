import os
try:
    # MoviePy 2.x imports
    from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
except ImportError:
    try:
        # Fallback for older versions
        from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
    except ImportError:
        print("Moviepy kütüphanesi eksik veya import hatası. Lütfen 'pip install moviepy' komutunu çalıştırın.")
        exit()

RAW_DIR = "raw_videos"
ASSETS_DIR = "assets"
LOGO_PATH = "assets/lgs_logo_mask.png"

def process_videos():
    if not os.path.exists(RAW_DIR):
        print(f"Klasör bulunamadı: {RAW_DIR}")
        return

    # İşlenecek videoları bul
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".mp4")]
    
    if not files:
        print(f"'{RAW_DIR}' klasöründe video bulunamadı.")
        return

    for filename in files:
        input_path = os.path.join(RAW_DIR, filename)
        
        # Temiz isim oluştur (ör: NB_Video_Konu.mp4 -> Konu.mp4 veya direkt aynı isim)
        output_filename = filename.replace("raw_", "").replace("_raw", "")
        if output_filename == filename:
            output_filename = f"processed_{filename}"
            
        output_path = os.path.join(ASSETS_DIR, output_filename)
        
        if os.path.exists(output_path):
            print(f"Zaten işlenmiş, atlanıyor: {output_filename}")
            continue
            
        print(f"İşleniyor: {filename} -> {output_filename}...")
        
        try:
            video = VideoFileClip(input_path)
            
            # YouTube "1080p" etiketi için upscale (Fake HD)
            if video.h < 1080:
                print(f"Upscaling from {video.h}p to 1080p (Fast Mode)...")
                video = video.resized(height=1080)
            
            # Logoyu yükle
            # MoviePy v2: set_duration -> with_duration
            logo = ImageClip(LOGO_PATH).with_duration(video.duration)
            
            # Logoyu sağ alta yerleştir (10px padding)
            logo = logo.with_position(("right", "bottom"))
            
            # Maskeleme (Composite)
            final = CompositeVideoClip([video, logo])
            
            # Kaydet (Ultra Hızlı Preset ile)
            # codec="libx264"
            # preset="ultrafast" -> En önemli ayar bu
            # bitrate="5000k" -> 1080p için ortalama yeterli
            final.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                bitrate="5000k",
                preset="ultrafast",
                threads=4
            )
            print(f"✅ Tamamlandı (1080p Fast Render): {output_path}")
            
            video.close()
            
        except Exception as e:
            print(f"❌ Hata ({filename}): {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    process_videos()
