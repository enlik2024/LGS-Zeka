"""
Prompts Modülü
AI için sistem promptları ve şablonları
"""

from .analysis_prompts import (
    QUICK_ANALYSIS_PROMPT,
    DETAILED_ANALYSIS_PROMPT,
    VISUAL_ANALYSIS_PROMPT
)

from .teaching_prompts import (
    SOCRATIC_TUTOR_PROMPT,
    HINT_GENERATOR_PROMPT,
    CONCEPT_EXPLAINER_PROMPT
)

__all__ = [
    'QUICK_ANALYSIS_PROMPT',
    'DETAILED_ANALYSIS_PROMPT',
    'VISUAL_ANALYSIS_PROMPT',
    'SOCRATIC_TUTOR_PROMPT',
    'HINT_GENERATOR_PROMPT',
    'CONCEPT_EXPLAINER_PROMPT'
]
