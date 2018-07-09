DROP TABLE IF EXISTS formula;

CREATE TABLE formula (
  title TEXT NOT NULL,
  sheet_id TEXT UNIQUE NOT NULL
);
