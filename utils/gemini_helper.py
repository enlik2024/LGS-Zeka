"""
Gemini AI Helper Modülü
LGS-Zeka platformu için Google Gemini AI entegrasyonu.
Soru görseli analizi ve AI destekli öğretim özellikleri.
"""

from typing import Dict, Any, Optional, List, Union
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import json
import base64
import re
from pathlib import Path
from google.api_core import exceptions

from datetime import datetime

# Yeni promptları import et
from prompts.analysis_prompts import (
    QUICK_ANALYSIS_PROMPT,
    DETAILED_ANALYSIS_PROMPT,
    VISUAL_ANALYSIS_PROMPT,
    QUESTION_ANALYSIS_PROMPT,
    BATCH_ANALYSIS_PROMPT,
    VARIANT_GENERATION_PROMPT
)
from prompts.teaching_prompts import (
    SOCRATIC_TUTOR_PROMPT,
    HINT_GENERATOR_PROMPT,
    CONCEPT_EXPLAINER_PROMPT
)


class GeminiHelper:
    """
    Google Gemini AI ile etkileşim için yardımcı sınıf.
    Soru analizi, çözüm önerileri ve eğitim desteği sağlar.
    """
    
    # Model tipleri artık config'den okunuyor
    # Bkz: config/app_config.yaml -> ai.models
    # Fallback sırası: primary -> fallback_1 -> fallback_2
    
    # Sistem promptları
    # Sistem promptları (prompts/analysis_prompts.py dosyasından gelir)
    QUESTION_ANALYSIS_PROMPT = QUESTION_ANALYSIS_PROMPT
    BATCH_ANALYSIS_PROMPT = BATCH_ANALYSIS_PROMPT
    VARIANT_GENERATION_PROMPT = VARIANT_GENERATION_PROMPT

    
    def __init__(self, api_key: Optional[str] = None, config_manager=None):
        """
        GeminiHelper başlatıcı.
        
        Args:
            api_key: Manuel API key (opsiyonel)
            config_manager: UnifiedConfigManager instance (opsiyonel)
        """
        # Config manager'dan API key ve model ayarlarını al
        from utils.config_manager import get_config
        self._config = config_manager or get_config()
        
        # API key öncelik sırası: manuel > config manager > secrets.toml
        self.api_key = api_key or self._config.get_active_api_key() or self._get_api_key_from_secrets()
        self._configure_api()
        self._models = {}
        self._current_model_index = 0
    
    # ... (diğer metodlar aynı)

    def _get_api_key_from_secrets(self) -> str:
        """Streamlit secrets'tan API anahtarını alır."""
        try:
            api_key = st.secrets.get("gemini", {}).get("api_key", None)
            if not api_key:
                raise ValueError(
                    "Gemini API key bulunamadı. "
                    ".streamlit/secrets.toml dosyasını kontrol edin."
                )
            return api_key
        except Exception as e:
            st.error(f"API key alınamadı: {str(e)}")
            raise
    
    def _configure_api(self) -> None:
        """Gemini API'yi yapılandırır."""
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            st.error(f"Gemini API yapılandırılamadı: {str(e)}")
            raise
    
    def _get_model(self, model_type: str = "flash") -> genai.GenerativeModel:
        """
        Modeli döndürür.
        
        Model seçimi config/app_config.yaml'dan yapılır.
        Cascade: primary -> fallback_1 -> fallback_2
        """
        # Model adını config'den al
        if model_type in ["primary", "flash"]:
            model_name = self._config.get_model("primary")
        elif model_type == "pro":
            # Pro için de primary kullan (aynı model)
            model_name = self._config.get_model("primary")
        elif model_type == "tts":
            model_name = self._config.get_model("tts")
        elif model_type == "audio":
            model_name = self._config.get_model("audio_dialog")
        else:
            model_name = self._config.get_model(model_type)
        
        if model_name not in self._models:
            # Generation config'i config'den al
            generation_config = self._config.get_generation_config()
            
            self._models[model_name] = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
        
        return self._models[model_name]
    
    def _try_with_fallback(self, func, *args, **kwargs):
        """
        API çağrısını fallback ile dene.
        Kota aşılırsa sonraki modele geç (model cascading).
        Tüm modeller başarısız olursa API key değiştir.
        """
        # Model cascade listesi
        model_cascade = self._config.get_model_cascade()
        
        for model_idx, model_name in enumerate(model_cascade):
            try:
                # Model'i güncelle
                kwargs['_model_name'] = model_name
                return func(*args, **kwargs)
                
            except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable) as e:
                # Kota veya servis hatası
                reason = "Kota Doldu"
                print(f"⚠️ {reason}: {model_name} ({type(e).__name__})")
                
                if model_idx < len(model_cascade) - 1:
                    next_model = model_cascade[model_idx + 1]
                    st.toast(f"🔄 {reason}: {model_name} → {next_model}", icon="🔀")
                    continue
                else:
                    # Kota hatasıysa ve fallback kalmadıysa API Key değiştir
                    if self._config.mark_key_quota_exceeded():
                        self.api_key = self._config.get_active_api_key()
                        if self.api_key:
                            self._configure_api()
                            self._models = {}
                            st.toast(f"🔑 API key değiştirildi (fallback)", icon="🔑")
                            return self._try_with_fallback(func, *args, **kwargs)
                raise
                
            except (exceptions.NotFound, exceptions.InvalidArgument) as e:
                # Model bulunamadı veya parametre hatası
                reason = "Model Bulunamadı"
                print(f"⚠️ {reason}: {model_name} ({type(e).__name__})")
                
                if model_idx < len(model_cascade) - 1:
                    next_model = model_cascade[model_idx + 1]
                    st.toast(f"🔄 {reason}: {model_name} → {next_model}", icon="🔀")
                    continue
                raise
            except Exception as e:
                raise e
        
        raise Exception("Tüm modeller denendi ve başarısız oldu.")

    def _prepare_image(self, image_input: Union[Image.Image, bytes, str]) -> Image.Image:
        """Görseli hazırlar."""
        try:
            if isinstance(image_input, Image.Image):
                return image_input
            elif isinstance(image_input, bytes):
                return Image.open(io.BytesIO(image_input))
            elif isinstance(image_input, str):
                return Image.open(image_input)
            else:
                raise ValueError(f"Desteklenmeyen görsel tipi: {type(image_input)}")
        except Exception as e:
            st.error(f"Görsel işlenemedi: {str(e)}")
            raise

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        JSON parse - kesik yanıtları da kurtarmaya çalışır.
        Token limiti aşıldığında JSON eksik kalabilir.
        """
        import re
        
        try:
            text = response_text.strip()
            
            # Markdown code block'u temizle
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                parts = text.split("```")
                if len(parts) >= 2:
                    text = parts[1].strip()
            
            # JSON objesini bul
            json_match = re.search(r'(\{.*)', text, re.DOTALL)
            if json_match:
                text = json_match.group(1)
            
            # İlk parse denemesi
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                # DEBUG: İlk parse hatası
                print(f"DEBUG FIRST PARSE FAILED: {e}")
                print(f"DEBUG Error position: char {e.pos if hasattr(e, 'pos') else 'unknown'}")
                # Hatanın olduğu bölgeyi göster
                if hasattr(e, 'pos') and e.pos:
                    start = max(0, e.pos - 50)
                    end = min(len(text), e.pos + 50)
                    print(f"DEBUG Around error: ...{text[start:end]}...")
                pass
            
            # Kesik JSON tamiri
            # Eksik parantez/tırnak ekle
            text = self._repair_truncated_json(text)
            
            return json.loads(text)
            
        except Exception as e:
            # DEBUG: Parse hatası detayları
            print(f"DEBUG JSON PARSE ERROR: {e}")
            print(f"DEBUG Text length: {len(response_text)} chars")
            print(f"DEBUG First 200 chars: {response_text[:200]}")
            st.toast(f"⚠️ JSON parse hatası: {str(e)[:50]}", icon="🔍")
            
            # En kötü durumda ham yanıttan temel bilgileri çıkar
            extracted = self._extract_basic_info(response_text)
            if extracted:
                extracted["_partial"] = True
                # Debug için daha fazla karakter göster (5000)
                extracted["ham_yanit"] = response_text[:5000] + "..." if len(response_text) > 5000 else response_text
                return extracted
            
            return {"error": "JSON Parse Error", "ham_yanit": response_text}
    
    def _repair_truncated_json(self, text: str) -> str:
        """Kesik JSON'ı tamir etmeye çalış."""
        # Trailing comma temizle
        text = re.sub(r',\s*$', '', text)
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        # Açık tırnakları kapat
        open_quotes = text.count('"') % 2
        if open_quotes == 1:
            text += '"'
        
        # Eksik parantezleri kapat
        open_brackets = text.count('[') - text.count(']')
        open_braces = text.count('{') - text.count('}')
        
        for _ in range(open_brackets):
            text += ']'
        for _ in range(open_braces):
            text += '}'
        
        return text
    
    def _extract_basic_info(self, text: str) -> Optional[Dict[str, Any]]:
        """Ham metinden temel bilgileri çıkar."""
        import re
        
        result = {}
        
        # Doğru cevabı bul - her türlü format (A, A) 3600, 3600, vb.)
        cevap_match = re.search(r'"dogru_cevap"\s*:\s*"([^"]+)"', text)
        if cevap_match:
            result["dogru_cevap"] = cevap_match.group(1)
        
        # Konu bul
        konu_match = re.search(r'"konu"\s*:\s*"([^"]+)"', text)
        if konu_match:
            result["konu"] = konu_match.group(1)
        
        # Zorluk bul
        zorluk_match = re.search(r'"zorluk_seviyesi"\s*:\s*(\d)', text)
        if zorluk_match:
            result["zorluk_seviyesi"] = int(zorluk_match.group(1))
        
        return result if result else None

    def _get_safe_response_text(self, response) -> str:
        """
        Güvenli bir şekilde yanıt metnini alır.
        MAX_TOKENS durumunda KISMI YANIT döndürür (Böylece kurtarabiliriz).
        """
        if not response.candidates:
            raise ValueError("AI yanıt döndürmedi (Aday yok).")
        
        candidate = response.candidates[0]
        finish_reason = getattr(candidate, 'finish_reason', None)
        
        # Finish Reason 2: MAX_TOKENS (Token limiti)
        # Hata fırlatmak yerine uyarı verip metni döndürelim.
        if finish_reason == 2 or str(finish_reason) == "MAX_TOKENS":
            # DEBUG: Token kullanımını logla
            usage = getattr(response, 'usage_metadata', None)
            if usage:
                print(f"DEBUG TOKEN USAGE:")
                print(f"  - Input tokens: {getattr(usage, 'prompt_token_count', 'N/A')}")
                print(f"  - Output tokens: {getattr(usage, 'candidates_token_count', 'N/A')}")
                print(f"  - Total tokens: {getattr(usage, 'total_token_count', 'N/A')}")
                st.toast(f"🔍 Debug: Output={getattr(usage, 'candidates_token_count', '?')} tokens", icon="📊")
            
            # Kısmi metni al
            partial_text = ""
            if candidate.content and candidate.content.parts:
                partial_text = "".join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
            
            if partial_text:
                st.warning(f"⚠️ Yanıt token limitine takıldı (finish_reason={finish_reason}), kısmi sonuç işleniyor...")
                return partial_text
            else:
                raise ValueError("❌ Yanıt token limitine takıldı ve metin alınamadı.")
        
        # Diğer kritik hatalar
        if finish_reason == 3 or str(finish_reason) == "SAFETY":
            raise ValueError("❌ Yanıt güvenlik filtresine takıldı. Görseli kontrol edin.")
        
        if finish_reason == 4 or str(finish_reason) == "RECITATION":
            raise ValueError("❌ Yanıt telif hakkı filtresine takıldı.")
        
        # Normal akış
        try:
            return response.text
        except Exception as e:
            if candidate.content and candidate.content.parts:
                partial_text = "".join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                if partial_text:
                    return partial_text
            raise ValueError(f"Yanıt metni alınamadı: {str(e)}")

    def analyze_question_image(
        self,
        image_input: Union[Image.Image, bytes, str],
        model_type: str = "flash",
        custom_prompt: Optional[str] = None,
        question_index: int = 1
    ) -> Dict[str, Any]:
        """
        Soru görselini analiz eder ve detaylı bilgi döndürür.
        Model cascading ile fallback desteği var.
        
        Args:
            image_input: Görsel (PIL Image, bytes veya dosya yolu)
            model_type (str): 'flash' (hızlı) veya 'pro' (yüksek kalite)
            custom_prompt (Optional[str]): Özel prompt (None ise varsayılan)
            question_index (int): Sayfadaki kaçıncı soruya odaklanılacağı.
            
        Returns:
            Dict: Soru analiz sonuçları
        """
        # Görseli hazırla
        image = self._prepare_image(image_input)
        
        # Prompt oluştur
        if custom_prompt:
            prompt = custom_prompt
        else:
            base_prompt = self.QUESTION_ANALYSIS_PROMPT
            if question_index > 1:
                prompt = f"""
                BU GÖRSELDEKİ {question_index}. SORUYA ODAKLAN.
                
                Sayfada yukarıdan aşağıya, soldan sağa doğru saydığında {question_index}. sırada olan soruyu analiz et.
                Diğer soru veya metinleri görmezden gel.
                
                {base_prompt}
                """
            else:
                prompt = f"""
                Bu görseldeki soruyu analiz et. Eğer birden fazla soru varsa İLK soruyu (veya en belirgin olanı) analiz et.
                
                {base_prompt}
                """
        
        # Generation config
        # NOT: gemini-2.5-flash LaTeX formüllü detaylı çözümler ürettiğinde
        # 8192 token yetmiyor, 16384'e çıkarıldı
        explicit_config = {
            "max_output_tokens": 16384,
            "temperature": 0.4,
            "response_mime_type": "application/json"
        }
        
        # Safety settings - BLOCK_NONE (llm_adapter.py'deki gibi)
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        # Model cascade listesi
        
        max_key_retries = 3
        key_retry_count = 0
        
        while key_retry_count < max_key_retries:
            model_cascade = self._config.get_model_cascade()
            last_error = None
            key_rotated = False
            
            for model_idx, model_name in enumerate(model_cascade):
                try:
                    with st.spinner(f"🤖 AI analiz ediyor ({model_name})..."):
                        # Model al veya oluştur
                        if model_name not in self._models:
                            self._models[model_name] = genai.GenerativeModel(model_name=model_name)
                        
                        model = self._models[model_name]
                        
                        response = model.generate_content(
                            [prompt, image],
                            generation_config=explicit_config,
                            safety_settings=safety_settings
                        )
                        
                        # Güvenli metin alımı
                        response_text = self._get_safe_response_text(response)
                        
                        # JSON parse
                        result = self._parse_json_response(response_text)
                        
                        # Metadata ekle
                        result["model_used"] = model_name
                        result["timestamp"] = st.session_state.get("current_time", "")
                        
                        return result
                        
                except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable) as e:
                    reason = "Kota Doldu"
                    last_error = e
                    print(f"⚠️ {reason}: {model_name} ({type(e).__name__})")
                    
                    if model_idx < len(model_cascade) - 1:
                        next_model = model_cascade[model_idx + 1]
                        st.toast(f"🔄 {reason}: {model_name} → {next_model}", icon="🔀")
                        continue
                    else:
                        # Bu anahtar için tüm modeller tükendi
                        st.error(f"⚠️ Bu API anahtarı için tüm modellerin kotası doldu.")
                        
                        # API Key Rotasyonu
                        if self._config.mark_key_quota_exceeded():
                            new_key = self._config.get_active_api_key()
                            if new_key:
                                self.api_key = new_key
                                self._configure_api()
                                self._models = {}
                                st.toast(f"🔑 Yeni API Anahtarına Geçiliyor...", icon="🔄")
                                key_rotated = True
                                break # For döngüsünü kır, While döngüsü başa dönecek
                        
                        st.error("❌ Yedek API anahtarı kalmadı.")
                        
                except (exceptions.NotFound, exceptions.InvalidArgument) as e:
                    reason = "Model Bulunamadı"
                    last_error = e
                    print(f"⚠️ {reason}: {model_name} ({type(e).__name__})")
                    
                    if model_idx < len(model_cascade) - 1:
                        next_model = model_cascade[model_idx + 1]
                        st.toast(f"🔄 {reason}: {model_name} → {next_model}", icon="🔀")
                        continue
                    else:
                        st.error(f"⚠️ Model bulunamadı ve fallback kalmadı.")

                except Exception as e:
                    last_error = e
                    st.error(f"Soru analizi hatası: {str(e)}")
                    break # Kritik hata, döngüden çık
            
            # For döngüsü bitti
            if key_rotated:
                key_retry_count += 1
                continue # While döngüsüne devam (Yeni key ile)
            else:
                break # Key rotasyonu olmadıysa işlem bitmiştir (başarılı veya başarısız)
        
        # Hata durumu
        return {
            "error": str(last_error) if last_error else "Bilinmeyen hata",
            "soru_metni": "Analiz başarısız",
            "konu": "Hata",
            "cozum_adimlari": ["Lütfen tekrar deneyin"],
            "zorluk_seviyesi": 0
        }
    
    def analyze_image_batch(
        self,
        image_input: Union[Image.Image, bytes, str],
        model_type: str = "flash"
    ) -> List[Dict[str, Any]]:
        """
        Görseldeki TÜM soruları tek seferde analiz eder (Batch Mode).
        Enterprise: JSON Mode ile garantili geçerli JSON çıktısı.
        """
        try:
        image = self._prepare_image(image_input)
            
        max_key_retries = 3
        key_retry_count = 0
        
        while key_retry_count < max_key_retries:
            model_cascade = self._config.get_model_cascade()
            key_rotated = False
            last_error = None
            
            for model_idx, model_name in enumerate(model_cascade):
                try:
                    with st.spinner(f"🚀 Toplu Analiz Yapılıyor ({model_name})..."):
                        # Model al veya oluştur
                        if model_name not in self._models:
                            self._models[model_name] = genai.GenerativeModel(model_name=model_name)
                        model = self._models[model_name]
                        
                        prompt = self.BATCH_ANALYSIS_PROMPT
                        
                        # ENTERPRISE: JSON Mode - API geçerli JSON döndürmeye zorlanır
                        generation_config = {
                            "max_output_tokens": 8192,
                            "temperature": 0.2,
                            "response_mime_type": "application/json"  # JSON MODE
                        }
                        
                        response = model.generate_content(
                            [prompt, image],
                            generation_config=generation_config
                        )
                        response_text = self._get_safe_response_text(response)
                        
                        # JSON Mode ile gelen yanıt doğrudan parse edilebilir
                        try:
                            results = json.loads(response_text)
                        except json.JSONDecodeError as e:
                            # Token Limit nedeniyle kesilme veya bozuk JSON durumu
                            # Kullanıcıyı korkutmamak için warning yerine toast kullanıyoruz
                            st.toast("Veri işleniyor... (Otomatik Düzeltme Devrede)", icon="🔧")
                            print(f"DEBUG: JSON Fix triggered: {e}")
                            
                            text = response_text.strip()
                            results = None
                            
                            # Kurtarma Senaryosu 1: Liste açılmış ([) ama kapanmamış
                            if text.startswith("["):
                                # Sondan geriye doğru son bitmiş objeyi "}," ile arayalım
                                last_clean_end = text.rfind("},")
                                if last_clean_end != -1:
                                    # Kesilen yere kadar al ve listeyi kapat
                                    fixed_text = text[:last_clean_end+1] + "]"
                                    try:
                                        results = json.loads(fixed_text)
                                        st.toast(f"✅ {len(results)} soru başarıyla analiz edildi!", icon="✨")
                                    except:
                                        pass
                                
                                # Eğer yukarıdaki çalışmadıysa, belki tek bir obje vardır ve "}" ile bitiyordur ama "]" yoktur
                                if not results:
                                    last_brace = text.rfind("}")
                                    if last_brace != -1:
                                        fixed_text = text[:last_brace+1] + "]"
                                        try:
                                            results = json.loads(fixed_text)
                                            st.toast("✅ Analiz tamamlandı.", icon="✨")
                                        except:
                                            pass
        
                            # Kurtarma Senaryosu 2: Halen başarısızsak ve veri yoksa
                            if not results:
                                st.error("JSON kurtarılamadı -> Fallback yapılacak.")
                                # JSON hatası model hatası değildir, o yüzden return ediyoruz
                                return [{
                                    "error": f"JSON Parse Error: {str(e)}",
                                    "konu": "Hata",
                                    "soru_metni": "AI yanıtı kesildi",
                                    "ham_yanit": response_text
                                }]
                        
                        # Sonuç işleme
                        if isinstance(results, list):
                            import datetime as dt_module
                            for res in results:
                                res['model_used'] = model_name
                                res['timestamp'] = dt_module.datetime.now().isoformat()
                                if 'cozum_adimlari' not in res: res['cozum_adimlari'] = []
                                if 'konu' not in res: res['konu'] = "Genel"
                                if 'soru_metni' not in res: res['soru_metni'] = "Metin okunamadı"
                            return results
                        elif isinstance(results, dict):
                            import datetime as dt_module
                            results['model_used'] = model_name
                            results['timestamp'] = dt_module.datetime.now().isoformat()
                            return [results]
                        else:
                            return [{"error": "Beklenmeyen format", "ham_yanit": response_text}]

                except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable) as e:
                    reason = "Kota Doldu"
                    last_error = e
                    print(f"⚠️ {reason}: {model_name} ({type(e).__name__})")
                    
                    if model_idx < len(model_cascade) - 1:
                        next_model = model_cascade[model_idx + 1]
                        st.toast(f"🔄 {reason}: {model_name} → {next_model}", icon="🔀")
                        continue
                    else:
                        st.error(f"⚠️ Bu API anahtarı için tüm modellerin kotası doldu.")
                        
                        if self._config.mark_key_quota_exceeded():
                            new_key = self._config.get_active_api_key()
                            if new_key:
                                self.api_key = new_key
                                self._configure_api()
                                self._models = {}
                                st.toast(f"🔑 Yeni API Anahtarına Geçiliyor...", icon="🔄")
                                key_rotated = True
                                break 
                        
                        st.error("❌ Yedek API anahtarı kalmadı.")

                except Exception as e:
                    st.error(f"Batch analiz hatası ({model_name}): {str(e)}")
                    last_error = e
                    # Diğer modelleri dene (Opsiyonel: Kritik hataysa break, ama batch analizde model değiştirmek işe yarayabilir)
                    if model_idx < len(model_cascade) - 1:
                        next_model = model_cascade[model_idx + 1]
                        st.toast(f"🔄 Hata sonrası model değişiyor: {model_name} → {next_model}", icon="⚠️")
                        continue
                    else:
                        break

            if key_rotated:
                key_retry_count += 1
                continue
            else:
                break
        
        return [{"error": str(last_error) if last_error else "Bilinmeyen hata", "konu": "Hata"}]

    def generate_study_plan(
        self,
        weak_topics: List[str],
        target_score: int,
        days_until_exam: int,
        model_type: str = "flash"
    ) -> Dict[str, Any]:
        """
        Zayıf konulara göre kişiselleştirilmiş çalışma planı oluşturur.
        
        Args:
            weak_topics: Zayıf olunan konular listesi
            target_score: Hedef LGS puanı
            days_until_exam: Sınava kalan gün sayısı
            model_type: Model tipi
            
        Returns:
            Dict: Çalışma planı
        """
        try:
            model = self._get_model(model_type)
            
            prompt = f"""Sen bir LGS hazırlık koçusun. Aşağıdaki bilgilere göre 
kişiselleştirilmiş bir çalışma planı oluştur:

Zayıf Konular: {', '.join(weak_topics)}
Hedef Puan: {target_score}
Sınava Kalan Gün: {days_until_exam}

JSON formatında şu yapıda bir plan oluştur:
{{
    "gunluk_program": [
        {{"gun": 1, "konular": ["Konu 1", "Konu 2"], "sure": "2 saat"}},
        ...
    ],
    "oncelikli_konular": ["Konu 1", "Konu 2"],
    "kaynak_onerileri": ["Kaynak 1", "Kaynak 2"],
    "motivasyon_mesaji": "Motivasyon metni",
    "hedef_analiz": "Hedef hakkında yorum"
}}
"""
            
            with st.spinner("📚 Çalışma planı hazırlanıyor..."):
                response = model.generate_content(prompt)
                result = self._parse_json_response(response.text)
                return result
                
        except Exception as e:
            st.error(f"Çalışma planı oluşturulamadı: {str(e)}")
            return {"error": str(e)}
    
    def chat(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        model_type: str = "flash",
        stream: bool = False
    ) -> Union[str, Any]:
        """
        AI ile sohbet eder (Faz 4 için).
        
        Args:
            message: Kullanıcı mesajı
            context: Bağlam bilgisi (öğrenci verileri vb.)
            model_type: Model tipi
            stream: Streaming yanıt (True/False)
            
        Returns:
            str veya Generator: AI yanıtı
        """
        try:
            model = self._get_model(model_type)
            
            # Context varsa ekle
            if context:
                context_text = f"\n\nÖğrenci Bağlamı:\n{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
                full_message = context_text + message
            else:
                full_message = message
            
            # Yanıt al
            if stream:
                response = model.generate_content(full_message, stream=True)
                return response
            else:
                response = model.generate_content(full_message)
                return response.text
                
        except Exception as e:
            st.error(f"Chat hatası: {str(e)}")
            return f"Üzgünüm, bir hata oluştu: {str(e)}"
    
    def explain_solution(
        self,
        question_text: str,
        student_answer: str,
        correct_answer: str,
        model_type: str = "flash"
    ) -> str:
        """
        Öğrencinin yanlış cevabını analiz edip açıklama yapar.
        
        Args:
            question_text: Soru metni
            student_answer: Öğrenci cevabı
            correct_answer: Doğru cevap
            model_type: Model tipi
            
        Returns:
            str: Açıklama metni
        """
        try:
            model = self._get_model(model_type)
            
            prompt = f"""Sen bir LGS öğretmenisin. Öğrencinin yanlış cevabını analiz et:

SORU: {question_text}

ÖĞRENCİ CEVABI: {student_answer}
DOĞRU CEVAP: {correct_answer}

Lütfen:
1. Öğrencinin nerede hata yaptığını açıkla
2. Doğru çözüm yolunu göster
3. Bu tür hataları önlemek için ipuçları ver
4. Destekleyici ve motive edici ol

Açıklamayı öğrenciye hitap ederek yaz.
"""
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            st.error(f"Açıklama oluşturulamadı: {str(e)}")
            return "Açıklama şu anda hazırlanamıyor."
    
    def quick_analyze(
        self,
        image_input: Union[Image.Image, bytes, str],
        model_type: str = "flash"
    ) -> Dict[str, Any]:
        """
        Hızlı soru analizi (sadece özet).
        
        Args:
            image_input: Görsel
            model_type: Model tipi
            
        Returns:
            Dict: Hızlı analiz sonuçları
        """
        try:
            image = self._prepare_image(image_input)
            model = self._get_model(model_type)
            
            with st.spinner("⚡ Hızlı analiz yapılıyor..."):
                response = model.generate_content([QUICK_ANALYSIS_PROMPT, image])
                result = self._parse_json_response(response.text)
                result["model_used"] = model_type
                return result
                
        except Exception as e:
            st.error(f"Hızlı analiz hatası: {str(e)}")
            return {"error": str(e)}
    
    def detailed_analyze(
        self,
        image_input: Union[Image.Image, bytes, str],
        model_type: str = "pro"
    ) -> Dict[str, Any]:
        """
        Detaylı soru analizi (çözüm + diyagram).
        
        Args:
            image_input: Görsel
            model_type: Model tipi
            
        Returns:
            Dict: Detaylı analiz sonuçları
        """
        try:
            image = self._prepare_image(image_input)
            model = self._get_model(model_type)
            
            with st.spinner("🧠 Detaylı analiz yapılıyor..."):
                response = model.generate_content([DETAILED_ANALYSIS_PROMPT, image])
                result = self._parse_json_response(response.text)
                result["model_used"] = model_type
                return result
                
        except Exception as e:
            st.error(f"Detaylı analiz hatası: {str(e)}")
            return {"error": str(e)}

    def generate_variant(
        self,
        question_text: str,
        topic: str = "Bilinmiyor",
        difficulty: Union[int, str] = 3,
        model_type: str = "flash"
    ) -> Dict[str, Any]:
        """
        Verilen soruya benzer yeni bir soru (varyant) üretir.
        Adaptif alıştırma (JIT Learning) için kullanılır.
        
        Args:
            question_text: Orijinal soru metni
            topic: Konu
            difficulty: Zorluk seviyesi
            model_type: Model tipi
            
        Returns:
            Dict: Yeni soru (metin, seçenekler, cevap, çözüm)
        """
        try:
            model = self._get_model(model_type)
            
            prompt = self.VARIANT_GENERATION_PROMPT.format(
                question_text=question_text,
                topic=topic,
                difficulty=difficulty
            )
            
            with st.spinner("🔄 Benzer soru hazırlanıyor..."):
                response = model.generate_content(prompt)
                result = self._parse_json_response(response.text)
                
                # Metadata ekle
                result["original_question_ref"] = question_text[:50] + "..."
                
                # Timestamp için datetime importu gerekebilir, st.session_state'den alalım veya boş geçelim
                import datetime as dt_module
                result["generated_at"] = dt_module.datetime.now().isoformat()
                
                return result
                
        except Exception as e:
            st.error(f"Varyant üretim hatası: {str(e)}")
            return {"error": str(e)}
    
    def generate_hint(
        self,
        question_text: str,
        context: Optional[Dict] = None,
        model_type: str = "flash"
    ) -> Dict[str, str]:
        """
        Soru için ipucu üret (3 seviye).
        
        Args:
            question_text: Soru metni
            context: Ek bağlam
            model_type: Model tipi
            
        Returns:
            Dict: İpucu seviyeleri
        """
        try:
            model = self._get_model(model_type)
            
            prompt = f"""
            {HINT_GENERATOR_PROMPT}
            
            SORU: {question_text}
            """
            
            if context:
                prompt += f"\nBAĞLAM: {json.dumps(context, ensure_ascii=False)}"
            
            response = model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            st.error(f"İpucu üretilemedi: {str(e)}")
            return {
                "ipucu_seviye_1": "İpucu üretilemedi",
                "ipucu_seviye_2": "İpucu üretilemedi",
                "ipucu_seviye_3": "İpucu üretilemedi"
            }
    
    def explain_concept(
        self,
        concept: str,
        model_type: str = "flash"
    ) -> Dict[str, Any]:
        """
        Kavram açıklaması üret.
        
        Args:
            concept: Açıklanacak kavram
            model_type: Model tipi
            
        Returns:
            Dict: Kavram açıklaması
        """
        try:
            model = self._get_model(model_type)
            
            prompt = f"""
            {CONCEPT_EXPLAINER_PROMPT}
            
            KAVRAM: {concept}
            """
            
            response = model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            st.error(f"Kavram açıklanamadı: {str(e)}")
            return {"error": str(e)}


# Yardımcı fonksiyonlar
def format_solution_steps(steps: List[str]) -> str:
    """
    Çözüm adımlarını formatlar.
    
    Args:
        steps: Adım listesi
        
    Returns:
        str: Formatlanmış HTML
    """
    html = "<div class='solution-steps'>"
    for i, step in enumerate(steps, 1):
        html += f"""
        <div class='step'>
            <span class='step-number'>Adım {i}</span>
            <p>{step}</p>
        </div>
        """
    html += "</div>"
    return html


def get_difficulty_badge(level: int) -> str:
    """
    Zorluk seviyesi badge'i döndürür.
    
    Args:
        level: 1-5 arası zorluk seviyesi
        
    Returns:
        str: HTML badge
    """
    colors = {
        1: "#28A745",  # Yeşil
        2: "#5CB85C",  # Açık yeşil
        3: "#FFC107",  # Sarı
        4: "#FF9800",  # Turuncu
        5: "#DC3545"   # Kırmızı
    }
    
    labels = {
        1: "Çok Kolay",
        2: "Kolay",
        3: "Orta",
        4: "Zor",
        5: "Çok Zor"
    }
    
    color = colors.get(level, "#6C757D")
    label = labels.get(level, "Bilinmiyor")
    
    return f"""
    <span style='
        background-color: {color};
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
    '>
        {label}
    </span>
    """


# Singleton instance
@st.cache_resource(ttl=3600)  # 1 saat cache
def get_gemini_helper(api_key: Optional[str] = None) -> 'GeminiHelper':
    """
    GeminiHelper singleton instance'ı döndürür.
    
    API Key öncelik sırası:
    1. Argüman olarak verilen key
    2. UnifiedConfigManager (env -> secrets.toml -> user_settings.json)
    
    Fallback:
    - Kota aşılırsa otomatik olarak secondary key'e geçer
    """
    from utils.config_manager import get_config
    config = get_config()
    
    # 1. Argüman olarak gelen key
    if api_key:
        return GeminiHelper(api_key=api_key, config_manager=config)
    
    # 2. Config manager üzerinden (tüm kaynakları kontrol eder)
    return GeminiHelper(config_manager=config)
