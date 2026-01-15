"""
İçerik Üretim ve Ayrıştırma Promptları
PDF işleme, soru üretme ve şekil sınıflandırma promptları
"""

# Fiş Üretimi (Content Fiche Generation)
FICHE_GENERATION_TASK_DESCRIPTIONS = {
    "publisher_original": "PDF sayfalarındaki içeriği OLDUĞU GİBİ (OCR mantığıyla) fiş formatına çevir. Yorum katma, metni değiştirme.",
    "ai_variant_of_publisher": "PDF'teki içeriği referans alarak BENZER ama FARKLI örneklerle yeni fişler üret (Varyant).",
    "ai_generated": "PDF sayfalarından LGS düzeyi öğretici fişler üret."
}

FICHE_GENERATION_PROMPT_TEMPLATE = """
GÖREV: {task_description}
KURALLAR:
- Sadece şu alt konu için üret: {lesson}/{topic}/{subtopic}
- En fazla 15 fiş üret. Kalite > adet.
- Çıktı SADECE JSON olacak.

JSON ŞEMASI:
{{
  "fiches": [
    {{
      "content_type": "micro_lesson|worked_example",
      "difficulty_band": 1-5,
      "estimated_time_min": 3-8,
      "summary_bullets": ["5-8 madde"],
      "strategy_steps": ["3-6 adım"],
      "common_mistakes": ["2-5 madde"],
      "mini_check_stem": "tek soru",
      "mini_check_options_json": {{"A":"..","B":"..","C":"..","D":".."}},
      "mini_check_correct_option": "A|B|C|D",
      "page_ref": "PDF s.xx"
    }}
  ]
}}
"""

# Soru Ayrıştırma (Question Extraction)
QUESTION_EXTRACTION_TASK_DESCRIPTIONS = {
    "publisher_original": "Resimdeki soruları BİREBİR (OCR gibi) metne dök. Asla değiştirme, yorum katma.",
    "ai_variant_of_publisher": "Resimdeki sorulara BENZER mantıkta ama FARKLI rakam/senaryolarla YENİ sorular üret (Varyant). UYARI: Eğer soruda karmaşık bir şekil/grafik varsa ve bunu metinle anlatamıyorsan, bu soruyu ATLAMA, sadece metin tabanlı bir varyant üretmeye çalış.",
    "ai_generated": "PDF/Resimdeki LGS sorularını ayrıştır ve JSON formatına çevir."
}

QUESTION_EXTRACTION_PROMPT_TEMPLATE = """
GÖREV: {task_description}
KURALLAR:
- Ders: {lesson}, Konu: {topic}, Alt Konu: {subtopic}
- Resimdeki her bir soruyu ayrı ayrı tanımla.
- Soru metnini (OCR) olabildiğince düzgün al.
- Seçenekleri (A, B, C, D) ayır.
- Doğru cevabı (varsa işaretli, yoksa tahmin et) belirt.
- Çıktı SADECE JSON olacak.

JSON ŞEMASI:
{{
  "questions": [
    {{
      "text": "Soru metni...",
      "options": {{"A":"..","B":"..","C":"..","D":".."}},
      "correct_answer": "A|B|C|D",
      "difficulty": 1-5,
      "question_origin": "publisher|meb|ai_generated"
    }}
  ]
}}
"""

# Şekil Sınıflandırma (Figure Classification)
FIGURE_CLASSIFICATION_PROMPT_TEMPLATE = """
GÖREV: Aşağıdaki soruyu analiz et ve görsel/şekil/grafik gerektirip gerektirmediğini belirle.

SORU METNİ: {text}
SEÇENEKLER: {options_json}

ANALİZ KRİTERLERİ:
- Metinde "grafiğe göre", "şekildeki", "yandaki", "aşağıdaki görsel" gibi ifadeler var mı?
- Soruyu çözmek için görsel veri şart mı?
- Eğer görsel (image) verildiyse, görselde soruyla ilgili bir grafik/şekil var mı?

ÇIKTI FORMATI (SADECE JSON):
{{
    "has_figure": true/false,
    "figure_type": "chart|geometry|schematic|table|none",
    "confidence": 0.0-1.0 (Güven skoru),
    "reason": "Kısa açıklama"
}}
"""

# JIT Soru Üretimi (Just-in-Time Generation)
JIT_QUESTION_GENERATION_PROMPT_TEMPLATE = """
GÖREV: Aşağıdaki konu anlatım metnini kullanarak LGS (Liselere Geçiş Sınavı) formatında {count} adet çoktan seçmeli soru üret.

KONU: {lesson} - {topic} - {subtopic}

METİN İÇERİĞİ:
{text_content}

KURALLAR:
- Sorular metindeki bilgilere dayalı olmalı.
- LGS tarzı (yeni nesil, mantık muhakeme içeren) sorular olsun.
- Her soru için 4 seçenek (A, B, C, D) ve 1 doğru cevap belirle.
- Zorluk seviyesi 1-5 arasında olsun.
- Çıktı SADECE JSON olacak.

JSON ŞEMASI:
{{
  "questions": [
    {{
      "text": "Soru metni...",
      "options": {{"A":"..","B":"..","C":"..","D":".."}},
      "correct_answer": "A|B|C|D",
      "difficulty": 1-5,
      "question_origin": "ai_generated_jit"
    }}
  ]
}}
"""
