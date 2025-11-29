/* Table with list of stacks */

CREATE TABLE portfolio.stacks (
  id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  TEXT NOT NULL
);
