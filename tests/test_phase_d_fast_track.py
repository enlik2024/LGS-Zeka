import pytest
from utils.content_ingest_engine import ContentIngestEngine
from utils.db_manager import DatabaseManager
from unittest.mock import MagicMock, patch
import pandas as pd

def test_parse_page_range():
    engine = ContentIngestEngine()
    assert engine.parse_page_range("1-3") == [1, 2, 3]
    assert engine.parse_page_range("5") == [5]
    assert engine.parse_page_range("10-10") == [10]
    assert engine.parse_page_range("invalid") == []

def test_build_fiche_rows():
    engine = ContentIngestEngine()
    mock_json = {
        "fiches": [
            {
                "content_type": "micro_lesson",
                "summary_bullets": ["Point 1"],
                "difficulty_band": 2
            }
        ]
    }
    meta = {"lesson": "Math", "topic": "Algebra", "subtopic": "Basics", "publisher": "Test"}
    
    rows = engine.build_fiche_rows_from_llm_output(mock_json, meta)
    assert len(rows) == 1
    assert rows[0]["lesson"] == "Math"
    assert rows[0]["status"] == "draft"
    assert "Point 1" in rows[0]["summary_bullets"]

def test_update_content_status(tmp_path):
    # Mock DB Manager with local file
    db = DatabaseManager()
    
    # Create dummy CSV
    csv_path = "content.csv" # DBManager uses hardcoded name in local mode
    # We need to mock os.path.exists and pandas read/write if we want to be safe, 
    # or use a temp dir but DBManager hardcodes filename.
    # Let's mock pandas read_csv and to_csv
    
    with patch("pandas.read_csv") as mock_read, \
         patch("pandas.DataFrame.to_csv") as mock_write, \
         patch("os.path.exists") as mock_exists:
        
        mock_exists.return_value = True
        
        df = pd.DataFrame([{
            "content_id": "CNT-0001",
            "status": "draft",
            "active": False
        }])
        mock_read.return_value = df
        
        success = db.update_content_status("CNT-0001", "approved", {"active": True})
        assert success
        
        # Verify write
        args, _ = mock_write.call_args
        # df is modified in place
        assert df.iloc[0]["status"] == "approved"
        assert df.iloc[0]["active"] == True
