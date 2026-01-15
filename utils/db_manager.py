"""
Veritabanı Yönetim Modülü
LGS-Zeka platformu için Google Sheets ve Supabase bağlantılarını yöneten modül.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

class DatabaseManager:
    """
    Veritabanı işlemlerini yöneten sınıf.
    Google Sheets (prototip) ve Supabase (production) desteği.
    """
    
    def __init__(self, db_type: str = "google_sheets"):
        self.db_type = db_type
        self._client = None
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Veritabanı bağlantısını başlatır."""
        try:
            if self.db_type == "google_sheets":
                self._initialize_google_sheets()
            elif self.db_type == "supabase":
                self._initialize_supabase()
        except Exception as e:
            # st.error(f"Veritabanı bağlantısı başlatılamadı: {str(e)}")
            # Bağlantı hatası olsa bile local fallback çalışmalı, o yüzden raise etmiyoruz.
            print(f"DB Connection Error: {e}")

        # Schema Migration (Local CSV only for now)
        self._migrate_questions_schema()

    def _migrate_questions_schema(self) -> None:
        """Questions tablosuna yeni kolonları ekler (Migration)."""
        filename = "questions.csv"
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                changed = False
                
                new_columns = {
                    "has_figure": False,
                    "figure_type": "none",
                    "figure_policy": "no_variant",
                    "figure_path": "",
                    # Phase I: AI Automation Fields
                    "has_figure_ai": False,
                    "figure_type_ai": "none",
                    "figure_confidence": 0.0,
                    "has_figure_final": False
                }
                
                for col, default_val in new_columns.items():
                    if col not in df.columns:
                        df[col] = default_val
                        changed = True
                
                if changed:
                    df.to_csv(filename, index=False)
                    print("Schema migration applied: questions.csv updated.")
            except Exception as e:
                print(f"Schema migration failed: {e}")
    
    def _initialize_google_sheets(self) -> None:
        """Google Sheets API bağlantısını başlatır."""
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials_dict = st.secrets.get("gcp_service_account", None)
            
            if credentials_dict:
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
                self._client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Google Sheets Init Error: {e}")
            # st.error(f"Google Sheets bağlantısı kurulamadı: {str(e)}")

    def _initialize_supabase(self) -> None:
        """Supabase bağlantısını başlatır."""
        try:
            from utils.supabase_client import get_supabase
            self._client = get_supabase()
            if self._client:
                print("Supabase bağlantısı başarılı!")
        except Exception as e:
            print(f"Supabase Init Error: {e}")
            self._client = None
    
    @st.cache_data(ttl=60, show_spinner=False)
    def fetch_data(_self, sheet_name: str) -> pd.DataFrame:
        """Belirtilen sheet'ten veri çeker."""
        # 1. Try Supabase (if db_type is supabase)
        if _self.db_type == "supabase" and _self._client:
            try:
                result = _self._client.table(sheet_name).select("*").execute()
                if result.data:
                    df = pd.DataFrame(result.data)
                    return _self._convert_types(df, sheet_name)
            except Exception as e:
                print(f"Supabase fetch failed for {sheet_name}: {e}")
                # Fallback to local
        
        # 2. Try Google Sheets (if client exists and db_type is google_sheets)
        if _self.db_type == "google_sheets" and _self._client:
            try:
                spreadsheet_key = st.secrets.get("google_sheets", {}).get("spreadsheet_key", None)
                if spreadsheet_key:
                    spreadsheet = _self._client.open_by_key(spreadsheet_key)
                    worksheet = spreadsheet.worksheet(sheet_name)
                    data = worksheet.get_all_records()
                    df = pd.DataFrame(data)
                    if 'Tarih' in df.columns:
                        df['Tarih'] = pd.to_datetime(df['Tarih'], errors='coerce')
                    return df
            except Exception as e:
                print(f"Cloud fetch failed for {sheet_name}: {e}")
                # Fallback to local
        
        # 3. Try Local Fallback (Case Insensitive)
        return _self._fetch_local_fallback(sheet_name)
    
    def _convert_types(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Supabase TEXT sütunlarını uygun tiplere dönüştürür."""
        if df.empty:
            return df
        
        try:
            # Boolean dönüşümü
            bool_columns = ['active', 'is_correct', 'is_active', 'is_completed', 'has_figure', 'has_figure_ai', 'has_figure_final']
            for col in bool_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.lower().isin(['true', '1', 'yes'])
            
            # Integer dönüşümü
            int_columns = ['difficulty_label', 'difficulty_band', 'estimated_time_min', 'xp', 'level']
            for col in int_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            # JSON dönüşümü
            json_columns = ['options_json', 'mini_check_options_json', 'details']
            for col in json_columns:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: json.loads(x) if x and str(x).strip() not in ['', 'nan', 'None', '{}'] else {})
        except Exception as e:
            print(f"Type conversion warning for {table_name}: {e}")
        
        return df
    
    def get_current_user(self) -> dict:
        """Oturum açmış kullanıcıyı döndürür (MVP: otomatik login)."""
        if "current_user" not in st.session_state:
            if self.db_type == "supabase" and self._client:
                try:
                    result = self._client.table("users").select("*").eq("student_id", "pilot_ogrenci_01").execute()
                    if result.data:
                        st.session_state.current_user = result.data[0]
                    else:
                        st.session_state.current_user = {"student_id": "pilot_ogrenci_01", "name": "Pilot Öğrenci"}
                except Exception as e:
                    print(f"User fetch error: {e}")
                    st.session_state.current_user = {"student_id": "pilot_ogrenci_01", "name": "Pilot Öğrenci"}
            else:
                st.session_state.current_user = {"student_id": "pilot_ogrenci_01", "name": "Pilot Öğrenci"}
        return st.session_state.current_user

    def _fetch_local_fallback(self, sheet_name: str) -> pd.DataFrame:
        """Yerel dosyalardan okumayı dener (CSV/Excel)."""
        # Dosya isimlerini küçük harfe çevirip dene
        base_name = sheet_name
        candidates = [
            f"{base_name}.csv",
            f"{base_name}.xlsx",
            f"{base_name.lower()}.csv",
            f"{base_name.lower()}.xlsx",
            f"{base_name.capitalize()}.csv",
            f"{base_name.capitalize()}.xlsx"
        ]
        
        for candidate in candidates:
            if os.path.exists(candidate):
                try:
                    if candidate.endswith(".csv"):
                        return pd.read_csv(candidate)
                    else:
                        return pd.read_excel(candidate)
                except Exception as e:
                    st.error(f"Yerel dosya okuma hatası ({candidate}): {e}")
        
        # Dosya bulunamadıysa sessizce boş DF dön (UI tarafı halletsin)
        # st.warning(f"'{sheet_name}' verisi bulunamadı (Cloud ve Local).")
        return pd.DataFrame()

    def add_data(self, sheet_name: str, data_dict: Dict[str, Any]) -> bool:
        """Veri ekler (Supabase -> GSheets -> Local Fallback)."""
        # 1. Try Supabase
        if self.db_type == "supabase" and self._client:
            try:
                result = self._client.table(sheet_name).insert(data_dict).execute()
                if result.data:
                    st.cache_data.clear()
                    return True
            except Exception as e:
                print(f"Supabase add failed: {e}")
        
        # 2. Try Google Sheets
        if self.db_type == "google_sheets" and self._client:
            try:
                success = self._add_to_google_sheets(sheet_name, data_dict)
                if success:
                    return True
            except Exception as e:
                print(f"GSheets add failed: {e}")
            
        # 3. Local Fallback (Append to CSV)
        return self._add_to_local_csv(sheet_name, data_dict)

    def _add_to_google_sheets(self, sheet_name: str, data_dict: Dict[str, Any]) -> bool:
        spreadsheet_key = st.secrets.get("google_sheets", {}).get("spreadsheet_key", None)
        spreadsheet = self._client.open_by_key(spreadsheet_key)
        worksheet = spreadsheet.worksheet(sheet_name)
        headers = worksheet.row_values(1)
        row_data = []
        for header in headers:
            value = data_dict.get(header, "")
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d")
            row_data.append(value)
        worksheet.append_row(row_data)
        st.cache_data.clear()
        return True

    def _add_to_local_csv(self, sheet_name: str, data_dict: Dict[str, Any]) -> bool:
        """Yerel CSV'ye ekler."""
        filename = f"{sheet_name.lower()}.csv"
        
        try:
            df_new = pd.DataFrame([data_dict])
            
            if os.path.exists(filename):
                # Mevcut dosyanın kolon sırasını al
                df_existing = pd.read_csv(filename, nrows=0)
                existing_columns = df_existing.columns.tolist()
                
                # Yeni veriyi bu sıraya göre düzenle (Eksik kolon varsa NaN, fazla varsa sona ekle veya yoksay)
                # Fazla kolonları şimdilik yoksayalım ki yapı bozulmasın, 
                # veya migration ile eklenmesi gerekir.
                
                # Sadece mevcut kolonları al
                df_new = df_new.reindex(columns=existing_columns)
                
                df_new.to_csv(filename, mode='a', header=False, index=False, quoting=1)
            else:
                df_new.to_csv(filename, index=False, quoting=1)
                
            st.cache_data.clear()
            return True
        except Exception as e:
            st.error(f"Yerel kayıt hatası: {e}")
            return False

    def load_curriculum_map(self) -> pd.DataFrame:
        """Müfredat haritasını yükler."""
        return self.fetch_data("curriculum_map")

    def load_content(self) -> pd.DataFrame:
        """İçerik tablosunu yükler."""
        return self.fetch_data("content")

    def append_content_rows(self, rows: List[Dict[str, Any]]) -> bool:
        """Birden fazla içerik satırını ekler."""
        # Şimdilik döngü ile tek tek ekleyelim (Cloud API kotası için batch yapmak daha iyi olurdu ama MVP)
        all_success = True
        for row in rows:
            # Otomatik alanlar
            if "created_at" not in row:
                row["created_at"] = datetime.now().isoformat()
            if "active" not in row:
                row["active"] = False # Default pasif
            if "status" not in row:
                row["status"] = "draft"
                
            if not self.add_data("content", row):
                all_success = False
        return all_success

    def update_content_status(self, content_id: str, status: str, extra_fields: Optional[Dict[str, Any]] = None) -> bool:
        """
        İçerik durumunu günceller (Draft -> Approved).
        Not: Google Sheets update işlemi biraz maliyetli, yerel CSV için kolay.
        """
        # 1. Local Update (Öncelikli MVP)
        filename = "content.csv"
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                if 'content_id' in df.columns:
                    mask = df['content_id'] == content_id
                    if mask.any():
                        df.loc[mask, 'status'] = status
                        if extra_fields:
                            for k, v in extra_fields.items():
                                if k in df.columns:
                                    df.loc[mask, k] = v
                        df.to_csv(filename, index=False)
                        st.cache_data.clear()
                        return True
            except Exception as e:
                st.error(f"Local update hatası: {e}")
                return False
        
        # Cloud update henüz implemente edilmedi (row index bulmak lazım)
        return False

    def add_curriculum_item(self, lesson: str, topic: str, subtopic: str, importance: int = 3) -> bool:
        """Yeni bir müfredat maddesi ekler."""
        try:
            df = self.load_curriculum_map()
            
            # Tekrarlı kayıt kontrolü
            if not df.empty:
                exists = df[
                    (df['lesson'] == lesson) & 
                    (df['topic'] == topic) & 
                    (df['subtopic'] == subtopic)
                ]
                if not exists.empty:
                    return False # Zaten var
                
            new_row = {
                "lesson": lesson,
                "topic": topic,
                "subtopic": subtopic,
                "importance_weight": importance,
                "active": True
            }
            
            return self.add_data("curriculum_map", new_row)
            
        except Exception as e:
            st.error(f"Müfredat ekleme hatası: {e}")
            return False

    def get_approved_content(self, lesson: str, topic: str, subtopic: str, limit: int = 2) -> pd.DataFrame:
        """Onaylı içerikleri getirir."""
        df = self.load_content()
        if df.empty:
            return pd.DataFrame()
            
        # Filtreleme
        mask = (
            (df['lesson'] == lesson) &
            (df['topic'] == topic) &
            (df['subtopic'] == subtopic) &
            (df['status'] == 'approved') &
            (df['active'].astype(str).str.lower() == 'true')
        )
        
        filtered = df[mask]
        return filtered.head(limit)

    def validate_question_pool(self) -> Dict[str, Any]:
        """
        Soru havuzundaki verileri doğrular (Phase K2).
        
        Returns:
            Dict: Doğrulama raporu { "total": int, "invalid_count": int, "issues": List[Dict] }
        """
        df = self.fetch_data("questions")
        report = {
            "total": 0,
            "invalid_count": 0,
            "issues": []
        }
        
        if df.empty:
            return report
            
        report["total"] = len(df)
        
        for idx, row in df.iterrows():
            issues = []
            
            # 1. ID Kontrolü
            q_id = str(row.get('question_id', '')).strip()
            if not q_id or q_id.lower() == 'nan':
                issues.append("Question ID eksik")
            
            # 2. Metin veya Görsel Kontrolü
            text = str(row.get('question_text', '')).strip()
            fig_path = str(row.get('figure_path', '')).strip()
            if (not text or text.lower() == 'nan') and (not fig_path or fig_path.lower() == 'nan'):
                issues.append("Soru metni veya görseli yok")
                
            # 3. Doğru Cevap Kontrolü
            correct = str(row.get('correct_option', '')).strip().upper()
            if correct not in ['A', 'B', 'C', 'D']:
                issues.append(f"Geçersiz doğru cevap: {correct}")
                
            # 4. JSON Options Kontrolü
            options_json = str(row.get('options_json', ''))
            try:
                import json
                if options_json and options_json.lower() != 'nan':
                    # CSV'den okunan escaped quotes'u düzelt: "" -> "
                    clean_json = options_json.replace('""', '"')
                    # Baş ve sondaki tırnak varsa kaldır
                    if clean_json.startswith('"') and clean_json.endswith('"'):
                        clean_json = clean_json[1:-1]
                    json.loads(clean_json)
            except:
                issues.append("Seçenekler JSON formatı bozuk")

            if issues:
                report["invalid_count"] += 1
                report["issues"].append({
                    "row_index": idx + 2, # CSV header + 1-based index
                    "question_id": q_id,
                    "reasons": issues
                })
                
        return report

    # ============ ANALYSIS HISTORY ============
    
    def save_analysis_session(self, session_data: Dict[str, Any]) -> bool:
        """
        Analiz oturumunu veritabanına kaydeder.
        
        Args:
            session_data: {
                'student_id': str,
                'image_hash': str (optional),
                'question_text': str,
                'solution_steps': str,
                'final_answer': str,
                'difficulty_level': int,
                'topic': str,
                'subtopic': str
            }
        """
        if self.db_type == "supabase" and self._client:
            try:
                from datetime import datetime
                session_data['created_at'] = datetime.now().isoformat()
                result = self._client.table("analysis_sessions").insert(session_data).execute()
                if result.data:
                    print(f"Analysis session saved: {result.data[0].get('id')}")
                    return True
            except Exception as e:
                print(f"Analysis save error: {e}")
        return False
    
    def load_analysis_history(self, student_id: str = "pilot_ogrenci_01", limit: int = 20) -> pd.DataFrame:
        """
        Öğrencinin analiz geçmişini yükler.
        
        Returns:
            DataFrame: Analiz geçmişi
        """
        if self.db_type == "supabase" and self._client:
            try:
                result = self._client.table("analysis_sessions").select("*").eq("student_id", student_id).order("created_at", desc=True).limit(limit).execute()
                if result.data:
                    return pd.DataFrame(result.data)
            except Exception as e:
                print(f"Analysis history load error: {e}")
        return pd.DataFrame()

    # ============ FLASHCARDS (SUPABASE) ============

    def save_flashcards_db(self, lesson: str, topic: str, subtopic: str, cards: List[Dict]) -> bool:
        """Flashcartları Supabase'e kaydeder."""
        if self.db_type == "supabase" and self._client:
            try:
                data = {
                    "lesson": lesson,
                    "topic": topic,
                    "subtopic": subtopic,
                    "cards_json": cards,
                    "user_id": "anon"
                }
                # insert
                self._client.table("flashcards").insert(data).execute()
                print("Flashcards saved to Supabase.")
                return True
            except Exception as e:
                print(f"Supabase Flashcard Save Error: {e}")
        return False

    def load_flashcards_db(self, lesson: str, topic: str, subtopic: str) -> Optional[List[Dict]]:
        """Flashcartları Supabase'den yükler."""
        if self.db_type == "supabase" and self._client:
            try:
                res = self._client.table("flashcards").select("cards_json").eq("lesson", lesson).eq("topic", topic).eq("subtopic", subtopic).order("created_at", desc=True).limit(1).execute()
                if res.data:
                    return res.data[0]['cards_json']
            except Exception as e:
                print(f"Supabase Flashcard Load Error: {e}")
        return None


# Singleton instance
@st.cache_resource
def get_db_manager(db_type: str = None) -> DatabaseManager:
    """
    Veritabanı yöneticisini döndürür.
    db_type: None ise session_state'ten okur, yoksa 'google_sheets' kullanır.
    """
    if db_type is None:
        db_type = st.session_state.get("db_type", "supabase")  # Varsayılan: Supabase
    return DatabaseManager(db_type=db_type)

