"""
Audio Service - Sesli Öğretim Modülü
Edge-TTS (Primary) + gTTS (Fallback) + Gemini TTS (Optional)

Kullanım:
    from utils.audio_service import get_audio_service
    
    audio = get_audio_service()
    audio.speak_text("Merhaba, bu bir test.")
    audio.narrate_solution(solution_steps)
"""

import streamlit as st
from typing import Optional, List, Dict, Any
import io
import base64
import asyncio
from pathlib import Path

# Config manager
from utils.config_manager import get_config


class AudioService:
    """
    Sesli öğretim servisi.
    
    Primary: Edge-TTS (Microsoft Neural Voices - Ücretsiz, Hızlı, Kaliteli)
    Fallback 1: gTTS (Google TTS - Ücretsiz, Hızlı, Robotik)
    Fallback 2: Gemini TTS (Yavaş ama kaliteli)
    """
    
    # Türkçe Neural ses seçenekleri
    TURKISH_VOICES = {
        "female": "tr-TR-EmelNeural",      # Kadın sesi
        "male": "tr-TR-AhmetNeural",        # Erkek sesi
    }
    
    def __init__(self):
        self._config = get_config()
        self._edge_tts_available = False
        self._gtts_available = False
        self._gemini_available = False
        self._check_availability()
    
    def _check_availability(self):
        """Hangi TTS servislerinin kullanılabilir olduğunu kontrol et."""
        # Edge-TTS kontrolü (Primary)
        try:
            import edge_tts
            self._edge_tts_available = True
        except ImportError:
            self._edge_tts_available = False
        
        # gTTS kontrolü (Fallback 1)
        try:
            from gtts import gTTS
            self._gtts_available = True
        except ImportError:
            self._gtts_available = False
        
        # Gemini kontrolü (Fallback 2)
        try:
            from google import genai
            api_key = self._config.get_active_api_key()
            if api_key:
                self._gemini_available = True
        except:
            self._gemini_available = False
    
    def speak_text(
        self, 
        text: str, 
        language: str = "tr",
        voice: str = "female"
    ) -> Optional[bytes]:
        """
        Metni sese çevir.
        
        Args:
            text: Seslendirilecek metin
            language: Dil kodu (tr, en, etc.)
            voice: Ses tipi (female, male)
            
        Returns:
            Audio bytes (mp3) veya None
        """
        # 1. Edge-TTS (Primary - En iyi kalite, hızlı)
        if self._edge_tts_available:
            audio_data = self._speak_with_edge_tts(text, voice)
            if audio_data:
                return audio_data
            st.toast("⚠️ Edge-TTS başarısız, gTTS deneniyor...", icon="🔄")
        
        # 2. gTTS (Fallback 1 - Hızlı ama robotik)
        if self._gtts_available:
            audio_data = self._speak_with_gtts(text, language)
            if audio_data:
                return audio_data
            st.toast("⚠️ gTTS başarısız...", icon="🔄")
        
        # 3. Gemini TTS (Fallback 2 - Kaliteli ama yavaş)
        if self._gemini_available:
            st.toast("🔄 Gemini TTS deneniyor (bu biraz sürebilir)...", icon="⏳")
            audio_data = self._speak_with_gemini(text)
            if audio_data:
                return audio_data
        
        st.error("❌ Hiçbir TTS servisi kullanılamıyor.")
        return None
    
    def _speak_with_edge_tts(self, text: str, voice: str = "male") -> Optional[bytes]:
        """Edge-TTS ile seslendirme (Microsoft Neural Voices)."""
        try:
            import edge_tts
            
            # Ses seç (varsayılan: erkek - daha tok ve vurgulu)
            voice_name = self.TURKISH_VOICES.get(voice, self.TURKISH_VOICES["male"])
            
            # Daha doğal konuşma için ayarlar
            rate = "-10%"    # Biraz yavaşlat (daha tane tane)
            pitch = "+0Hz"   # Varsayılan ton
            
            # Async fonksiyonu sync olarak çalıştır
            async def _generate():
                communicate = edge_tts.Communicate(
                    text, 
                    voice_name,
                    rate=rate,
                    pitch=pitch
                )
                audio_buffer = io.BytesIO()
                
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_buffer.write(chunk["data"])
                
                audio_buffer.seek(0)
                return audio_buffer.read()
            
            # Event loop kontrolü - Streamlit bazen kendi loop'unu çalıştırır
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Loop zaten çalışıyor, yeni thread'de çalıştır
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, _generate())
                        return future.result(timeout=30)
                else:
                    return loop.run_until_complete(_generate())
            except RuntimeError:
                # Yeni loop oluştur
                return asyncio.run(_generate())
            
        except Exception as e:
            print(f"Edge-TTS Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _speak_with_gtts(self, text: str, language: str = "tr") -> Optional[bytes]:
        """gTTS ile seslendirme (fallback)."""
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Bytes olarak kaydet
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.read()
            
        except Exception as e:
            print(f"gTTS Error: {e}")
            return None
    
    def _speak_with_gemini(self, text: str) -> Optional[bytes]:
        """Gemini TTS ile seslendirme (yavaş fallback)."""
        try:
            from google import genai
            from google.genai import types
            import wave
            
            api_key = self._config.get_active_api_key()
            if not api_key:
                return None
            
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Aoede"
                            )
                        )
                    )
                )
            )
            
            if response.candidates and response.candidates[0].content.parts:
                part = response.candidates[0].content.parts[0]
                if hasattr(part, 'inline_data') and part.inline_data:
                    pcm_data = part.inline_data.data
                    
                    if isinstance(pcm_data, str):
                        pcm_data = base64.b64decode(pcm_data)
                    
                    # PCM → WAV
                    wav_buffer = io.BytesIO()
                    with wave.open(wav_buffer, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(24000)
                        wf.writeframes(pcm_data)
                    
                    wav_buffer.seek(0)
                    return wav_buffer.read()
            
            return None
            
        except Exception as e:
            print(f"Gemini TTS Error: {e}")
            return None
    
    def narrate_solution(
        self, 
        solution_steps: List[str],
        intro: str = "Şimdi çözümü adım adım anlatacağım."
    ) -> Optional[bytes]:
        """Çözüm adımlarını sesli anlat."""
        full_text = intro + " "
        
        for i, step in enumerate(solution_steps, 1):
            full_text += f"Adım {i}: {step}. "
        
        full_text += "Çözüm tamamlandı."
        
        return self.speak_text(full_text)
    
    def get_status(self) -> Dict[str, bool]:
        """Servis durumunu döndür."""
        return {
            "edge_tts": self._edge_tts_available,
            "gtts": self._gtts_available,
            "gemini_tts": self._gemini_available
        }


# Singleton
@st.cache_resource
def get_audio_service() -> AudioService:
    """Global audio service instance."""
    return AudioService()
