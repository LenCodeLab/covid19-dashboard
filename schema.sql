-- schema.sql

DROP TABLE IF EXISTS covid_data;

CREATE TABLE covid_data (
    id SERIAL PRIMARY KEY,
    iso_code TEXT,
    continent TEXT,
    location TEXT,
    date DATE NOT NULL,
    total_cases INTEGER,
    new_cases INTEGER,
    total_deaths INTEGER,
    new_deaths INTEGER
);

-- Optional: add indexes to speed up queries
CREATE INDEX idx_location_date ON covid_data (location, date);
