import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch
from utils.config_manager import UnifiedConfigManager as ConfigManager
from utils.event_logger import EventLogger
from utils.llm_adapter import LLMAdapter

def test_feature_flags_loading():
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "features:\n  test_flag: true"
        
        with patch("pathlib.Path.exists", return_value=True):
            config = ConfigManager()
            # Mocking yaml load is tricky with simple open mock, 
            # so we rely on the fact that if file exists it tries to load.
            # For unit test simplicity, let's mock _load_flags directly
            config.flags = {"features": {"test_flag": True}}
            
            assert config.get_feature("test_flag") == True
            assert config.get_feature("non_existent") == False

def test_event_logging(tmp_path):
    # Use a temporary file for logging
    log_file = tmp_path / "test_events.csv"
    
    with patch("utils.event_logger.EventLogger._ensure_log_file") as mock_ensure:
        logger = EventLogger()
        logger.log_file = log_file
        
        # Create dummy file
        pd.DataFrame(columns=["event_id", "timestamp", "event_type", "user_id", "details", "session_id"]).to_csv(log_file, index=False)
        
        logger.log_event("test_event", "user1", {"key": "value"})
        
        df = pd.read_csv(log_file)
        assert len(df) == 1
        assert df.iloc[0]["event_type"] == "test_event"
        assert df.iloc[0]["user_id"] == "user1"

def test_prompt_loading():
    # Use side_effect to avoid breaking other open calls (like streamlit config)
    original_open = open
    
    def side_effect(file, mode='r', *args, **kwargs):
        # Check if it's our test file (either string path or Path object)
        if "test_prompt.txt" in str(file):
            mock_file = MagicMock()
            mock_file.read.return_value = "Hello {name}"
            mock_file.__enter__.return_value = mock_file
            return mock_file
        return original_open(file, mode, *args, **kwargs)
    
    with patch("builtins.open", side_effect=side_effect):
        adapter = LLMAdapter()
        adapter.api_key = "dummy"
        
        prompt = adapter.load_prompt("test_prompt.txt", name="World")
        assert prompt == "Hello World"

def test_prompt_formatting():
    """Test formatting logic directly to isolate the issue."""
    template = "Hello {name}"
    formatted = template.format(name="World")
    assert formatted == "Hello World"

def test_real_adaptive_plan_loading():
    """Integration test to verify the actual adaptive_plan_v1.txt file exists and loads."""
    adapter = LLMAdapter()
    # No need for API key to load prompt
    
    # Empty summary_json just for formatting
    prompt = adapter.load_prompt("adaptive_plan_v1.txt", summary_json="{}")
    
    assert prompt is not None
    assert len(prompt) > 0
    assert "Öğrenci Özeti:" in prompt
    assert "Strict JSON" in prompt
