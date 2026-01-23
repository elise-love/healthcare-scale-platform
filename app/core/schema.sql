PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS scales (
  scale_id   TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  short_name TEXT,
  language   TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS scale_versions (
  scale_id        TEXT NOT NULL,
  version         TEXT NOT NULL,
  definition_json TEXT NOT NULL,
  created_at      TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (scale_id, version),
  FOREIGN KEY (scale_id) REFERENCES scales(scale_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scale_items (
  scale_id     TEXT NOT NULL,
  version      TEXT NOT NULL,
  item_id      TEXT NOT NULL,
  item_order   INTEGER NOT NULL,
  text         TEXT NOT NULL,
  item_type    TEXT DEFAULT 'single_choice',
  reverse      INTEGER DEFAULT 0,  -- reverse-scored item (0/1)
  weight       REAL DEFAULT 1.0,   -- 權重
  PRIMARY KEY (scale_id, version, item_id),
  FOREIGN KEY (scale_id, version) REFERENCES scale_versions(scale_id, version) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scale_options (
  scale_id    TEXT NOT NULL,
  version     TEXT NOT NULL,
  option_key  TEXT NOT NULL,       -- defines answer options
  label       TEXT NOT NULL,
  PRIMARY KEY (scale_id, version, option_key),
  FOREIGN KEY (scale_id, version) REFERENCES scale_versions(scale_id, version) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assessments (
  assessment_id  TEXT PRIMARY KEY, -- attempt ID
  scale_id       TEXT NOT NULL,     -- scale used
  version        TEXT NOT NULL,
  subject_id     TEXT,
  total_score    REAL NOT NULL,
  interpretation TEXT,              -- optional clinical interpretation
  answers_json   TEXT NOT NULL,     -- raw answers snapshot
  created_at     TEXT DEFAULT (datetime('now')), -- submission time
  FOREIGN KEY (scale_id, version) REFERENCES scale_versions(scale_id, version)
);

CREATE TABLE IF NOT EXISTS assessment_answers (
  assessment_id TEXT NOT NULL,
  item_id       TEXT NOT NULL,
  answer_value  TEXT NOT NULL,
  score         REAL NOT NULL,
  PRIMARY KEY (assessment_id, item_id),
  FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scale_items_order
  ON scale_items(scale_id, version, item_order);

CREATE INDEX IF NOT EXISTS idx_assessments_subject_time
  ON assessments(subject_id, created_at);

CREATE INDEX IF NOT EXISTS idx_answers_item
  ON assessment_answers(item_id);
