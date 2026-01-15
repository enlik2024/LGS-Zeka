"""
Sokratik Dialog Manager
LGS-Zeka AI Koçu için JSON tabanlı etkileşim yöneticisi
"""

import streamlit as st
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from utils.llm_adapter import get_llm_adapter
from utils.gamification import get_gamification_manager
from prompts.teaching_prompts import SOCRATIC_MASTER_PROMPT


class SocraticManager:
    """
    Sokratik öğretim için dialog yöneticisi.
    Master prompt'a göre JSON çıktı formatı kullanır.
    """
    
    MASTER_PROMPT = SOCRATIC_MASTER_PROMPT
    
    def __init__(self):
        """Manager başlatıcı."""
        self.llm = get_llm_adapter()
        self.gm = get_gamification_manager()
    
    def get_socratic_response(
        self,
        user_message: str,
        context: Dict[str, Any],
        chat_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Kullanıcı mesajına Sokratik yanıt al.
        """
        try:
            # Prompt oluştur
            prompt = self._build_prompt(user_message, context, chat_history)
            
            # LLM Adapter üzerinden yanıt al (JSON)
            response_json = self.llm.generate_json(prompt)
            
            return response_json

        except Exception as e:
            st.error(f"Sokratik yanıt hatası: {e}")
            return self._fallback_response(user_message)
            
        except Exception as e:
            # Detaylı hata mesajı
            error_details = f"Hata türü: {type(e).__name__}\nMesaj: {str(e)}"
            st.error(f"❌ Sokratik yanıt hatası:\n{error_details}")
            
            # Hata detaylarını expander'da göster
            with st.expander("🔍 Hata Detayları"):
                st.exception(e)
            
            return self._fallback_response(user_message)
    
    def _build_prompt(
        self,
        user_message: str,
        context: Dict[str, Any],
        chat_history: Optional[List[Dict]] = None
    ) -> str:
        """Prompt oluştur."""
        prompt = f"{self.MASTER_PROMPT}\n\n"
        prompt += "SORU BAĞLAMI:\n"
        prompt += f"Konu: {context.get('konu', 'Bilinmiyor')}\n"
        prompt += f"Zorluk: {context.get('zorluk', 'Orta')}\n"
        prompt += f"Doğru Cevap: {context.get('dogru_cevap', '?')} (Öğrenciye söyleme!)\n\n"
        
        if chat_history:
            prompt += "SOHBET GEÇMİŞİ:\n"
            for msg in chat_history[-5:]:  # Son 5 mesaj (Artırıldı)
                role = "Öğrenci" if msg['role'] == 'user' else "Sen"
                prompt += f"{role}: {msg['content']}\n"
            prompt += "\n"
        
        prompt += f"ÖĞRENCİ MESAJI: {user_message}\n\n"
        prompt += "ÖNEMLİ: Sadece JSON formatında yanıt ver, başka metin ekleme!"
        
        return prompt
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """JSON yanıtı parse et."""
        try:
            # Markdown code block'larını temizle
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            # JSON parse
            return json.loads(cleaned)
            
        except json.JSONDecodeError as e:
            st.warning(f"JSON parse hatası: {str(e)}")
            # Fallback: Basit JSON oluştur
            return {
                "ui_mode": "dialog",
                "content": {
                    "message_text": response_text,
                    "voice_tone": "encouraging"
                },
                "visual_aid": {"required": False},
                "learning_artifacts": {
                    "flashcards": [],
                    "missing_knowledge_tag": "",
                    "difficulty_level": 3
                },
                "interaction": {
                    "suggested_options": [],
                    "quiz_question": None
                },
                "gamification": {
                    "xp_award": 5,
                    "streak_bonus": False,
                    "toast_message": "Devam et! 💪"
                }
            }
    
    def _apply_gamification(self, gamification_data: Dict[str, Any]):
        """Gamification verilerini uygula."""
        xp_award = gamification_data.get('xp_award', 0)
        toast_message = gamification_data.get('toast_message', '')
        
        if xp_award > 0:
            self.gm.add_xp(xp_award, toast_message)
    
    def _fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Hata durumunda fallback yanıt."""
        return {
            "ui_mode": "dialog",
            "content": {
                "message_text": f"Mesajını aldım: '{user_message}'\n\nBu konuda sana nasıl yardımcı olabilirim? 🤔",
                "voice_tone": "encouraging"
            },
            "visual_aid": {"required": False},
            "learning_artifacts": {
                "flashcards": [],
                "missing_knowledge_tag": "",
                "difficulty_level": 3
            },
            "interaction": {
                "suggested_options": [
                    "Konuyu açıkla",
                    "Örnek ver",
                    "İpucu ver"
                ],
                "quiz_question": None
            },
            "gamification": {
                "xp_award": 5,
                "streak_bonus": False,
                "toast_message": "Sohbet devam ediyor! 💬"
            }
        }


# Singleton instance
@st.cache_resource
def get_socratic_manager() -> SocraticManager:
    """
    SocraticManager singleton instance döndürür.
    
    Returns:
        SocraticManager: Manager instance
    """
    return SocraticManager()
