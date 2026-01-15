"""
LLM Adapter Layer
Vendor lock-in riskini azaltmak için LLM servis katmanı.
Şu an Gemini kullanıyor, ancak ileride OpenAI, Anthropic veya Local LLM'e geçişi kolaylaştırır.
"""

from typing import Dict, Any, Optional, List, Union
import streamlit as st
import json
from pathlib import Path
from utils.gemini_helper import get_gemini_helper
from prompts.content_generation_prompts import (
    FICHE_GENERATION_TASK_DESCRIPTIONS,
    FICHE_GENERATION_PROMPT_TEMPLATE,
    QUESTION_EXTRACTION_TASK_DESCRIPTIONS,
    QUESTION_EXTRACTION_PROMPT_TEMPLATE,
    FIGURE_CLASSIFICATION_PROMPT_TEMPLATE,
    JIT_QUESTION_GENERATION_PROMPT_TEMPLATE
)

class LLMAdapter:
    """
    LLM Sağlayıcısı için soyutlama katmanı.
    """
    
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self.gemini = get_gemini_helper()
        
    def load_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Prompts klasöründen şablon yükler ve formatlar.
        """
        try:
            # Proje kök dizinini bul (utils'in bir üstü)
            root_dir = Path(__file__).parent.parent
            prompt_path = root_dir / "prompts" / prompt_name
            
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()
            print(f"DEBUG TEMPLATE: '{template}'")
            return template.format(**kwargs)
        except Exception as e:
            st.error(f"Prompt Yükleme Hatası ({prompt_name}): {e}")
            return ""
        
    def generate_json(self, prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        LLM'den JSON formatında yanıt alır.
        
        Args:
            prompt (str): İstek metni
            model (str): Model ismi (Opsiyonel)
            
        Returns:
            Dict: JSON yanıtı
        """
        if self.provider == "gemini":
            return self._generate_json_gemini(prompt, model)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented yet.")

    def chat(self, prompt: str, history: Optional[List[Dict]] = None, model: Optional[str] = None) -> str:
        """
        LLM ile sohbet eder (metin yanıtı).
        
        Args:
            prompt (str): Kullanıcı mesajı
            history (List): Sohbet geçmişi
            model (str): Model ismi
            
        Returns:
            str: Yanıt metni
        """
        if self.provider == "gemini":
            return self._chat_gemini(prompt, history, model)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented yet.")

    def vision_analyze(self, image: Any, prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Görsel analizi yapar.
        
        Args:
            image: PIL Image veya bytes
            prompt: Analiz talimatı
            
        Returns:
            Dict: Analiz sonucu (Genelde JSON istenir)
        """
        if self.provider == "gemini":
            return self._vision_analyze_gemini(image, prompt, model)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented yet.")

    # --- Gemini Implementasyonları ---
    
    def _generate_json_gemini(self, prompt: str, model_name: Optional[str]) -> Dict[str, Any]:
        """Gemini kullanarak JSON üretir."""
        # GeminiHelper'daki metodları kullan veya direkt API çağır
        # GeminiHelper zaten yapılandırılmış, onu kullanmak en temizi
        
        # Not: GeminiHelper'da direkt 'generate_json' yoksa burada implemente edebiliriz
        # veya GeminiHelper'a ekleyebiliriz. Şimdilik GeminiHelper'ın modelini alıp
        # generate_content çağıracağız.
        
        model = self.gemini._get_model("pro") # Varsayılan Pro
        
        # JSON zorlama promptu ekle (Eğer promptta yoksa)
        if "JSON" not in prompt:
            prompt += "\n\nLütfen yanıtı sadece geçerli bir JSON formatında ver."
            
        try:
            response = model.generate_content(prompt)
            text = response.text
            
            # Markdown temizliği (```json ... ```)
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text.strip())
            
        except Exception as e:
            st.error(f"LLM JSON Hatası: {e}")
            return {}

    def _chat_gemini(self, prompt: str, history: Optional[List[Dict]], model_name: Optional[str]) -> str:
        """Gemini ile sohbet."""
        # Model seçimi (Varsayılan Flash)
        model_type = "flash" if not model_name else model_name
        model = self.gemini._get_model(model_type)
        
        # History formatı Gemini'ye uygun mu?
        gemini_history = []
        if history:
            for msg in history:
                role = "user" if msg.get("role") == "user" else "model"
                gemini_history.append({
                    "role": role,
                    "parts": [msg.get("content", "")]
                })
        
        # Güvenlik Ayarları (Crash önlemek için BLOCK_NONE)
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        try:
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(prompt, safety_settings=safety_settings)
            
            # response.text erişimi bazen hata verebilir (boş part)
            try:
                return response.text
            except ValueError:
                # Feedback kontrolü
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                    return f"Safety Block: {response.prompt_feedback}"
                # Candidate kontrolü
                if response.candidates:
                    finish_reason = response.candidates[0].finish_reason
                    return f"Model durdu (Sebep: {finish_reason}). Yanıt boş."
                return "Hata: Model boş yanıt döndürdü."
                
        except Exception as e:
            return f"LLM Hatası: {str(e)}"

    def _vision_analyze_gemini(self, image: Any, prompt: str, model_name: Optional[str]) -> Dict[str, Any]:
        """Gemini ile görsel analiz."""
        return self.gemini.analyze_image(image, prompt)


    def generate_content_fiches_from_images(self, images: List[bytes], lesson: str, topic: str, subtopic: str, publisher: Optional[str] = None, source_type: str = "ai_generated") -> Dict[str, Any]:
        """
        Görsellerden içerik fişi üretir (Multimodal).
        source_type: 'publisher_original', 'ai_variant_of_publisher', 'ai_generated'
        """
        
        
        task_description = FICHE_GENERATION_TASK_DESCRIPTIONS.get(
            source_type, 
            FICHE_GENERATION_TASK_DESCRIPTIONS["ai_generated"]
        )
            
        prompt = FICHE_GENERATION_PROMPT_TEMPLATE.format(
            task_description=task_description,
            lesson=lesson,
            topic=topic,
            subtopic=subtopic
        )
        
        # Gemini Pro Vision (veya 1.5 Flash) kullanımı
        # GeminiHelper üzerinden çağırmak lazım ama helper metodumuz text/image ayrımını nasıl yapıyor?
        # Helper'a 'analyze_image' benzeri ama çoklu resim destekleyen bir metod lazım.
        # Şimdilik direkt model objesine erişip generate_content diyeceğiz.
        
        try:
            model = self.gemini._get_model("flash") # Flash daha hızlı ve multimodal için iyi
            
            content_parts = [prompt]
            
            # Resimleri ekle
            import PIL.Image
            import io
            
            for img_bytes in images:
                image = PIL.Image.open(io.BytesIO(img_bytes))
                content_parts.append(image)
            
            # Güvenlik ayarları (BLOCK_NONE)
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            # Generasyon ayarları
            generation_config = {
                "temperature": 0.2,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json" # JSON mode
            }
                
            response = model.generate_content(
                content_parts,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            try:
                text = response.text
            except ValueError:
                # Eğer response.text hata verirse (FinishReason yüzünden)
                feedback = response.prompt_feedback
                finish_reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
                st.error(f"LLM Yanıt Vermedi. Finish Reason: {finish_reason}. Feedback: {feedback}")
                return {"fiches": []}
            
            # JSON Temizliği (JSON mode kullansak bile bazen markdown gelebilir)
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text.strip())
            
        except Exception as e:
            st.error(f"Fiş Üretme Hatası: {e}")
            return {"fiches": []}

    def generate_questions_from_images(self, images: List[bytes], lesson: str, topic: str, subtopic: str, publisher: Optional[str] = None, source_type: str = "ai_generated") -> Dict[str, Any]:
        """
        Görsellerden soru üretir/ayrıştırır.
        """
        task_description = QUESTION_EXTRACTION_TASK_DESCRIPTIONS.get(
            source_type,
            QUESTION_EXTRACTION_TASK_DESCRIPTIONS["ai_generated"]
        )
            
        prompt = QUESTION_EXTRACTION_PROMPT_TEMPLATE.format(
            task_description=task_description,
            lesson=lesson,
            topic=topic,
            subtopic=subtopic
        )
        
        try:
            # Kullanıcı isteği üzerine Flash'a dönüş, ancak token limiti yüksek kalsın
            model = self.gemini._get_model("flash")
            content_parts = [prompt]
            
            import PIL.Image
            import io
            for img_bytes in images:
                image = PIL.Image.open(io.BytesIO(img_bytes))
                content_parts.append(image)
                
            # Güvenlik ayarları
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            generation_config = {
                "temperature": 0.1, 
                "max_output_tokens": 16384, # Limit artırıldı
                "response_mime_type": "application/json"
            }
                
            response = model.generate_content(
                content_parts,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            try:
                text = response.text
            except Exception as e:
                # FinishReason yüzünden hata verirse (örn: MaxTokens veya Safety)
                # Hata mesajını loglayalım ama kullanıcıya göstermeden kurtarmaya çalışalım
                print(f"DEBUG: response.text error: {e}")
                
                if response.candidates and response.candidates[0].content.parts:
                    text = response.candidates[0].content.parts[0].text
                    st.warning("⚠️ Uyarı: Yanıt çok uzun olduğu için kesildi (Max Tokens). Eksik sorular olabilir.")
                else:
                    finish_reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
                    st.error(f"Soru Ayrıştırma Hatası: Model yanıt döndüremedi. (Sebep: {finish_reason}). Lütfen daha az sayfa yüklemeyi deneyin.")
                    return {"questions": []}
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text.strip())
            
        except Exception as e:
            st.error(f"Soru Ayrıştırma Hatası: {e}")
            return {"questions": []}

        except Exception as e:
            st.error(f"Soru Üretme Hatası: {e}")
            return {"questions": []}

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Metin içinden JSON bloğunu bulup çıkarmaya çalışır.
        """
        import re
        
        # 1. Markdown Code Block (```json ... ```)
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            # 2. Markdown Code Block (``` ... ```) - dil belirtilmemiş
            match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                # 3. Süslü parantez aralığı ({ ... })
                match = re.search(r"\{.*\}", text, re.DOTALL)
                if match:
                    json_str = match.group(0)
                else:
                    # Hiçbir şey bulamazsa ham metni dene
                    json_str = text

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Basit temizlik denemeleri
            # Bazen satır sonları sorun yaratır
            try:
                # Control characters temizle
                clean_str = "".join(ch for ch in json_str if ord(ch) >= 32 or ch == '\n' or ch == '\r' or ch == '\t')
                return json.loads(clean_str)
            except:
                pass
            raise # İlk hatayı fırlat

    def classify_has_figure(self, text: str, options: Dict[str, str], image: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Sorunun şekil içerip içermediğini analiz eder.
        """
        prompt = FIGURE_CLASSIFICATION_PROMPT_TEMPLATE.format(
            text=text,
            options_json=json.dumps(options, ensure_ascii=False)
        )
        
        try:
            model = self.gemini._get_model("flash")
            content_parts = [prompt]
            
            if image:
                import PIL.Image
                import io
                img = PIL.Image.open(io.BytesIO(image))
                content_parts.append(img)
                
            response = model.generate_content(content_parts)
            return self._extract_json(response.text)
            
        except Exception as e:
            print(f"Classification Error: {e}")
            return {"has_figure": False, "figure_type": "none", "confidence": 0.0, "reason": "Error"}

    def generate_questions_from_text(self, text_content: str, lesson: str, topic: str, subtopic: str, count: int = 5) -> Dict[str, Any]:
        """
        Metin içeriğinden (fişlerden) soru üretir.
        """
        prompt = JIT_QUESTION_GENERATION_PROMPT_TEMPLATE.format(
            count=count,
            lesson=lesson,
            topic=topic,
            subtopic=subtopic,
            text_content=text_content[:10000] # Token limitine takılmamak için kırpıyoruz
        )
        
        try:
            model = self.gemini._get_model("flash")
            
            # Güvenlik ayarları
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            generation_config = {
                "temperature": 0.3, 
                "max_output_tokens": 8192,
                "response_mime_type": "application/json"
            }
                
            response = model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            return self._extract_json(response.text)
            
        except Exception as e:
            # Hata detayını kullanıcıya gösterme, logla
            print(f"JIT Error: {e}")
            # st.error(f"Soru Üretme Hatası: {e}") # Kullanıcıya gösterme
            return {"questions": []}

    # ─────────────────────────────────────────────────────────────────────────
    # BETA MODU (Scaffolding + Perplexity Critic)
    # ─────────────────────────────────────────────────────────────────────────
    
    def _call_perplexity_critic(self, question: str, steps: str, proposed_answer: str, image_data: bytes = None) -> Dict[str, Any]:
        """
        Perplexity API'ye bağlanıp çözümü denetletir.
        Artık görsel de gönderilebilir (Multimodal).
        """
        # Varsayılan fallback yanıtı
        DEFAULT_RESPONSE = {
            "verification_status": "unavailable", 
            "critic_note": "Denetim yapılamadı"
        }
        
        from utils.config_manager import get_config
        config = get_config()
        api_key = config.get_perplexity_api_key()
        
        if not api_key:
            print("BETA: Perplexity API key bulunamadı, critic atlanıyor.")
            return {**DEFAULT_RESPONSE, "critic_note": "API key eksik"}
        
        from prompts.beta_prompts import PERPLEXITY_CRITIC_PROMPT, PERPLEXITY_CRITIC_SYSTEM
        
        prompt = PERPLEXITY_CRITIC_PROMPT.format(
            question=question,
            steps=steps if steps else "Adımlar belirtilmedi",
            proposed_answer=proposed_answer
        )
        
        try:
            import requests
            import base64
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Mesaj içeriğini hazırla
            user_content = []
            
            # Görsel varsa base64 olarak ekle
            if image_data:
                b64_image = base64.b64encode(image_data).decode('utf-8')
                image_size_kb = len(image_data) / 1024
                print(f"BETA: Görsel boyutu: {image_size_kb:.1f} KB, base64 uzunluğu: {len(b64_image)} karakter")
                
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64_image}"
                    }
                })
                print("BETA: Görsel Perplexity'ye gönderiliyor...")
            
            # Metin promptunu ekle
            user_content.append({
                "type": "text",
                "text": prompt
            })
            
            payload = {
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": PERPLEXITY_CRITIC_SYSTEM},
                    {"role": "user", "content": user_content}
                ],
                "max_tokens": 2000,  # Artırıldı (kesilme önlenmesi için)
                "temperature": 0.2
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                raw_content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # DEBUG: Ham yanıtı logla
                print(f"DEBUG - Perplexity Raw Response: {raw_content[:500]}")
                
                # JSON Temizliği (Markdown blokları temizle)
                cleaned_content = self._clean_json_string(raw_content)
                
                # JSON parse dene
                try:
                    parsed = json.loads(cleaned_content)
                    
                    # Esnek anahtar kontrolü (.get ile)
                    return {
                        "verification_status": parsed.get("verification_status", parsed.get("status", "unknown")),
                        "critic_note": parsed.get("critic_note", parsed.get("note", "")),
                        "suggested_answer": parsed.get("suggested_answer", "")
                    }
                except json.JSONDecodeError as e:
                    print(f"BETA: JSON parse hatası: {e}")
                    print(f"BETA: Temizlenmiş içerik: {cleaned_content[:300]}")
                    # Parse edilemezse ham metni not olarak döndür
                    return {
                        "verification_status": "parse_error", 
                        "critic_note": raw_content[:200] if raw_content else "Boş yanıt"
                    }
            else:
                print(f"BETA: Perplexity API hatası: {response.status_code} - {response.text[:200]}")
                return {**DEFAULT_RESPONSE, "critic_note": f"API Error: {response.status_code}"}
                
        except requests.exceptions.Timeout:
            print("BETA: Perplexity timeout")
            return {**DEFAULT_RESPONSE, "critic_note": "Timeout"}
        except Exception as e:
            print(f"BETA: Perplexity exception: {e}")
            return {**DEFAULT_RESPONSE, "critic_note": str(e)[:100]}
    
    def _clean_json_string(self, text: str) -> str:
        """
        Markdown kod bloklarını ve gereksiz karakterleri temizler.
        Örn: ```json {...} ``` -> {...}
        Ayrıca başında { olmayan JSON-like metinleri düzeltir.
        """
        if not text:
            return "{}"
        
        cleaned = text.strip()
        
        # Markdown JSON bloğunu temizle
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            parts = cleaned.split("```")
            if len(parts) >= 2:
                cleaned = parts[1]
        
        # Baştaki/sondaki boşlukları temizle
        cleaned = cleaned.strip()
        
        # Eğer { ile başlamıyorsa
        if not cleaned.startswith("{"):
            # { bulmaya çalış
            start_idx = cleaned.find("{")
            if start_idx != -1:
                cleaned = cleaned[start_idx:]
            else:
                # { yoksa ama "key": ile başlıyorsa, { ekle
                if cleaned.startswith('"') and '":' in cleaned:
                    cleaned = "{" + cleaned
        
        # Eğer } ile bitmiyorsa, son }'yi bul
        if not cleaned.endswith("}"):
            end_idx = cleaned.rfind("}")
            if end_idx != -1:
                cleaned = cleaned[:end_idx + 1]
            else:
                # } yoksa ekle
                if cleaned.startswith("{"):
                    cleaned = cleaned + "}"
        
        return cleaned
    
    def _repair_truncated_json(self, text: str) -> str:
        """
        Kesilmiş/eksik JSON'u onarmaya çalışır.
        Örn: {"steps": ["a", "b  -> {"steps": ["a", "b"]}
        """
        if not text:
            return "{}"
        
        repaired = text.strip()
        
        # Açık string'leri kapat
        # Son açık tırnak varsa kapat
        quote_count = repaired.count('"')
        if quote_count % 2 != 0:
            repaired += '"'
        
        # Açık array'leri kapat
        open_brackets = repaired.count('[')
        close_brackets = repaired.count(']')
        repaired += ']' * (open_brackets - close_brackets)
        
        # Açık object'leri kapat
        open_braces = repaired.count('{')
        close_braces = repaired.count('}')
        repaired += '}' * (open_braces - close_braces)
        
        # Trailing comma temizle (geçersiz JSON yapar)
        import re
        repaired = re.sub(r',\s*]', ']', repaired)
        repaired = re.sub(r',\s*}', '}', repaired)
        
        return repaired

    def generate_beta_scaffolded_analysis(self, question_text: str, image_data: Any = None) -> Dict[str, Any]:
        """
        Beta Modu: Adım adım çözüm (Scaffolding) + Perplexity doğrulaması.
        
        Returns:
            Dict: {
                "steps": ["Adım 1...", "Adım 2..."],
                "final_answer": "Doğru Cevap: C",
                "confidence": 95,
                "verification": {"status": "confirmed" | "disputed" | "unavailable", ...},
                "status": "success" | "fallback"
            }
        """
        from prompts.beta_prompts import BETA_SOLVER_SYSTEM_PROMPT
        
        # 1. Gemini'den JSON formatında adım adım çözüm al
        full_prompt = f"{BETA_SOLVER_SYSTEM_PROMPT}\n\nSORU:\n{question_text}"
        
        try:
            model = self.gemini._get_model("flash")
            
            content_parts = [full_prompt]
            
            # Görsel varsa ekle
            if image_data:
                import PIL.Image
                import io
                if isinstance(image_data, bytes):
                    image = PIL.Image.open(io.BytesIO(image_data))
                    content_parts.append(image)
                elif hasattr(image_data, 'read'):
                    image = PIL.Image.open(image_data)
                    content_parts.append(image)
            
            # Güvenlik ayarları
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            generation_config = {
                "temperature": 0.3,
                "max_output_tokens": 8192,  # Artırıldı
                "response_mime_type": "application/json"
            }
            
            response = model.generate_content(
                content_parts,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            # DEBUG: Gemini ham yanıtını logla
            print(f"DEBUG - Gemini Raw Response: {response.text[:500]}")
            
            # JSON parse - _clean_json_string kullan
            cleaned_response = self._clean_json_string(response.text)
            print(f"DEBUG - Cleaned Response: {cleaned_response[:300]}")
            
            try:
                solution = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                print(f"DEBUG - JSON Parse Error: {e}")
                # Kesilmiş JSON'u onarmaya çalış
                repaired_json = self._repair_truncated_json(cleaned_response)
                try:
                    solution = json.loads(repaired_json)
                    print(f"DEBUG - Repaired JSON successful")
                except json.JSONDecodeError:
                    print(f"DEBUG - Repair failed, using fallback")
                    # Son çare: düz metin döndür
                    return {
                        "steps": ["Gemini yanıtı tamamlanamadı, lütfen tekrar deneyin."],
                        "final_answer": response.text[:300] if response.text else "Yanıt alınamadı",
                        "confidence": 0,
                        "verification": {"verification_status": "unavailable"},
                        "status": "truncated"
                    }
            
            if not solution or "steps" not in solution:
                # Fallback: düz metin döndür
                print(f"DEBUG - No steps found, falling back")
                return {
                    "steps": [],
                    "final_answer": response.text[:500] if response.text else "Yanıt alınamadı",
                    "confidence": 0,
                    "verification": {"verification_status": "unavailable"},
                    "status": "fallback"
                }
            
            # 2. Perplexity Critic'e gönder - Adımları ve görseli de gönder
            steps_text = "\n".join([f"- {s}" for s in solution.get("steps", [])])
            verification = self._call_perplexity_critic(
                question=question_text,
                steps=steps_text,
                proposed_answer=solution.get("final_answer", ""),
                image_data=image_data  # Görseli de gönder
            )
            
            # 3. Sonucu birleştir - verification her zaman dict olmalı
            if not isinstance(verification, dict):
                verification = {"verification_status": "unavailable", "critic_note": str(verification)}
            
            solution["verification"] = verification
            solution["status"] = "success"
            
            # Eğer critic dispute ettiyse uyarı ekle
            if verification.get("verification_status") == "disputed":
                solution["warning"] = verification.get("critic_note", "Denetçi farklı düşünüyor")
            
            return solution
            
        except Exception as e:
            import traceback
            print(f"BETA Error: {e}")
            print(f"BETA Traceback: {traceback.format_exc()}")
            return {
                "steps": [],
                "final_answer": f"Hata oluştu: {str(e)[:100]}",
                "confidence": 0,
                "verification": {"verification_status": "unavailable"},
                "status": "error"
            }

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Basit metin üretimi."""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUSER: {prompt}"
            
        return self._chat_gemini(full_prompt, history=[], model_name="flash")

    def generate_graphviz(self, lesson: str, topic: str, subtopic: str, context: str = "") -> str:
        """Graphviz (DOT) diyagramı üretir."""
        system_prompt = f"""
        GÖREV: Aşağıdaki konu için öğrencilerin konuyu anlamasını kolaylaştıracak bir Graphviz (DOT) diyagramı oluştur.
        
        DERS: {lesson}
        KONU: {topic}
        ALT KONU: {subtopic}
        
        BAĞLAM (İÇERİK ÖZETİ):
        {context}
        
        KURALLAR:
        1. Çıktı geçerli bir DOT formatında olmalıdır (digraph G {{ ... }}).
        2. 'node [fontname="Arial", shape=box, style=filled, fillcolor="#E3F2EF", color="#2D6A4F"];' ayarını kullan (Türkçe karakter ve stil için).
        3. Kenarlar (edges) için basit etiketler kullanabilirsin.
        4. Çıktı olarak SADECE DOT kodunu ver. Kod blokları (```dot) kullanma.
        5. Karmaşık olmasın, hiyerarşik bir yapı (rankdir=TB) kullan.
        """
        
        response = self.generate(f"{topic} - {subtopic} için kavram haritası (DOT) oluştur.", system_prompt=system_prompt)
        
        # Temizlik
        if "```dot" in response:
            response = response.split("```dot")[1].split("```")[0]
        elif "```graphviz" in response:
            response = response.split("```graphviz")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
            
        return response.strip()

    def generate_flashcards(self, lesson: str, topic: str, subtopic: str, context: str) -> List[Dict[str, str]]:
        """İçerikten bilgi kartları üretir."""
        system_prompt = f"""
        GÖREV: Aşağıdaki LGS konu anlatımını kullanarak öğrenciler için 5 adet BİLGİ KARTI (Flashcard) üret.
        
        DERS: {lesson}
        KONU: {topic}
        ALT KONU: {subtopic}
        
        BAĞLAM (İÇERİK ÖZETİ):
        {context}
        
        KURALLAR:
        1. Sorular KISA ve NET olmalı (örn: "Üslü sayılarda çarpma işleminde üsler ne yapılır?").
        2. Cevaplar KISA ve NET olmalı (örn: "Toplanır").
        3. Asla "Özet nedir?" gibi genel sorular sorma. Nokta atışı bilgi sor.
        4. Çıktı JSON formatında olsun: [ {{"front": "Soru", "back": "Cevap"}} ]
        """
        
        response = self.generate("Bana bu konudan 5 tane kısa bilgi kartı (JSON) ver.", system_prompt=system_prompt)
        
        import json
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response.strip())
        except Exception as e:
            st.error(f"Kart üretme JSON hatası: {e}")
            return []

# Singleton
@st.cache_resource
def get_llm_adapter() -> LLMAdapter:
    return LLMAdapter(provider="gemini")
