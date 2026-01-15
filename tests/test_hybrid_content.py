import pytest
import pandas as pd
from utils.teaching_engine import TeachingEngine
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_db():
    db = MagicMock()
    # Mock questions
    q_data = {
        "question_id": ["q1"],
        "lesson": ["Matematik"],
        "topic": ["Üslü İfadeler"],
        "subtopic": ["Üslü Sayıların Özellikleri"]
    }
    db.fetch_data.return_value = pd.DataFrame(q_data)
    
    # Mock content
    # 1 Publisher, 1 Variant, 1 AI Generated
    c_data = {
        "content_id": ["c1", "c2", "c3"],
        "lesson": ["Matematik"] * 3,
        "topic": ["Üslü İfadeler"] * 3,
        "subtopic": ["Üslü Sayıların Özellikleri"] * 3,
        "status": ["approved"] * 3,
        "active": ["True"] * 3,
        "source_type": ["publisher", "ai_variant_of_publisher", "ai_generated"],
        "publisher": ["Hız", "Hız", "AI"]
    }
    db.load_content.return_value = pd.DataFrame(c_data)
    return db

@patch('utils.teaching_engine.get_db_manager')
def test_suggest_content_priority(mock_get_db, mock_db):
    mock_get_db.return_value = mock_db
    engine = TeachingEngine()
    
    suggestions = engine.suggest_content_for_wrong_question("q1", "student1")
    
    assert len(suggestions) == 2
    # First should be publisher
    assert suggestions[0]["source_type"] == "publisher"
    # Second should be variant
    assert suggestions[1]["source_type"] == "ai_variant_of_publisher"

@patch('utils.teaching_engine.get_db_manager')
def test_suggest_content_fallback(mock_get_db, mock_db):
    mock_get_db.return_value = mock_db
    engine = TeachingEngine()
    
    # Remove publisher and variant from mock
    c_data = {
        "content_id": ["c3", "c4"],
        "lesson": ["Matematik"] * 2,
        "topic": ["Üslü İfadeler"] * 2,
        "subtopic": ["Üslü Sayıların Özellikleri"] * 2,
        "status": ["approved"] * 2,
        "active": ["True"] * 2,
        "source_type": ["ai_generated", "ai_generated"],
        "publisher": ["AI", "AI"]
    }
    mock_db.load_content.return_value = pd.DataFrame(c_data)
    
    suggestions = engine.suggest_content_for_wrong_question("q1", "student1")
    
    assert len(suggestions) == 2
    assert suggestions[0]["source_type"] == "ai_generated"
    assert suggestions[1]["source_type"] == "ai_generated"

if __name__ == "__main__":
    pass
