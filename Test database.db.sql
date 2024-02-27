BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "employee" (
	"e_name"	VARCHAR(255) NOT NULL, 
	"e_school"	VARCHAR(255) NOT NULL,
	"e_type"	VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "individual" (
	"i_performance"	VARCHAR(255) NOT NULL,
	"i_contribution"	VARCHAR(255) NOT NULL,
);
CREATE TABLE IF NOT EXISTS "project" (
	"p_performance"	VARCHAR(255) NOT NULL,
	"p_development"	VARCHAR(255) NOT NULL,
);
CREATE TABLE IF NOT EXISTS "people" (
	"pe_performance"	VARCHAR(255) NOT NULL,
	"pe_development"	VARCHAR(255) NOT NULL,
);
COMMIT;
