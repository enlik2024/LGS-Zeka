import sys
import os
sys.path.append(os.getcwd())

import logging
from utils.llm_adapter import get_llm_adapter
from components.socratic_chat import _get_inline_response

def test_graphviz():
    print("\n[TEST 1] Graphviz Generation")
    llm = get_llm_adapter()
    
    lesson = "Fen Bilimleri"
    topic = "Mevsimler ve İklim"
    subtopic = "Mevsimlerin Oluşumu"
    context = "Dünyanın eksen eğikliği (23 derece 27 dakika) mevsimlerin temel sebebidir."
    
    try:
        print("Waiting for LLM generation...")
        code = llm.generate_graphviz(lesson, topic, subtopic, context)
        print(f"Code Length: {len(code)}")
        print(f"Snippet: {code[:50]}...")
        
        if "digraph" in code:
            print("✅ PASS: Valid DOT format detected.")
        else:
            print("❌ FAIL: Code does not contain 'digraph'.")
            print(f"Full Output: {code}")
            
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")

def test_tutor_context():
    print("\n[TEST 2] Tutor Context Injection")
    
    user_input = "Mevsimler neden oluşur?"
    history = []
    current_context = {
        "lesson": "Fen Bilimleri",
        "topic": "Mevsimler",
        "subtopic": "Oluşum"
    }
    learning_context = "ÖZEL BİLGİ: Mevsimlerin oluşumunda 'Eksen Eğikliği' en kritik faktördür."
    
    try:
        response = _get_inline_response(user_input, history, current_context, learning_context)
        print(f"Tutor Response: {response}")
        
    except Exception as e:
        print(f"❌ FAIL: Exception: {e}")

if __name__ == "__main__":
    test_graphviz()
    test_tutor_context()
