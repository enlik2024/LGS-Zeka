-- =====================================================================
-- LGS-ZEKA SUPABASE TABLO OLUŞTURMA SCRIPTLERI
-- Tarih: 2026-01-20
-- Not: Bu scriptleri Supabase Dashboard > SQL Editor'de çalıştırın
-- =====================================================================

-- =====================================================================
-- 1. MEB KAZANIMLAR TABLOSU
-- Amaç: MEB müfredat kazanımlarını ve LGS öncelik puanlarını saklar
-- =====================================================================
CREATE TABLE IF NOT EXISTS meb_kazanimlar (
    kazanim_id VARCHAR(20) PRIMARY KEY,           -- Örn: M.8.1.1.1
    ders VARCHAR(50) NOT NULL,                    -- Matematik, Fen Bilimleri
    unite VARCHAR(100),                           -- Sayılar ve İşlemler
    konu VARCHAR(100) NOT NULL,                   -- Çarpanlar ve Katlar
    alt_konu VARCHAR(200),                        -- EKOK, EBOB vb.
    kazanim_metni TEXT,                           -- Tam MEB kazanım açıklaması
    sinif INT DEFAULT 8,
    lgs_soru_sayisi_3yil INT DEFAULT 0,           -- Son 3 yıl toplam soru sayısı
    oncelik_seviyesi VARCHAR(10) DEFAULT 'orta',  -- kritik/yuksek/orta/dusuk
    curriculum_map_subtopic VARCHAR(200),         -- curriculum_map.csv ile eşleşme
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_kazanimlar_ders ON meb_kazanimlar(ders);
CREATE INDEX IF NOT EXISTS idx_kazanimlar_konu ON meb_kazanimlar(konu);

-- =====================================================================
-- 2. İÇERİKLER TABLOSU
-- Amaç: NotebookLM'den çekilen tüm içerikleri saklar
-- =====================================================================
CREATE TABLE IF NOT EXISTS icerikler (
    icerik_id VARCHAR(30) PRIMARY KEY,            -- Örn: NB-MAT-001
    kazanim_id VARCHAR(20) REFERENCES meb_kazanimlar(kazanim_id),
    
    -- İçerik meta bilgileri
    icerik_tipi VARCHAR(30) NOT NULL,             -- video/flashcard/quiz/infographic/guide/audio
    kaynak_tipi VARCHAR(30) DEFAULT 'notebooklm', -- notebooklm/youtube/ai_generated/manual
    baslik VARCHAR(300),
    aciklama TEXT,
    
    -- NotebookLM kaynak bilgileri
    notebook_url VARCHAR(500),                    -- Orijinal notebook linki
    notebooklm_item_name VARCHAR(200),            -- Studio'daki item adı
    
    -- Medya bilgileri
    video_url VARCHAR(500),                       -- Video/Audio URL
    image_path VARCHAR(500),                      -- Supabase Storage path (infografik vs)
    pdf_path VARCHAR(500),                        -- PDF dosya yolu
    
    -- İçerik detayları (JSON)
    icerik_json JSONB,                            -- Tip'e göre değişken yapı
    
    -- Eğitim meta bilgileri
    zorluk_seviyesi INT DEFAULT 3 CHECK (zorluk_seviyesi BETWEEN 1 AND 5),
    tahmini_sure_dk INT,
    etiketler TEXT[],                             -- ['üslü', 'çarpma', 'bölme']
    
    -- Durum
    status VARCHAR(20) DEFAULT 'draft',           -- draft/approved/archived
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_icerikler_kazanim ON icerikler(kazanim_id);
CREATE INDEX IF NOT EXISTS idx_icerikler_tipi ON icerikler(icerik_tipi);
CREATE INDEX IF NOT EXISTS idx_icerikler_status ON icerikler(status);

-- =====================================================================
-- 3. FLASHCARDS TABLOSU (GELİŞTİRİLMİŞ)
-- Amaç: Spaced Repetition destekli flashcard sistemi
-- =====================================================================
CREATE TABLE IF NOT EXISTS flashcards_v2 (
    id SERIAL PRIMARY KEY,
    icerik_id VARCHAR(30) REFERENCES icerikler(icerik_id),
    kazanim_id VARCHAR(20) REFERENCES meb_kazanimlar(kazanim_id),
    
    -- Kart içeriği
    front TEXT NOT NULL,                          -- Soru / Ön yüz
    back TEXT NOT NULL,                           -- Cevap / Arka yüz
    hint TEXT,                                    -- Opsiyonel ipucu
    
    -- Kategorizasyon
    lesson VARCHAR(50),                           -- Matematik
    topic VARCHAR(100),                           -- Kareköklü İfadeler
    subtopic VARCHAR(200),                        -- Toplama ve Çıkarma
    
    -- Zorluk ve etiketler
    difficulty VARCHAR(10) DEFAULT 'medium',      -- easy/medium/hard
    tags TEXT[],                                  -- ['karekök', 'toplama']
    
    -- Spaced Repetition (SM-2 algoritması için)
    ease_factor FLOAT DEFAULT 2.5,
    interval_days INT DEFAULT 1,
    repetitions INT DEFAULT 0,
    next_review_date DATE DEFAULT CURRENT_DATE,
    
    -- Meta
    source VARCHAR(50) DEFAULT 'notebooklm',      -- notebooklm/manual/ai_generated
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for spaced repetition queries
CREATE INDEX IF NOT EXISTS idx_flashcards_review ON flashcards_v2(next_review_date);
CREATE INDEX IF NOT EXISTS idx_flashcards_kazanim ON flashcards_v2(kazanim_id);
CREATE INDEX IF NOT EXISTS idx_flashcards_topic ON flashcards_v2(lesson, topic, subtopic);

-- =====================================================================
-- 4. LGS SORU ARŞİVİ
-- Amaç: 2018-2025 LGS sorularını saklar
-- =====================================================================
CREATE TABLE IF NOT EXISTS lgs_arsiv (
    soru_id VARCHAR(30) PRIMARY KEY,              -- Örn: LGS-2024-MAT-15
    yil INT NOT NULL CHECK (yil BETWEEN 2018 AND 2030),
    ders VARCHAR(50) NOT NULL,
    
    -- Kazanım eşleştirme
    kazanim_id VARCHAR(20) REFERENCES meb_kazanimlar(kazanim_id),
    konu VARCHAR(100),
    alt_konu VARCHAR(200),
    
    -- Soru içeriği
    soru_metni TEXT,
    secenekler JSONB,                             -- {"A": "...", "B": "...", "C": "...", "D": "..."}
    dogru_cevap CHAR(1) CHECK (dogru_cevap IN ('A', 'B', 'C', 'D')),
    cozum_aciklamasi TEXT,
    
    -- Görsel
    gorsel_url VARCHAR(500),                      -- Supabase Storage path
    
    -- Zorluk ve etiketler
    zorluk_seviyesi INT DEFAULT 3 CHECK (zorluk_seviyesi BETWEEN 1 AND 5),
    etiketler TEXT[],                             -- ['geometri', 'alan', 'çember']
    
    -- İstatistikler (opsiyonel)
    dogru_orani FLOAT,                            -- Türkiye geneli doğru oranı
    
    -- Meta
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_lgs_yil ON lgs_arsiv(yil);
CREATE INDEX IF NOT EXISTS idx_lgs_ders ON lgs_arsiv(ders);
CREATE INDEX IF NOT EXISTS idx_lgs_kazanim ON lgs_arsiv(kazanim_id);

-- =====================================================================
-- 5. NOTEBOOKLM IMPORT KAYITLARI
-- Amaç: NotebookLM'den yapılan import'ları takip eder
-- =====================================================================
CREATE TABLE IF NOT EXISTS notebooklm_imports (
    import_id SERIAL PRIMARY KEY,
    notebook_url VARCHAR(500) NOT NULL,
    notebook_title VARCHAR(300),
    
    -- İçerik özeti
    items_found INT DEFAULT 0,
    items_imported INT DEFAULT 0,
    import_summary JSONB,                         -- Detaylı import bilgisi
    
    -- Eşleştirme
    kazanim_ids TEXT[],                           -- Eşleştirilen kazanımlar
    
    -- Durum
    status VARCHAR(20) DEFAULT 'pending',         -- pending/completed/failed
    error_message TEXT,
    
    -- Meta
    imported_by VARCHAR(50) DEFAULT 'system',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================================
-- 6. ÖĞRENCİ İLERLEME TAKİBİ (Kazanım bazlı)
-- Amaç: Öğrencinin kazanım bazlı ilerlemesini takip eder
-- =====================================================================
CREATE TABLE IF NOT EXISTS ogrenci_kazanim_ilerleme (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    kazanim_id VARCHAR(20) REFERENCES meb_kazanimlar(kazanim_id),
    
    -- İlerleme metrikleri
    mastery_level VARCHAR(20) DEFAULT 'baslanmadi', -- baslanmadi/ogreniyor/pratik/uzman/usta
    quiz_dogru_sayisi INT DEFAULT 0,
    quiz_toplam_sayisi INT DEFAULT 0,
    flashcard_review_count INT DEFAULT 0,
    
    -- Son aktivite
    last_activity_date TIMESTAMP WITH TIME ZONE,
    
    -- Meta
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(student_id, kazanim_id)
);

CREATE INDEX IF NOT EXISTS idx_ilerleme_student ON ogrenci_kazanim_ilerleme(student_id);

-- =====================================================================
-- ROW LEVEL SECURITY (Opsiyonel - Çoklu öğrenci için)
-- =====================================================================
-- ALTER TABLE ogrenci_kazanim_ilerleme ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Users can only see their own progress" 
--     ON ogrenci_kazanim_ilerleme FOR ALL 
--     USING (student_id = auth.uid()::text);

-- =====================================================================
-- TAMAMLANDI! 
-- Bu scripti çalıştırdıktan sonra tablolar hazır olacak.
-- =====================================================================
