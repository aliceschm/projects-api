/* Table with list of projects */

CREATE TYPE project_status AS ENUM (
  'idea',
  'planning',
  'in_progress',
  'paused',
  'finished',
  'archived'
);

CREATE TABLE portfolio.projects (
  id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  created_at  TIMESTAMP NOT NULL,
  updated_at  TIMESTAMP NOT NULL,
  status      project_status NOT NULL DEFAULT 'idea',
  slug        TEXT NOT NULL
);
