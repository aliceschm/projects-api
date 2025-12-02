/* Table with project details for each language*/

CREATE TABLE portfolio.project_desc (
  project_id  INTEGER NOT NULL REFERENCES portfolio.projects(id) ON DELETE CASCADE,
  name        TEXT NOT NULL DEFAULT '',
  about       TEXT,
  full_desc   TEXT,
  lang        TEXT NOT NULL DEFAULT 'pt',
  CONSTRAINT lang_check CHECK (lang IN ('pt', 'en', 'es')),
  CONSTRAINT project_desc_pk PRIMARY KEY (project_id, lang)
);
