"""
Unified Configuration Manager
Tüm konfigürasyonların tek erişim noktası.

FAZ 1: Teknik Temizlik
- Çoklu API key fallback desteği
- Model cascading
- Merkezi config yönetimi
"""

import yaml
import os
from pathlib import Path
from typing import Any, Dict, Optional, List
import streamlit as st
from dataclasses import dataclass
from enum import Enum


class APIKeyStatus(Enum):
    """API key durumları."""
    ACTIVE = "active"
    QUOTA_EXCEEDED = "quota_exceeded"
    INVALID = "invalid"
    NOT_SET = "not_set"


@dataclass
class APIKeyInfo:
    """API key bilgisi."""
    key: str
    status: APIKeyStatus = APIKeyStatus.ACTIVE
    name: str = "primary"


class UnifiedConfigManager:
    """
    Tek merkezi config yöneticisi.
    
    Öncelik sırası:
    1. Environment variables
    2. Streamlit secrets (secrets.toml)
    3. App config (app_config.yaml)
    4. Feature flags (feature_flags.yaml)
    
    Özellikler:
    - Çoklu API key fallback
    - Model cascading
    - Dot notation erişim
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.config_dir = Path(__file__).parent.parent / "config"
        self._app_config = self._load_yaml("app_config.yaml")
        self._feature_flags = self._load_yaml("feature_flags.yaml")
        self._api_keys: List[APIKeyInfo] = []
        self._current_key_index = 0
        self._load_api_keys()
        self._initialized = True
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """YAML dosyasını yükle."""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Config Load Error ({filename}): {e}")
            return {}
    
    def _load_api_keys(self) -> None:
        """Tüm API key'leri yükle (fallback sırasıyla)."""
        keys = []
        
        # 1. Environment variable
        env_key = os.environ.get("GEMINI_API_KEY")
        if env_key:
            keys.append(APIKeyInfo(key=env_key, name="env_primary"))
        
        env_key_secondary = os.environ.get("GEMINI_API_KEY_SECONDARY")
        if env_key_secondary:
            keys.append(APIKeyInfo(key=env_key_secondary, name="env_secondary"))
        
        # 2. Streamlit secrets
        try:
            gemini_secrets = st.secrets.get("gemini", {})
            
            # Primary key
            primary = gemini_secrets.get("api_key")
            if primary and not any(k.key == primary for k in keys):
                keys.append(APIKeyInfo(key=primary, name="secrets_primary"))
            
            # Secondary key (fallback)
            secondary = gemini_secrets.get("api_key_secondary")
            if secondary and not any(k.key == secondary for k in keys):
                keys.append(APIKeyInfo(key=secondary, name="secrets_secondary"))
                
            # Tertiary key (fallback 2)
            tertiary = gemini_secrets.get("api_key_tertiary")
            if tertiary and not any(k.key == tertiary for k in keys):
                keys.append(APIKeyInfo(key=tertiary, name="secrets_tertiary"))
                
        except Exception:
            pass
        
        # 3. Ayarlar sayfasından kaydedilen key (user_settings.json)
        try:
            settings_path = self.config_dir / "user_settings.json"
            if settings_path.exists():
                import json
                with open(settings_path, "r") as f:
                    settings = json.load(f)
                    
                    # Primary key from user settings
                    user_key = settings.get("chat_api_key")
                    if user_key and not any(k.key == user_key for k in keys):
                        keys.append(APIKeyInfo(key=user_key, name="ayarlar_primary"))
                    
                    # Secondary key from user settings
                    user_key_secondary = settings.get("chat_api_key_secondary")
                    if user_key_secondary and not any(k.key == user_key_secondary for k in keys):
                        keys.append(APIKeyInfo(key=user_key_secondary, name="ayarlar_secondary"))
                        
                    # Tertiary key from user settings
                    user_key_tertiary = settings.get("chat_api_key_tertiary")
                    if user_key_tertiary and not any(k.key == user_key_tertiary for k in keys):
                        keys.append(APIKeyInfo(key=user_key_tertiary, name="ayarlar_tertiary"))
        except Exception:
            pass
        
        self._api_keys = keys
    
    # ─────────────────────────────────────────────────────────────────────────
    # API KEY YÖNETİMİ (Çoklu Key Fallback)
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_active_api_key(self) -> Optional[str]:
        """Aktif API key'i döndür."""
        if not self._api_keys:
            return None
        
        # Geçerli index'teki key'i döndür
        while self._current_key_index < len(self._api_keys):
            key_info = self._api_keys[self._current_key_index]
            if key_info.status == APIKeyStatus.ACTIVE:
                return key_info.key
            self._current_key_index += 1
        
        return None
    
    def mark_key_quota_exceeded(self) -> bool:
        """
        Mevcut key'i kota aşıldı olarak işaretle ve sonrakine geç.
        
        Returns:
            bool: Fallback key varsa True, yoksa False
        """
        if self._current_key_index < len(self._api_keys):
            self._api_keys[self._current_key_index].status = APIKeyStatus.QUOTA_EXCEEDED
            self._current_key_index += 1
            
            if self._current_key_index < len(self._api_keys):
                print(f"🔄 API Key fallback: {self._api_keys[self._current_key_index].name}")
                return True
        
        return False
    
    def reset_api_keys(self) -> None:
        """Tüm key'leri aktif duruma sıfırla (günlük sıfırlama için)."""
        for key_info in self._api_keys:
            key_info.status = APIKeyStatus.ACTIVE
        self._current_key_index = 0
    
    def get_api_key_count(self) -> int:
        """Toplam API key sayısı."""
        return len(self._api_keys)
    
    def get_api_key_status(self) -> List[Dict[str, Any]]:
        """Tüm key'lerin durumunu döndür (UI için)."""
        return [
            {
                "name": key.name,
                "status": key.status.value,
                "masked": key.key[:8] + "..." + key.key[-4:] if len(key.key) > 12 else "***"
            }
            for key in self._api_keys
        ]
    
    # ─────────────────────────────────────────────────────────────────────────
    # MODEL YÖNETİMİ
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_model(self, model_type: str = "primary") -> str:
        """
        Model adını al.
        Öncelik: Secrets > App Config > Hardcoded Default
        
        Args:
            model_type: "primary", "fallback_1", "fallback_2", "tts", "audio_dialog"
        """
        # 1. Check Secrets (User Override)
        try:
            gemini_secrets = st.secrets.get("gemini", {})
            if model_type == "primary" and "default_model" in gemini_secrets:
                return gemini_secrets["default_model"]
            if model_type == "primary" and "pro_model" in gemini_secrets: # Legacy naming support
                 return gemini_secrets["pro_model"]
        except:
            pass

        # 2. Check App Config (YAML)
        models_config = self.get("ai.models", {})
        
        # Text modelleri
        if model_type in ["primary", "fallback_1", "fallback_2"]:
            text_models = models_config.get("text", {})
            return text_models.get(model_type, "gemini-3-flash-preview")
        
        # Özel modeller
        return models_config.get(model_type, "gemini-3-flash-preview")
    
    def get_model_cascade(self) -> List[str]:
        """
        Model fallback sıralamasını döndür.
        
        KULLANICI İSTEĞİ (2025-01): 
        Fallback modelleri iptal edildi. Sadece 'primary' model kullanılır.
        Kota dolarsa 'gemini_helper.py' içindeki döngü API Key'i değiştirir.
        Böylece: Key 1 (Model A) -> Error -> Key 2 (Model A) ... şeklinde çalışır.
        """
        return [
            self.get_model("primary")
        ]
    
    def get_generation_config(self) -> Dict[str, Any]:
        """AI generation parametreleri."""
        defaults = {
            "temperature": 0.4,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192
        }
        return self.get("ai.generation", defaults)
    
    # ─────────────────────────────────────────────────────────────────────────
    # GENEL CONFIG ERİŞİMİ
    # ─────────────────────────────────────────────────────────────────────────
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Dot notation ile config değeri al.
        Örnek: config.get("ai.models.text.primary")
        """
        keys = key_path.split(".")
        value = self._app_config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_lgs_constants(self) -> Dict[str, Any]:
        """LGS hesaplama sabitleri."""
        return self.get("lgs", {})
    
    def get_database_backend(self) -> str:
        """Aktif veritabanı backend'i."""
        return self.get("database.backend", "google_sheets")
    
    def is_supabase_enabled(self) -> bool:
        """Supabase aktif mi?"""
        return self.get("database.supabase.enabled", False)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SECRETS (Hassas veriler - secrets.toml'dan)
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_gcp_credentials(self) -> Optional[Dict]:
        """GCP service account credentials."""
        try:
            creds = st.secrets.get("gcp_service_account", {})
            return dict(creds) if creds else None
        except Exception:
            return None
    
    def get_sheets_key(self) -> Optional[str]:
        """Google Sheets spreadsheet key."""
        try:
            return st.secrets.get("google_sheets", {}).get("spreadsheet_key")
        except Exception:
            return None
    
    def get_supabase_config(self) -> Dict[str, str]:
        """Supabase config."""
        try:
            return {
                "url": st.secrets.get("supabase_url", ""),
                "key": st.secrets.get("supabase_key", "")
            }
        except Exception:
            return {"url": "", "key": ""}
    
    # ─────────────────────────────────────────────────────────────────────────
    # FEATURE FLAGS
    # ─────────────────────────────────────────────────────────────────────────
    
    def is_feature_enabled(self, feature_name: str, default: bool = False) -> bool:
        """Feature flag kontrolü."""
        features = self._feature_flags.get("features", {})
        return features.get(feature_name, default)
    
    def get_feature(self, feature_name: str, default: bool = False) -> bool:
        """Legacy alias for is_feature_enabled."""
        return self.is_feature_enabled(feature_name, default)
    
    def get_system_setting(self, key: str, default: Any = None) -> Any:
        """Sistem ayarı."""
        system = self._feature_flags.get("system", {})
        return system.get(key, default)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PEDAGOJİK AYARLAR
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_pedagogy_setting(self, key_path: str, default: Any = None) -> Any:
        """Pedagojik ayar al."""
        return self.get(f"pedagogy.{key_path}", default)
    
    def is_ambient_noise_enabled(self) -> bool:
        """Sınav simülasyonu ambient noise."""
        return self.get("pedagogy.exam_simulation.ambient_noise", False)
    
    def is_tts_enabled(self) -> bool:
        """TTS özelliği aktif mi?"""
        return self.get("pedagogy.audio.tts_enabled", False)
    
    # ─────────────────────────────────────────────────────────────────────────
    # EXTERNAL API KEYS (Beta Modu)
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_perplexity_api_key(self) -> Optional[str]:
        """Perplexity API key'i al (Beta Modu için)."""
        # 1. Environment variable
        import os
        env_key = os.environ.get("PERPLEXITY_API_KEY")
        if env_key:
            return env_key
        
        # 2. Streamlit secrets
        try:
            perplexity_secrets = st.secrets.get("perplexity", {})
            if perplexity_secrets:
                return perplexity_secrets.get("api_key")
        except Exception:
            pass
        
        return None


# ─────────────────────────────────────────────────────────────────────────────
# SINGLETON ERİŞİM
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_config() -> UnifiedConfigManager:
    """Global config instance."""
    return UnifiedConfigManager()


# Legacy uyumluluk için eski fonksiyon
def get_config_manager() -> UnifiedConfigManager:
    """Legacy uyumluluk için alias."""
    return get_config()
