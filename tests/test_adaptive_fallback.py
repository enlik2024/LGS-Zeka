import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from utils.exam_engine import ExamEngine

# Mock Data
MOCK_QUESTIONS = pd.DataFrame([
    {
        "question_id": "q1", "lesson": "Matematik", "topic": "Üslü İfadeler", 
        "difficulty_label": 3, "text": "Q1", "option_a": "A", "option_b": "B", 
        "option_c": "C", "option_d": "D", "correct_answer": "A", "question_origin": "TEST"
    },
    {
        "question_id": "q2", "lesson": "Matematik", "topic": "Kareköklü İfadeler", 
        "difficulty_label": 2, "text": "Q2", "option_a": "A", "option_b": "B", 
        "option_c": "C", "option_d": "D", "correct_answer": "B", "question_origin": "TEST"
    }
])

@pytest.fixture
def exam_engine():
    with patch('utils.db_manager.get_db_manager') as mock_db_get:
        mock_db = MagicMock()
        mock_db.fetch_data.return_value = MOCK_QUESTIONS
        mock_db_get.return_value = mock_db
        
        with patch('utils.llm_adapter.get_llm_adapter') as mock_llm_get:
            mock_llm = MagicMock()
            mock_llm_get.return_value = mock_llm
            
            with patch('utils.analysis_engine.get_analysis_engine') as mock_analysis_get:
                mock_analysis = MagicMock()
                mock_analysis_get.return_value = mock_analysis
                
                engine = ExamEngine()
                engine.db = mock_db # Explicitly set mock
                engine.llm = mock_llm
                engine.analysis = mock_analysis
                return engine

def test_fallback_difficulty_relax(exam_engine):
    """Test 1: Zorluk seviyesi bulunamazsa esnetilmeli."""
    # Plan: Zorluk 5 istiyor (DB'de yok, sadece 2 ve 3 var)
    plan = [{"lesson": "Matematik", "topic": "Üslü İfadeler", "difficulty": 5}]
    
    exam = exam_engine.create_adaptive_exam("student_1", plan=plan)
    
    assert len(exam['questions']) == 1
    # Zorluk 5 yoktu ama 3 (q1) geldi çünkü konu tutuyor
    assert exam['questions'][0]['question_id'] == 'q1'

def test_fallback_topic_only(exam_engine):
    """Test 2: Konu varsa ama zorluk çok farklıysa konu bazlı gelmeli."""
    # Plan: Zorluk 1 istiyor (DB'de 3 var)
    plan = [{"lesson": "Matematik", "topic": "Üslü İfadeler", "difficulty": 1}]
    
    exam = exam_engine.create_adaptive_exam("student_1", plan=plan)
    
    assert len(exam['questions']) == 1
    assert exam['questions'][0]['topic'] == "Üslü İfadeler"

def test_fallback_insufficient_questions(exam_engine):
    """Test 3: Yetersiz soru durumunda sistem çökmemeli."""
    # Plan: 5 soru istiyor ama DB'de sadece 2 soru var
    plan = [
        {"lesson": "Matematik", "topic": "Üslü İfadeler", "difficulty": 3},
        {"lesson": "Matematik", "topic": "Kareköklü İfadeler", "difficulty": 2},
        {"lesson": "Matematik", "topic": "Yok", "difficulty": 1}, # Yok
        {"lesson": "Matematik", "topic": "Yok", "difficulty": 1}, # Yok
        {"lesson": "Matematik", "topic": "Yok", "difficulty": 1}  # Yok
    ]
    
    exam = exam_engine.create_adaptive_exam("student_1", plan=plan)
    
    # Sistem akıllıca davranıp eksikleri aynı dersten rastgele sorularla tamamlamalı
    # Bu yüzden 2 değil, planlanan sayı olan 5 dönmeli
    assert len(exam['questions']) == 5
    assert exam['type'] == 'adaptive'
    
    # İlk 2 soru hedeflenen sorular olmalı (veya en azından listede olmalı)
    ids = [q['question_id'] for q in exam['questions']]
    assert 'q1' in ids
    assert 'q2' in ids
