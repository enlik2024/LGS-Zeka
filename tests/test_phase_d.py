import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from utils.curriculum_engine import CurriculumEngine
from utils.content_engine import ContentEngine

# Mock Data
MOCK_CURRICULUM = pd.DataFrame([
    {"lesson": "Matematik", "topic": "Üslü İfadeler", "subtopic": "Çözümleme", "active": True},
    {"lesson": "Matematik", "topic": "Üslü İfadeler", "subtopic": "Bilimsel Gösterim", "active": False}
])

MOCK_CONTENT = pd.DataFrame([
    {
        "lesson": "Matematik", "topic": "Üslü İfadeler", "subtopic": "Çözümleme", 
        "content_type": "fiche", "active": True, "summary_bullets": "Test Summary"
    }
])

MOCK_QUESTIONS = pd.DataFrame([
    {"question_id": "q1", "lesson": "Matematik", "topic": "Üslü İfadeler", "subtopic": "Çözümleme"}
])

@pytest.fixture
def engines():
    with patch('utils.db_manager.get_db_manager') as mock_db_get:
        mock_db = MagicMock()
        mock_db.fetch_data.side_effect = lambda x: {
            "curriculum_map": MOCK_CURRICULUM,
            "content": MOCK_CONTENT,
            "questions": MOCK_QUESTIONS
        }.get(x, pd.DataFrame())
        
        mock_db_get.return_value = mock_db
        
        curr_engine = CurriculumEngine()
        curr_engine.db = mock_db
        
        cont_engine = ContentEngine()
        cont_engine.db = mock_db
        cont_engine.curriculum = curr_engine
        
        return curr_engine, cont_engine

def test_validate_tags(engines):
    curr, _ = engines
    # Active tag
    assert curr.validate_tags("Matematik", "Üslü İfadeler", "Çözümleme") == True
    # Inactive tag
    assert curr.validate_tags("Matematik", "Üslü İfadeler", "Bilimsel Gösterim") == False
    # Non-existent tag
    assert curr.validate_tags("Matematik", "Yok", "Yok") == False

def test_build_learning_packet(engines):
    _, cont = engines
    packet = cont.build_learning_packet("student1", "Matematik", "Üslü İfadeler", "Çözümleme")
    
    assert packet is not None
    assert packet['topic'] == "Üslü İfadeler"
    assert packet['content']['summary_bullets'] == "Test Summary"

def test_wrong_to_learn_hook(engines):
    _, cont = engines
    suggestion = cont.suggest_content_for_wrong_question("q1")
    
    assert suggestion is not None
    assert suggestion['subtopic'] == "Çözümleme"
