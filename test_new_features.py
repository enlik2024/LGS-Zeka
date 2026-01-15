"""
Test script for new features (Schedule & Exam Engines)
"""
import pytest
from datetime import datetime
from utils.schedule_engine import get_schedule_engine
from utils.exam_engine import get_exam_engine

def test_schedule_engine_initialization():
    engine = get_schedule_engine()
    assert engine is not None

def test_get_today_blocks():
    engine = get_schedule_engine()
    blocks = engine.get_today_blocks()
    assert isinstance(blocks, list)
    assert len(blocks) > 0
    assert "task" in blocks[0]

def test_exam_engine_initialization():
    engine = get_exam_engine()
    assert engine is not None

def test_create_fixed_exam():
    engine = get_exam_engine()
    exam = engine.create_fixed_exam("Matematik", 5)
    assert exam["type"] == "fixed"
    assert len(exam["questions"]) == 5
    assert exam["questions"][0]["lesson"] == "Matematik"

def test_create_adaptive_exam():
    engine = get_exam_engine()
    exam = engine.create_adaptive_exam("student_1")
    assert exam["type"] == "adaptive"
    assert len(exam["questions"]) > 0
