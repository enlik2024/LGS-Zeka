"""
Schedule Engine (DEPRECATED)
⚠️ BU DOSYA VE 'schedule' TABLOSU ARTIK KULLANILMAMAKTADIR.
Lütfen 'utils/scheduler_engine.py' ve 'schedules' tablosunu kullanın.

Günlük çalışma planı ve zaman yönetimi motoru.
"""

import pandas as pd
from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Any
import streamlit as st
from utils.db_manager import get_db_manager

class ScheduleEngine:
    """
    Günlük plan ve zaman yönetimi işlemlerini yürütür.
    """
    
    def __init__(self):
        self.db = get_db_manager()
        
    def _initialize_schedule(self):
        """
        Session state içinde schedule verisini başlatır.
        Önce DB'den okumayı dener.
        """
        if 'schedule_data' not in st.session_state:
            # DB'den oku
            df = self.db.fetch_data("schedule")
            
            if not df.empty:
                # DataFrame'i list of dicts'e çevir
                # CSV'den gelen veriyi UI formatına uyarla
                records = df.to_dict('records')
                formatted_schedule = []
                
                for row in records:
                    # CSV kolonlarını UI'ın beklediği formata map et
                    formatted_schedule.append({
                        "id": row.get("schedule_id", f"sch_{row.get('block_start')}"),
                        "start": row.get("block_start"),
                        "end": row.get("block_end"),
                        "type": row.get("block_type"),
                        "task": row.get("task_type"), # UI 'task' bekliyor, CSV 'task_type'
                        "desc": row.get("target_desc"),
                        "status": "completed" if str(row.get("is_completed")).lower() == 'true' else "pending",
                        "duration_min": 40 # Varsayılan veya hesaplanabilir
                    })
                
                st.session_state.schedule_data = formatted_schedule
            else:
                # DB boşsa boş liste
                st.session_state.schedule_data = []

    def save_schedule(self, schedule_list: List[Dict[str, Any]], day: str = None, overwrite_all: bool = False):
        """
        Programı kaydeder.
        day: "Monday", "Tuesday" vb.
        overwrite_all: True ise tüm günleri bu şablonla ezer (Eski davranış).
        """
        # Mevcut tüm veriyi çek
        all_data_df = self.db.fetch_data("schedule")
        
        # Yeni kayıtları hazırla
        new_rows = []
        target_days = [day] if day and not overwrite_all else ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for d in target_days:
            for item in schedule_list:
                new_rows.append({
                    "schedule_id": f"{d[:3]}_{item.get('id')}", # Unique ID: Mon_blk_1
                    "student_id": "pilot_ogrenci_01",
                    "day_of_week": d,
                    "block_start": item.get("start"),
                    "block_end": item.get("end"),
                    "block_type": item.get("type"),
                    "task_type": item.get("task"),
                    "target_desc": item.get("desc"),
                    "is_active": True,
                    "is_completed": True if item.get("status") == "completed" else False
                })
        
        new_df = pd.DataFrame(new_rows)
        
        if overwrite_all or all_data_df.empty:
            final_df = new_df
        else:
            # Sadece ilgili günleri silip yenisini ekle
            # Mevcut veriden target_days olmayanları tut
            remaining_df = all_data_df[~all_data_df['day_of_week'].isin(target_days)]
            final_df = pd.concat([remaining_df, new_df], ignore_index=True)
            
        try:
            # Supabase'e kaydet: Mevcut günleri sil, yenilerini ekle
            if self.db._client and self.db.db_type == "supabase":
                # Hedef günlerdeki eski kayıtları sil
                for d in target_days:
                    self.db._client.table("schedule").delete().eq("day_of_week", d).eq("student_id", "pilot_ogrenci_01").execute()
                
                # Yeni kayıtları ekle
                for row in new_rows:
                    self.db._client.table("schedule").insert(row).execute()
            else:
                # Fallback: CSV'ye yaz
                final_df.to_csv("schedule.csv", index=False)
            
            st.cache_data.clear()
            # Session state güncelle
            if 'schedule_data' in st.session_state:
                del st.session_state['schedule_data']
            
            # Debug: Kayıt başarılı bildirimi
            if self.db._client and self.db.db_type == "supabase":
                st.toast(f"✅ {len(new_rows)} blok Supabase'e kaydedildi!", icon="💾")
        except Exception as e:
            st.error(f"Kayıt hatası: {e}")
        
    def get_today_blocks(self, student_id: str = "pilot_ogrenci_01") -> List[Dict[str, Any]]:
        """
        Bugüne (gerçek gün ismine göre) ait çalışma bloklarını getirir.
        """
        today_name = datetime.now().strftime("%A")
        # Türkçe gün isimleri mapping (gerekirse)
        # Şimdilik İngilizce gün isimleri kullanıyoruz (Monday, Tuesday...)
        
        return self.get_schedule_for_day(today_name)

    def get_schedule_for_day(self, day: str) -> List[Dict[str, Any]]:
        """
        Belirli bir günün programını getirir.
        """
        df = self.db.fetch_data("schedule")
        if df.empty:
            return []
            
        day_df = df[df['day_of_week'] == day]
        if day_df.empty:
            return []
            
        formatted_schedule = []
        for row in day_df.to_dict('records'):
            formatted_schedule.append({
                "id": row.get("schedule_id", "").split("_")[-1] if "_" in str(row.get("schedule_id", "")) else row.get("schedule_id"), # ID temizle
                "start": row.get("block_start"),
                "end": row.get("block_end"),
                "type": row.get("block_type"),
                "task": row.get("task_type"),
                "desc": row.get("target_desc"),
                "status": "completed" if str(row.get("is_completed")).lower() == 'true' else "pending",
                "duration_min": 40 # Varsayılan
            })
            
        # Saate göre sırala
        formatted_schedule.sort(key=lambda x: x['start'])
        return formatted_schedule

    def mark_block_completed(self, block_id: str):
        """
        Bloğu tamamlandı olarak işaretler.
        Not: Bu sadece o günkü kaydı güncellemeli.
        """
        # Bu kısım biraz karmaşık çünkü ID'ler gün bazlı değişiyor.
        # Basitlik için: Bugünün programını çek, güncelle, kaydet.
        today_name = datetime.now().strftime("%A")
        blocks = self.get_schedule_for_day(today_name)
        
        updated = False
        for block in blocks:
            # ID eşleşmesi (prefixsiz ID ile kontrol edebiliriz veya tam ID)
            # block_id muhtemelen UI'dan geliyor.
            if block_id in block['id'] or block['id'] in block_id:
                block['status'] = 'completed'
                updated = True
                break
        
        if updated:
            self.save_schedule(blocks, day=today_name, overwrite_all=False)

    def compute_daily_summary(self) -> str:
        """
        Gün sonu veya anlık durum özeti üretir (LLM destekli).
        """
        blocks = self.get_today_blocks()
        if not blocks:
            return "Bugün için henüz bir plan oluşturulmamış."
            
        total = len(blocks)
        completed = sum(1 for b in blocks if b.get('status') == 'completed')
        progress = (completed / total) * 100 if total > 0 else 0
        
        # Basit kural tabanlı özet (LLM yedeği)
        if progress == 0:
            return "Henüz başlamadın. İlk bloğu tamamlamak en zorudur, hadi başlayalım! 🚀"
        elif progress == 100:
            return "Harika iş! Bugünün tüm hedeflerini tamamladın. Kendinle gurur duyabilirsin! 🎉"
        elif progress >= 50:
            return f"Yarıyı geçtin! ({completed}/{total}) blok bitti. Ritmini koru. 💪"
        else:
            return f"İyi gidiyorsun, {completed} blok tamamlandı. Sırada {total - completed} blok var. ⏳"

    def find_active_block(self, blocks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Şu anki saate göre aktif bloğu bulur.
        """
        now = datetime.now().time()
        
        for block in blocks:
            start_time = datetime.strptime(block['start'], "%H:%M").time()
            end_time = datetime.strptime(block['end'], "%H:%M").time()
            
            if start_time <= now <= end_time:
                return block
                
        return None

    def find_next_block(self, blocks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Sıradaki ilk bloğu bulur.
        """
        now = datetime.now().time()
        
        for block in blocks:
            start_time = datetime.strptime(block['start'], "%H:%M").time()
            if start_time > now:
                return block
                
        return None

    def calculate_progress(self, blocks: List[Dict[str, Any]]) -> float:
        """
        Günlük tamamlanma yüzdesini hesaplar.
        """
        if not blocks:
            return 0.0
            
        total = len(blocks)
        completed = sum(1 for b in blocks if b.get('status') == 'completed')
        
        return (completed / total) * 100

# Singleton
@st.cache_resource
def get_schedule_engine() -> ScheduleEngine:
    return ScheduleEngine()
