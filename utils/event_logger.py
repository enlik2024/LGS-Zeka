"""
Event Logger
Kullanıcı olaylarını ve sistem hareketlerini loglar.
"""

import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class EventLogger:
    """
    Olayları kaydeder (CSV/DB).
    """
    
    def __init__(self):
        self.log_file = Path(__file__).parent.parent / "events.csv"
        self._ensure_log_file()
        
    def _ensure_log_file(self):
        """Log dosyasının varlığını kontrol eder."""
        if not self.log_file.exists():
            df = pd.DataFrame(columns=[
                "event_id", "timestamp", "event_type", 
                "user_id", "details", "session_id"
            ])
            df.to_csv(self.log_file, index=False)
            
    def log_event(self, event_type: str, user_id: str = "anonymous", details: Dict[str, Any] = None):
        """
        Bir olay kaydeder.
        
        Args:
            event_type: Olay tipi (örn: 'exam_start', 'page_view')
            user_id: Kullanıcı ID
            details: Ek bilgiler (dict)
        """
        try:
            new_event = {
                "event_id": f"evt_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "user_id": user_id,
                "details": str(details) if details else "{}",
                "session_id": "current_session" # Streamlit session ID eklenebilir
            }
            
            # Append to CSV
            df = pd.DataFrame([new_event])
            df.to_csv(self.log_file, mode='a', header=False, index=False)
            
        except Exception as e:
            print(f"Logging Error: {e}")

# Singleton
@st.cache_resource
def get_event_logger() -> EventLogger:
    return EventLogger()
