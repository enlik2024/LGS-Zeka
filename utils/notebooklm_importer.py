"""
NotebookLM Importer
Browser automation ile NotebookLM'den içerik çekme modülü.
Playwright kullanarak: Flashcards, Infographics, Summaries, Quizzes, Audio/Video çeker.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import streamlit as st

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class NotebookContent:
    """NotebookLM'den çekilen içerik yapısı"""
    notebook_url: str
    notebook_title: str = ""
    
    # Studio içerikleri
    flashcards: List[Dict[str, str]] = field(default_factory=list)
    summary_text: str = ""
    infographic_path: str = ""
    quiz_questions: List[Dict[str, Any]] = field(default_factory=list)
    audio_url: str = ""
    video_url: str = ""
    
    # Metadata
    source_count: int = 0
    extraction_timestamp: str = ""
    errors: List[str] = field(default_factory=list)


class NotebookLMImporter:
    """
    NotebookLM'den içerik çekme sınıfı.
    
    Kullanım:
        # İlk kullanımda oturum açmak için:
        importer = NotebookLMImporter()
        importer.login_and_save_session()  # Manuel login yaparsınız
        
        # Sonraki kullanımlarda:
        content = importer.extract_all("https://notebooklm.google.com/notebook/xxx")
    """
    
    COOKIE_FILE = "data/notebooklm_cookies.json"
    
    def __init__(self, headless: bool = True, download_dir: str = None):
        """
        Args:
            headless: Tarayıcıyı arka planda çalıştır
            download_dir: İndirilen dosyaların kaydedileceği klasör
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright yüklü değil. 'pip install playwright' ile yükleyin.")
        
        self.headless = headless
        self.download_dir = download_dir or str(Path.cwd() / "data" / "notebooklm_imports")
        
        # Download klasörünü oluştur
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        Path("data").mkdir(parents=True, exist_ok=True)
    
    def login_and_save_session(self) -> bool:
        """
        Persistent browser context ile oturum açar.
        Bu yöntem Google'ın bot algılamasını atlatır.
        
        Returns:
            bool: Başarılı ise True
        """
        print("🔐 Google oturumu açılıyor (Persistent Mode)...")
        print("📝 Lütfen açılan tarayıcıda Google hesabınıza giriş yapın.")
        print("⏳ NotebookLM ana sayfası yüklenince otomatik kaydedilecek.\n")
        
        user_data_dir = str(Path.cwd() / "data" / "browser_profile")
        Path(user_data_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            with sync_playwright() as p:
                # Persistent context - kalıcı profil, gerçek tarayıcı gibi davranır
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=False,
                    locale="tr-TR",
                    # Gerçek tarayıcı gibi görünmek için
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                )
                
                page = context.new_page()
                
                # NotebookLM'e git
                page.goto("https://notebooklm.google.com/", wait_until="networkidle")
                
                print("⌛ Giriş yapmanızı bekliyorum... (Max 5 dakika)")
                print("   Giriş yapınca otomatik kaydedilecek.")
                
                # NotebookLM ana sayfasına yönlendirilmesini bekle (login sonrası)
                try:
                    # "Not defteri" veya benzer bir element görününce giriş başarılı
                    page.wait_for_selector("text=Not defteri", timeout=300000)
                    page.wait_for_timeout(2000)  # Sayfa tamamen yüklensin
                except:
                    # Alternatif: URL'nin notebook içermesini bekle
                    try:
                        page.wait_for_url("**/notebooklm.google.com/**", timeout=60000)
                    except:
                        pass
                
                # Cookie'leri kaydet (tarayıcı kapanmadan ÖNCE)
                cookies = context.cookies()
                with open(self.COOKIE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cookies, f, ensure_ascii=False, indent=2)
                
                print(f"\n✅ Oturum kaydedildi!")
                print(f"   Browser profil: {user_data_dir}")
                print(f"   Cookie backup: {self.COOKIE_FILE} ({len(cookies)} cookie)")
                print(f"\n🔔 Şimdi tarayıcıyı kapatabilirsiniz.")
                
                # Kullanıcının tarayıcıyı kapatmasını bekle
                try:
                    page.wait_for_event("close", timeout=60000)
                except:
                    pass
                
                context.close()
                return True
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            return False
    
    def _load_cookies(self, context):
        """Kayıtlı cookie'leri yükler."""
        if not os.path.exists(self.COOKIE_FILE):
            return False
        
        try:
            with open(self.COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print(f"🍪 {len(cookies)} cookie yüklendi.")
            return True
        except Exception as e:
            print(f"⚠️ Cookie yükleme hatası: {e}")
            return False
    
    def has_valid_session(self) -> bool:
        """Kayıtlı geçerli bir oturum var mı kontrol eder."""
        return os.path.exists(self.COOKIE_FILE)
    
    def extract_all(self, notebook_url: str, progress_callback=None) -> NotebookContent:
        """
        NotebookLM'den tüm içerikleri çeker.
        Persistent context kullanarak Google bot algılamasını atlatır.
        
        Args:
            notebook_url: NotebookLM notebook URL'i
            progress_callback: İlerleme durumu callback fonksiyonu (0-100)
        
        Returns:
            NotebookContent: Çekilen tüm içerikler
        """
        content = NotebookContent(notebook_url=notebook_url)
        content.extraction_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Browser profil kontrolü
        user_data_dir = str(Path.cwd() / "data" / "browser_profile")
        if not os.path.exists(user_data_dir):
            content.errors.append("Browser profil bulunamadı. Önce 'login_and_save_session()' çalıştırın.")
            return content
        
        try:
            with sync_playwright() as p:
                # Persistent context - kayıtlı profili kullan
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=self.headless,
                    locale="tr-TR",
                    accept_downloads=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox"
                    ]
                )
                
                page = context.new_page()
                
                # 1. Sayfayı aç (domcontentloaded daha hızlı, sonra manuel bekle)
                if progress_callback:
                    progress_callback(10, "Notebook açılıyor...")
                
                page.goto(notebook_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(5000)  # Sayfanın JS'lerini yüklemesi için bekle
                
                # 2. Başlığı al
                try:
                    title_elem = page.query_selector("h1, [class*='title']")
                    if title_elem:
                        content.notebook_title = title_elem.inner_text().strip()
                except:
                    pass
                
                # 3. Studio sekmesine git
                if progress_callback:
                    progress_callback(20, "Studio sekmesi açılıyor...")
                
                try:
                    studio_tab = page.get_by_text("Studio", exact=True)
                    if studio_tab:
                        studio_tab.click()
                        page.wait_for_timeout(2000)
                except Exception as e:
                    content.errors.append(f"Studio sekmesi bulunamadı: {str(e)}")
                
                # 4. Studio içeriklerini listele ve çek
                if progress_callback:
                    progress_callback(30, "İçerikler taranıyor...")
                
                studio_items = self._get_studio_items(page)
                
                for idx, item in enumerate(studio_items):
                    item_type = item.get("type", "unknown")
                    item_name = item.get("name", "")
                    
                    progress = 30 + int((idx / max(len(studio_items), 1)) * 60)
                    if progress_callback:
                        progress_callback(progress, f"Çekiliyor: {item_name}")
                    
                    try:
                        if "kart" in item_name.lower() or "flashcard" in item_type.lower():
                            content.flashcards = self._extract_flashcards(page, item)
                        
                        elif "rehber" in item_name.lower() or "infographic" in item_type.lower():
                            content.infographic_path = self._extract_infographic(page, item)
                        
                        elif "sınav" in item_name.lower() or "quiz" in item_type.lower():
                            content.quiz_questions = self._extract_quiz(page, item)
                        
                        elif "anatomisi" in item_name.lower() or "summary" in item_type.lower():
                            content.summary_text = self._extract_summary(page, item)
                        
                        elif "şifre" in item_name.lower() or "audio" in item_type.lower() or "video" in item_type.lower():
                            audio_url = self._extract_audio(page, item)
                            if audio_url:
                                content.audio_url = audio_url
                                
                    except Exception as e:
                        content.errors.append(f"{item_name} çekilemedi: {str(e)}")
                
                if progress_callback:
                    progress_callback(95, "Temizlik yapılıyor...")
                
                context.close()
                
                if progress_callback:
                    progress_callback(100, "Tamamlandı!")
        
        except Exception as e:
            content.errors.append(f"Genel hata: {str(e)}")
        
        return content
    
    def _get_studio_items(self, page: Page) -> List[Dict[str, str]]:
        """Studio sekmesindeki tüm içerikleri listeler."""
        items = []
        
        try:
            # Studio listesindeki öğeleri bul
            item_elements = page.query_selector_all("[class*='studio'] [class*='item'], [class*='card']")
            
            for elem in item_elements:
                try:
                    text = elem.inner_text().strip()
                    if text and len(text) > 2:
                        items.append({
                            "name": text.split("\n")[0],  # İlk satır başlık
                            "type": self._guess_type(text),
                            "element": elem
                        })
                except:
                    continue
        except:
            pass
        
        # Fallback: Metin bazlı arama
        if not items:
            known_items = [
                ("Kartları", "flashcard"),
                ("Rehber", "infographic"),
                ("Sınavı", "quiz"),
                ("Anatomisi", "summary"),
                ("Şifre", "audio")
            ]
            
            for keyword, item_type in known_items:
                elem = page.get_by_text(keyword, exact=False).first
                if elem:
                    items.append({
                        "name": keyword,
                        "type": item_type,
                        "element": elem
                    })
        
        return items
    
    def _guess_type(self, text: str) -> str:
        """Metin içeriğinden içerik tipini tahmin et."""
        text_lower = text.lower()
        if "kart" in text_lower: return "flashcard"
        if "rehber" in text_lower: return "infographic"
        if "sınav" in text_lower: return "quiz"
        if "anatom" in text_lower: return "summary"
        if "şifre" in text_lower or "podcast" in text_lower: return "audio"
        return "unknown"
    
    def _extract_flashcards(self, page: Page, item: Dict) -> List[Dict[str, str]]:
        """Flashcard'ları çeker (CSV indirerek)."""
        flashcards = []
        
        try:
            # Elementi yeniden bul (stale reference önleme)
            keyword = item.get("name", "Kartları")
            elem = page.get_by_text(keyword, exact=False).first
            
            if elem:
                elem.click()
                page.wait_for_timeout(2000)
            
            # Download butonunu bul ve tıkla
            download_btn = page.locator("[aria-label*='Download'], [aria-label*='download'], [aria-label*='indir']").first
            
            if download_btn and download_btn.is_visible():
                with page.expect_download() as download_info:
                    download_btn.click()
                
                download = download_info.value
                csv_path = os.path.join(self.download_dir, f"flashcards_{int(time.time())}.csv")
                download.save_as(csv_path)
                
                # CSV'yi parse et
                import csv
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        flashcards.append({
                            "front": row.get("front", row.get("Soru", row.get("question", ""))),
                            "back": row.get("back", row.get("Cevap", row.get("answer", ""))),
                            "difficulty": row.get("difficulty", "medium"),
                            "tags": row.get("tags", "")
                        })
            
            # Geri dön (back butonu veya escape)
            try:
                back_btn = page.locator("[aria-label*='Back'], [aria-label*='back'], [aria-label*='Geri']").first
                if back_btn and back_btn.is_visible():
                    back_btn.click()
                else:
                    page.keyboard.press("Escape")
            except:
                page.keyboard.press("Escape")
            
            page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"Flashcard extraction error: {e}")
        
        return flashcards
    
    def _extract_infographic(self, page: Page, item: Dict) -> str:
        """İnfografik resmini indirir."""
        try:
            item["element"].click()
            page.wait_for_timeout(2000)
            
            # Infografik görselini bul ve screenshot al
            img_elem = page.locator("img[src*='infographic'], [class*='infographic'] img").first
            
            if img_elem:
                img_path = os.path.join(self.download_dir, f"infographic_{int(time.time())}.png")
                img_elem.screenshot(path=img_path)
                
                # Geri dön
                page.go_back()
                page.wait_for_timeout(1000)
                
                return img_path
        except Exception as e:
            print(f"Infographic extraction error: {e}")
        
        return ""
    
    def _extract_quiz(self, page: Page, item: Dict) -> List[Dict[str, Any]]:
        """Quiz sorularını çeker."""
        questions = []
        
        try:
            item["element"].click()
            page.wait_for_timeout(2000)
            
            # Quiz sorularını bul
            question_elems = page.query_selector_all("[class*='question']")
            
            for q_elem in question_elems:
                try:
                    q_text = q_elem.inner_text()
                    questions.append({
                        "question": q_text,
                        "options": [],  # Şıkları çekmek için daha detaylı parsing gerekli
                        "correct_answer": ""
                    })
                except:
                    continue
            
            # Geri dön
            page.go_back()
            page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Quiz extraction error: {e}")
        
        return questions
    
    def _extract_summary(self, page: Page, item: Dict) -> str:
        """Özet metnini çeker."""
        try:
            item["element"].click()
            page.wait_for_timeout(2000)
            
            # İçerik metnini al
            content_elem = page.locator("[class*='content'], [class*='body'], main").first
            if content_elem:
                text = content_elem.inner_text()
                
                # Geri dön
                page.go_back()
                page.wait_for_timeout(1000)
                
                return text
        except Exception as e:
            print(f"Summary extraction error: {e}")
        
        return ""
    
    def _extract_audio(self, page: Page, item: Dict) -> str:
        """Audio/Video URL'ini çeker."""
        try:
            item["element"].click()
            page.wait_for_timeout(2000)
            
            # Audio/Video elementini bul
            media_elem = page.locator("audio source, video source, [src*='googlevideo']").first
            
            if media_elem:
                url = media_elem.get_attribute("src")
                
                # Geri dön
                page.go_back()
                page.wait_for_timeout(1000)
                
                return url or ""
        except Exception as e:
            print(f"Audio extraction error: {e}")
        
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT UI ENTEGRASYONU
# ─────────────────────────────────────────────────────────────────────────────

def render_notebooklm_importer():
    """Veli panelinde NotebookLM içerik aktarma arayüzü."""
    
    st.subheader("📥 NotebookLM'den İçerik Aktar")
    
    if not PLAYWRIGHT_AVAILABLE:
        st.error("⚠️ Playwright yüklü değil. Lütfen 'pip install playwright' komutunu çalıştırın.")
        return
    
    notebook_url = st.text_input(
        "Notebook URL",
        placeholder="https://notebooklm.google.com/notebook/...",
        help="NotebookLM'den paylaşıma açtığınız notebook linki"
    )
    
    # Hedef kazanım seçimi (opsiyonel)
    target_kazanim = st.text_input(
        "Hedef Kazanım Kodu (opsiyonel)",
        placeholder="M.8.1.1.1",
        help="Bu içeriklerin bağlanacağı MEB kazanım kodu"
    )
    
    # Çekilecek içerikler
    st.write("**Çekilecek İçerikler:**")
    col1, col2 = st.columns(2)
    with col1:
        extract_flashcards = st.checkbox("🃏 Flashcard'lar", value=True)
        extract_infographic = st.checkbox("📊 İnfografik", value=True)
        extract_summary = st.checkbox("📄 Özet", value=True)
    with col2:
        extract_quiz = st.checkbox("❓ Quiz", value=False)
        extract_audio = st.checkbox("🎧 Audio/Video", value=True)
    
    if st.button("🚀 İçeriği Çek", type="primary", disabled=not notebook_url):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(percent, message):
            progress_bar.progress(percent / 100)
            status_text.text(message)
        
        try:
            importer = NotebookLMImporter(headless=True)
            content = importer.extract_all(notebook_url, progress_callback=update_progress)
            
            # Sonuçları göster
            st.success("✅ İçerik çekme tamamlandı!")
            
            # İstatistikler
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Flashcard", len(content.flashcards))
            with col2:
                st.metric("Quiz Soruları", len(content.quiz_questions))
            with col3:
                has_audio = "✅" if content.audio_url else "❌"
                st.metric("Audio", has_audio)
            
            # Detaylar
            with st.expander("📋 Çekilen İçerik Detayları"):
                st.json({
                    "title": content.notebook_title,
                    "flashcard_count": len(content.flashcards),
                    "summary_length": len(content.summary_text),
                    "infographic_path": content.infographic_path,
                    "audio_url": content.audio_url[:100] + "..." if content.audio_url else "",
                    "errors": content.errors
                })
            
            # Session state'e kaydet
            st.session_state["last_notebooklm_import"] = content
            
            if content.errors:
                st.warning(f"⚠️ {len(content.errors)} hata oluştu. Detaylar için yukarıdaki JSON'a bakın.")
                
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")


# Test için
if __name__ == "__main__":
    import sys
    
    importer = NotebookLMImporter(headless=False)  # Debug için görünür tarayıcı
    
    # Oturum kontrolü
    if not importer.has_valid_session():
        print("=" * 50)
        print("🔐 İLK KULLANIM - OTURUM GEREKLİ")
        print("=" * 50)
        print("\nBir tarayıcı penceresi açılacak.")
        print("Google hesabınızla giriş yapın.")
        print("NotebookLM sayfası yüklendiğinde cookie'ler kaydedilecek.\n")
        
        input("Devam etmek için ENTER'a basın...")
        
        if importer.login_and_save_session():
            print("\n✅ Oturum kaydedildi! Şimdi içerik çekmeyi deneyebilirsiniz.")
        else:
            print("\n❌ Oturum kaydedilemedi.")
            sys.exit(1)
    
    # Örnek URL ile test
    print("\n" + "=" * 50)
    print("📥 İÇERİK ÇEKME TESTİ")
    print("=" * 50)
    
    test_url = "https://notebooklm.google.com/notebook/03c5a26f-1e9f-4082-8bf5-2284b8ef9188"
    print(f"URL: {test_url}\n")
    
    content = importer.extract_all(test_url)
    
    print(f"\n📊 SONUÇLAR:")
    print(f"   Başlık: {content.notebook_title}")
    print(f"   Flashcard: {len(content.flashcards)} adet")
    print(f"   Quiz Soruları: {len(content.quiz_questions)} adet")
    print(f"   Özet Uzunluğu: {len(content.summary_text)} karakter")
    print(f"   İnfografik: {content.infographic_path or 'Yok'}")
    print(f"   Audio URL: {'Var' if content.audio_url else 'Yok'}")
    print(f"   Hatalar: {len(content.errors)} adet")
    
    if content.errors:
        print(f"\n⚠️ HATALAR:")
        for err in content.errors:
            print(f"   - {err}")

