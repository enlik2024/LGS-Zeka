import pytest
import pandas as pd
from utils.exam_engine import ExamEngine
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_db():
    db = MagicMock()
    # Mock questions data
    data = {
        "question_id": ["q1", "q2", "q3", "q4", "q5"],
        "lesson": ["Matematik"] * 5,
        "topic": ["Üslü İfadeler"] * 5,
        "difficulty_label": [3] * 5,
        "question_origin": ["publisher", "meb", "ai_variant_of_pool", "ai_original", "publisher"],
        "question_text": ["Soru 1", "Soru 2", "Soru 3", "Soru 4", "Soru 5"],
        "options_json": ["{}"] * 5,
        "correct_option": ["A"] * 5
    }
    df = pd.DataFrame(data)
    db.fetch_data.return_value = df
    return db

@patch('utils.exam_engine.get_db_manager')
def test_select_questions_by_mix_hint(mock_get_db, mock_db):
    mock_get_db.return_value = mock_db
    engine = ExamEngine()
    
    # Mock mix config to be neutral
    engine.mix_config = {
        "default_mix": {"publisher": 0.25, "meb": 0.25, "ai_variant_of_pool": 0.25, "ai_original": 0.25}
    }
    
    # Test with Hint
    plan_item = {
        "lesson": "Matematik",
        "topic": "Üslü İfadeler",
        "difficulty": 3,
        "count": 1,
        "origin_mix_hint": "meb"
    }
    
    questions_df = mock_db.fetch_data("questions")
    selected = engine.select_questions_by_mix(plan_item, questions_df)
    
    assert len(selected) == 1
    assert selected[0]["origin"] == "meb"
    assert selected[0]["question_id"] == "q2"

@patch('utils.exam_engine.get_db_manager')
def test_select_questions_by_mix_fallback(mock_get_db, mock_db):
    mock_get_db.return_value = mock_db
    engine = ExamEngine()
    
    # Test Fallback (Requested 'ai_original' but only 'publisher' available in filtered set if we filter strictly)
    # But our mock data has ai_original. Let's filter manually to simulate scarcity.
    
    plan_item = {
        "lesson": "Matematik",
        "topic": "Üslü İfadeler",
        "difficulty": 3,
        "count": 1,
        "origin_mix_hint": "ai_original"
    }
    
    questions_df = mock_db.fetch_data("questions")
    # Remove ai_original from df passed to method
    filtered_df = questions_df[questions_df['question_origin'] != 'ai_original']
    
    selected = engine.select_questions_by_mix(plan_item, filtered_df)
    
    assert len(selected) == 1
    # Should fallback to any available (publisher, meb, etc.)
    assert selected[0]["origin"] in ["publisher", "meb", "ai_variant_of_pool"]

if __name__ == "__main__":
    # Manual run setup
    pass
