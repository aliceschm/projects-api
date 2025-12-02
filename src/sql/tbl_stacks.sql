/* Table with list of stacks */

CREATE TABLE portfolio.stacks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL,

    CONSTRAINT stacks_name_normalized_unique UNIQUE (name_normalized)
);
