"""
Content Ingest Engine
PDF'den içerik fişi üretimi için yardımcı modül.
"""

try:
    import fitz  # PyMuPDF
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False
    fitz = None

import streamlit as st
from typing import List, Dict, Any, Optional
import json
import re

class ContentIngestEngine:
    """
    PDF işleme ve içerik dönüştürme motoru.
    """
    
    @staticmethod
    def parse_page_range(page_range_str: str) -> List[int]:
        """
        "12-15" formatındaki stringi [12, 13, 14, 15] listesine çevirir.
        Tek sayfa "12" -> [12]
        """
        pages = []
        try:
            parts = page_range_str.split('-')
            if len(parts) == 1:
                pages.append(int(parts[0]))
            elif len(parts) == 2:
                start = int(parts[0])
                end = int(parts[1])
                pages.extend(range(start, end + 1))
        except ValueError:
            st.error(f"Geçersiz sayfa aralığı formatı: {page_range_str}")
            return []
        return pages

    @staticmethod
    def pdf_pages_to_images(pdf_bytes: bytes, page_numbers: List[int]) -> List[bytes]:
        """
        PDF bytes'tan belirtilen sayfaları resim (bytes) olarak döndürür.
        """
        if not FITZ_AVAILABLE:
            st.error("⚠️ PyMuPDF (fitz) kütüphanesi bulunamadı. PDF işleme devre dışı. `pip install PyMuPDF` komutunu çalıştırın.")
            return []
        
        images = []
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page_num in page_numbers:
                # PDF 0-indexed, kullanıcı 1-indexed girer genelde.
                # Ancak PyMuPDF 0-indexed. Kullanıcıdan "1. sayfa" diye 1 gelirse 0. indexi almalıyız.
                # Varsayım: Kullanıcı PDF viewer'da gördüğü numarayı (1-based) giriyor.
                idx = page_num - 1
                
                if 0 <= idx < len(doc):
                    page = doc.load_page(idx)
                    pix = page.get_pixmap(dpi=150) # 150 DPI yeterli
                    img_bytes = pix.tobytes("png")
                    images.append(img_bytes)
                else:
                    st.warning(f"Sayfa {page_num} PDF sınırları dışında.")
            doc.close()
        except Exception as e:
            st.error(f"PDF işleme hatası: {e}")
        return images

    @staticmethod
    def build_fiche_rows_from_llm_output(output_json: Dict[str, Any], meta: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        LLM JSON çıktısını DB satırlarına dönüştürür.
        """
        fiches = output_json.get("fiches", [])
        rows = []
        
        for i, fiche in enumerate(fiches):
            # JSON alanlarını string'e çevir (DB için)
            summary = json.dumps(fiche.get("summary_bullets", []), ensure_ascii=False)
            strategy = json.dumps(fiche.get("strategy_steps", []), ensure_ascii=False)
            mistakes = json.dumps(fiche.get("common_mistakes", []), ensure_ascii=False)
            options = json.dumps(fiche.get("mini_check_options_json", {}), ensure_ascii=False)
            
            row = {
                "content_id": f"CNT-{st.session_state.get('content_counter', 0) + i + 1:04d}", # Basit ID
                "lesson": meta.get("lesson", ""),
                "topic": meta.get("topic", ""),
                "subtopic": meta.get("subtopic", ""),
                "publisher": meta.get("publisher", ""),
                "source_type": meta.get("source_type", "ai_generated"),
                "content_type": fiche.get("content_type", "micro_lesson"),
                "difficulty_band": fiche.get("difficulty_band", 3),
                "estimated_time_min": fiche.get("estimated_time_min", 5),
                "summary_bullets": summary,
                "strategy_steps": strategy,
                "common_mistakes": mistakes,
                "mini_check_stem": fiche.get("mini_check_stem", ""),
                "mini_check_options_json": options,
                "mini_check_correct_option": fiche.get("mini_check_correct_option", ""),
                "page_ref": fiche.get("page_ref", ""),
                "status": "draft",
                "active": False,
                "derivation_ref": meta.get("derivation_ref", "")
            }
            rows.append(row)
            
        return rows

# Singleton
@st.cache_resource
def get_content_ingest_engine() -> ContentIngestEngine:
    return ContentIngestEngine()
