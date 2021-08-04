CREATE SCHEMA IF NOT EXISTS ml;
CREATE TABLE IF NOT EXISTS ml.accuracies (
	id SERIAL NOT NULL,
	ml_id TEXT NOT NULL,
	ml_date DATE NOT NULL,
	accuracy DECIMAL NOT NULL,
	PRIMARY KEY (ml_id, ml_date)
);