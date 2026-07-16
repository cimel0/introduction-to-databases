-- Tabelle der Kantone
CREATE TABLE canton (
  canton_short TEXT PRIMARY KEY,
  canton_name  TEXT NOT NULL,
  UNIQUE (canton_name)
);

-- Tabelle der Bezirke
CREATE TABLE district (
  district_id   INTEGER PRIMARY KEY,
  distric_name  TEXT NOT NULL,
  canton_short  TEXT NOT NULL,
  FOREIGN KEY (canton_short) REFERENCES canton(canton_short)
);

-- Tabelle der Gemeinden
CREATE TABLE municipality (
  municipality_id   INTEGER PRIMARY KEY,
  municipality_name TEXT NOT NULL,
  hist_nr           INTEGER UNIQUE,
  join_date         TEXT NOT NULL,
  district_id       INTEGER NOT NULL,
  FOREIGN KEY (district_id) REFERENCES district(district_id)
);

