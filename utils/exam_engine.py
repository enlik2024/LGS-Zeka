"""
Exam Engine
Deneme sınavı oluşturma ve yönetme motoru.
"""

import pandas as pd
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st
from utils.db_manager import get_db_manager
from utils.db_manager import get_db_manager
from utils.llm_adapter import get_llm_adapter
from utils.analysis_engine import get_analysis_engine
import json
import yaml
import os

class ExamEngine:
    """
    Sınav oluşturma, soru seçme ve sonuç kaydetme işlemlerini yürütür.
    """
    
    def __init__(self):
        self.db = get_db_manager()
        self.llm = get_llm_adapter()
        self.analysis = get_analysis_engine()
        self.mix_config = self._load_mix_config()

    def _load_mix_config(self) -> Dict[str, Any]:
        """Soru karışım konfigürasyonunu yükler."""
        config_path = "config/question_mix.yaml"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
        
    def create_fixed_exam(self, lesson: str, topic: Optional[str] = None, num_questions: int = 10) -> Dict[str, Any]:
        """
        Sabit bir mini deneme oluşturur (Gerçek Veri).
        """
        # DB'den soruları çek
        df = self.db.fetch_data("questions") # Sheet adı: questions (küçük harf duyarlı olabilir)
        
        if df.empty:
            st.error("Soru bankası boş veya okunamadı! (questions.xlsx)")
            return {}

        # Derse göre filtrele
        lesson_questions = df[df['lesson'] == lesson]
        
        # Konuya göre filtrele (Varsa)
        if topic and topic != "Tümü":
            lesson_questions = lesson_questions[lesson_questions['topic'] == topic]
        
        if lesson_questions.empty:
            # --- FALLBACK: JIT Question Generation ---
            st.info(f"⚠️ {lesson} - {topic if topic else 'Genel'} için soru bulunamadı. Konu fişlerinden üretiliyor...")
            
            generated_questions = self._generate_fallback_questions_from_content(lesson, topic)
            if not generated_questions:
                st.warning("Konu fişi de bulunamadı veya soru üretilemedi.")
                return {}
            
            # Üretilenleri DataFrame'e çevirip devam et
            lesson_questions = pd.DataFrame(generated_questions)
            
        # Rastgele seçim yap
        # Önce geçerli soruları filtrele (Metni olanlar)
        lesson_questions = lesson_questions[
            lesson_questions['question_text'].notna() & 
            (lesson_questions['question_text'].astype(str).str.strip() != '')
        ]
        
        # Eğer istenen sayıdan az soru varsa hepsini al
        sample_size = min(len(lesson_questions), num_questions)
        selected_df = lesson_questions.sample(n=sample_size)
        
        questions = []
        for _, row in selected_df.iterrows():
            questions.append({
                "question_id": row['question_id'],
                "lesson": row['lesson'],
                "topic": row['topic'],
                "difficulty": row.get('difficulty_label', 3),
                "text": row.get('question_text', row.get('text', '')),
                "options": json.loads(row['options_json']) if isinstance(row.get('options_json'), str) else row.get('options', {}),
                "correct": row['correct_option'] if 'correct_option' in row else row.get('correct_answer', ''),
                "figure_path": row.get('figure_path', '') if not pd.isna(row.get('figure_path', '')) else ''
            })
            
        exam_id = f"exam_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "exam_id": exam_id,
            "title": f"{lesson} Mini Deneme",
            "type": "fixed",
            "lesson": lesson,
            "created_at": datetime.now().isoformat(),
            "questions": questions
        }

    def request_adaptive_plan_from_llm(self, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        LLM'den adaptif deneme planı ister.
        """
        # Prompt'u dosyadan yükle (Versiyonlama)
        prompt = self.llm.load_prompt(
            "adaptive_plan_v1.txt", 
            summary_json=json.dumps(summary, ensure_ascii=False, indent=2)
        )
        
        if not prompt:
            return []
        
        try:
            response = self.llm.generate_json(prompt)
            plan = response.get("plan", [])
            
            # Basit doğrulama
            if not isinstance(plan, list):
                return []
            return plan
            
        except Exception as e:
            st.error(f"Plan oluşturma hatası: {e}")
            return []

    def create_adaptive_exam(self, student_id: str, num_questions: int = 10, plan: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Öğrencinin seviyesine göre adaptif deneme oluşturur.
        """
        # 1. Plan yoksa oluştur
        if not plan:
            summary = self.analysis.build_student_skill_summary(student_id)
            # LLM'e soru sayısını da söyleyebiliriz ama şimdilik planı alıp keselim/genişletelim
            plan = self.request_adaptive_plan_from_llm(summary)
            
        # Plan hala boşsa (LLM hatası veya veri yoksa) fallback
        if not plan:
            return self.create_fixed_exam("Matematik", num_questions=num_questions)
            
        # 2. Plandaki soruları DB'den çek
        questions_df = self.db.fetch_data("questions")
        selected_questions = []
        
        for item in plan:
            # Hybrid Selection Logic
            selected_for_item = self.select_questions_by_mix(item, questions_df)
            selected_questions.extend(selected_for_item)
            
        # 3. Yetersiz soru kontrolü (Graceful Fallback)
        if len(selected_questions) < num_questions:
             # TODO: Rastgele soru ile tamamla
             pass
                
        return {
            "exam_id": f"adapt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": "Kişiye Özel Adaptif Deneme",
            "type": "adaptive",
            "lesson": "Karma",
            "created_at": datetime.now().isoformat(),
            "questions": selected_questions
        }

    def select_questions_by_mix(self, plan_item: Dict[str, Any], all_questions_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Plan maddesine ve mix oranlarına göre soru seçer.
        """
        # 1. Temel Filtreleme (Ders, Konu, Zorluk)
        candidates = all_questions_df[
            (all_questions_df['lesson'] == plan_item['lesson']) & 
            (all_questions_df['topic'] == plan_item['topic'])
        ]
        
        # Zorluk filtresi (Esnek)
        diff_candidates = candidates[candidates['difficulty_label'] == plan_item['difficulty']]
        if diff_candidates.empty:
            # +/- 1 esneklik
            diff_candidates = candidates[candidates['difficulty_label'].between(plan_item['difficulty']-1, plan_item['difficulty']+1)]
        
        if not diff_candidates.empty:
            candidates = diff_candidates
            
        if candidates.empty:
            return []

        # 2. Seçim Döngüsü
        target_count = plan_item.get("count", 1)
        selected = []
        hint = plan_item.get("origin_mix_hint")
        
        for _ in range(target_count):
            if candidates.empty:
                break
                
            chosen_origin = None
            
            # A) Hint varsa onu kullan
            if hint and hint in ["publisher", "meb", "ai_variant_of_pool", "ai_original"]:
                chosen_origin = hint
            else:
                # B) Yoksa Config'den Olasılıksal Seç
                mix_ratios = self.mix_config.get("by_mode", {}).get("adaptive", self.mix_config.get("default_mix", {}))
                total = sum(mix_ratios.values())
                if total > 0:
                    r = random.random() * total
                    current = 0
                    for origin, weight in mix_ratios.items():
                        current += weight
                        if r <= current:
                            chosen_origin = origin
                            break
            
            # C) Adayları Filtrele
            origin_candidates = pd.DataFrame()
            if chosen_origin:
                origin_candidates = candidates[candidates['question_origin'] == chosen_origin]
            
            # D) Fallback: Seçilen kaynakta soru yoksa havuzdan rastgele al
            if origin_candidates.empty:
                origin_candidates = candidates
                
            # E) Seçim Yap
            if not origin_candidates.empty:
                row = origin_candidates.sample(1).iloc[0]
                
                # Seçenekleri parse et
                options = {}
                if isinstance(row['options_json'], str):
                    try:
                        options = json.loads(row['options_json'])
                    except:
                        pass
                else:
                     options = {
                        "A": row.get('option_a', ''),
                        "B": row.get('option_b', ''),
                        "C": row.get('option_c', ''),
                        "D": row.get('option_d', '')
                     }

                selected.append({
                    "question_id": row['question_id'],
                    "lesson": row['lesson'],
                    "topic": row['topic'],
                    "difficulty": row['difficulty_label'],
                    "text": row['question_text'] if 'question_text' in row else row.get('text', ''),
                    "options": options,
                    "correct": row['correct_option'] if 'correct_option' in row else row.get('correct_answer', ''),
                    "origin": row.get('question_origin', 'UNKNOWN'),
                    "figure_path": row.get('figure_path', '') if not pd.isna(row.get('figure_path', '')) else ''
                })
                
                # Seçileni adaylardan çıkar (Tekrar seçilmesin)
                candidates = candidates.drop(row.name)
                
        return selected

    def validate_ai_question_quality(self, question_row: Dict[str, Any]) -> bool:
        """AI soruları için kalite kontrolü."""
        if question_row.get('question_origin', '').startswith('ai_'):
            if question_row.get('quality_state') != 'active':
                return False
            # Ekstra kontroller (seçenek sayısı vb.) buraya
        return True

    def save_exam_result(self, exam_data: Dict[str, Any], answers: Dict[str, str], student_id: str = "pilot_ogrenci_01"):
        """
        Sınav sonucunu 'answers' ve 'exams' tablolarına kaydeder.
        """
        correct_count = 0
        total_questions = len(exam_data['questions'])
        
        # 1. Answers Tablosuna Kayıt
        for q in exam_data['questions']:
            given = answers.get(q['question_id'])
            is_correct = (given == q['correct'])
            if is_correct:
                correct_count += 1
                
            answer_record = {
                "answer_id": f"ans_{datetime.now().strftime('%Y%m%d%H%M%S')}_{q['question_id']}",
                "exam_id": exam_data['exam_id'],
                "student_id": student_id,
                "question_id": q['question_id'],
                "given_option": given if given else "BOS",
                "is_correct": is_correct,
                "created_at": datetime.now().isoformat()
            }
            self.db.add_data("answers", answer_record)
            
        # 2. Exams Tablosuna Kayıt (Özet)
        exam_record = {
            "exam_id": exam_data['exam_id'],
            "student_id": student_id,
            "title": exam_data['title'],
            "mode": exam_data['type'],
            "lesson": exam_data.get('lesson', 'Genel'),
            "created_at": exam_data['created_at'],
            "status": "tamamlandi",
            "score": (correct_count / total_questions) * 100 if total_questions > 0 else 0
        }
        self.db.add_data("exams", exam_record)
            
        return {
            "total": total_questions,
            "correct": correct_count,
            "wrong": total_questions - correct_count,
            "score": exam_record["score"]
        }

    def _generate_fallback_questions_from_content(self, lesson: str, topic: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Soru yoksa, konu fişlerinden JIT soru üretir.
        """
        # 1. İlgili Konu Fişlerini Bul
        content_df = self.db.load_content()
        if content_df.empty:
            return []
            
        mask = (content_df['lesson'] == lesson) & (content_df['status'] == 'approved')
        if topic and topic != "Tümü":
            mask &= (content_df['topic'] == topic)
            
        target_content = content_df[mask]
        if target_content.empty:
            return []
            
        # 2. Metinleri Birleştir (En fazla 3 fiş alalım ki token şişmesin)
        # Öncelik: Micro Lesson > Worked Example
        texts = []
        for _, row in target_content.head(3).iterrows():
            summary = row.get('summary_bullets', '')
            strategy = row.get('strategy_steps', '')
            mistakes = row.get('common_mistakes', '')
            
            # String temizliği (Liste ise stringe çevir)
            if isinstance(summary, list): summary = "\n".join(summary)
            if isinstance(strategy, list): strategy = "\n".join(strategy)
            if isinstance(mistakes, list): mistakes = "\n".join(mistakes)
            
            texts.append(f"KONU ÖZETİ:\n{summary}\n\nSTRATEJİLER:\n{strategy}\n\nHATALAR:\n{mistakes}")
            
        full_text = "\n\n---\n\n".join(texts)
        
        # 3. LLM'e Gönder
        subtopic = target_content.iloc[0]['subtopic'] if not target_content.empty else "Genel"
        topic_name = topic if topic else target_content.iloc[0]['topic']
        
        result = self.llm.generate_questions_from_text(full_text, lesson, topic_name, subtopic, count=5)
        questions = result.get("questions", [])
        
        # 4. Veritabanına Kaydet (Gelecek sefer için)
        saved_questions = []
        if questions:
            count = 0
            for q in questions:
                q_id = f"q_jit_{datetime.now().strftime('%Y%m%d%H%M%S')}_{count}"
                q_data = {
                    "question_id": q_id,
                    "lesson": lesson,
                    "topic": topic_name,
                    "subtopic": subtopic,
                    "difficulty_label": q.get("difficulty", 3),
                    "question_origin": "ai_generated_jit",
                    "origin_detail": "JIT Fallback",
                    "text": q.get("text", ""),
                    "options_json": json.dumps(q.get("options", {}), ensure_ascii=False),
                    "correct_answer": q.get("correct_answer", ""),
                    "active": True,
                    "created_at": datetime.now().isoformat()
                }
                self.db.add_data("questions", q_data)
                
                # DataFrame formatına uygun hale getir (Return için)
                q_data['option_a'] = q.get("options", {}).get("A", "")
                q_data['option_b'] = q.get("options", {}).get("B", "")
                q_data['option_c'] = q.get("options", {}).get("C", "")
                q_data['option_d'] = q.get("options", {}).get("D", "")
                saved_questions.append(q_data)
                count += 1
                
        return saved_questions

# Singleton
@st.cache_resource
def get_exam_engine() -> ExamEngine:
    return ExamEngine()
