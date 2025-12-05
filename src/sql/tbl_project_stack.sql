-- Table that links each project to each stack 

CREATE TABLE portfolio.project_stack (
  project_id  INTEGER NOT NULL REFERENCES portfolio.projects(id) ON DELETE CASCADE,
  stack_id    INTEGER NOT NULL REFERENCES portfolio.stacks(id),
  
  CONSTRAINT project_stack_pkey PRIMARY KEY (project_id, stack_id)
);
