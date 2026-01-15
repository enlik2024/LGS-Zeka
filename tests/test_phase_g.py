import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from utils.analysis_engine import AnalysisEngine

# Mock Data
MOCK_ANSWERS = pd.DataFrame([
    {"student_id": "student1", "question_id": "q1", "is_correct": True},
    {"student_id": "student1", "question_id": "q2", "is_correct": False}
])

MOCK_QUESTIONS = pd.DataFrame([
    {"question_id": "q1", "lesson": "Matematik", "topic": "Üslü İfadeler", "difficulty_label": 3},
    {"question_id": "q2", "lesson": "Matematik", "topic": "Üslü İfadeler", "difficulty_label": 5}
])

MOCK_EXAMS = pd.DataFrame([
    {"student_id": "student1", "created_at": "2024-01-01", "score": 50, "lesson": "Matematik"},
    {"student_id": "student1", "created_at": "2024-01-02", "score": 60, "lesson": "Matematik"}
])

@pytest.fixture
def analysis_engine():
    with patch('utils.db_manager.get_db_manager') as mock_db_get:
        mock_db = MagicMock()
        mock_db.fetch_data.side_effect = lambda x: {
            "answers": MOCK_ANSWERS,
            "questions": MOCK_QUESTIONS,
            "exams": MOCK_EXAMS
        }.get(x, pd.DataFrame())
        
        mock_db_get.return_value = mock_db
        engine = AnalysisEngine()
        engine.db = mock_db
        return engine

def test_get_mastery_heatmap_data(analysis_engine):
    df = analysis_engine.get_mastery_heatmap_data("student1")
    assert not df.empty
    assert "Konu" in df.columns
    assert "Skor" in df.columns
    # q1 correct (3 pts), q2 wrong (0 pts). Total 3/8 -> 37.5%
    # Wait, logic: total_points += is_correct * difficulty
    # q1: 1 * 3 = 3
    # q2: 0 * 5 = 0
    # Total = 3. Max = 8. Score = 37.5
    assert df.iloc[0]["Skor"] == 37.5

def test_get_net_trend_data(analysis_engine):
    df = analysis_engine.get_net_trend_data("student1")
    assert not df.empty
    assert len(df) == 2
    assert "score" in df.columns

def test_generate_weekly_report_html(analysis_engine):
    html = analysis_engine.generate_weekly_report_html("student1")
    assert "Haftalık Gelişim Raporu" in html
    assert "Üslü İfadeler" in html
