BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Employee" (
	"e_name"	VARCHAR(255) NOT NULL, 
	"e_school"	VARCHAR(255) NOT NULL,
	"e_type"	VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "Individual" (
	"i_performance"	VARCHAR(255) NOT NULL,
	"i_contribution"	VARCHAR(255) NOT NULL,
);
CREATE TABLE IF NOT EXISTS "Project" (
	"p_performance"	VARCHAR(255) NOT NULL,
	"p_development"	VARCHAR(255) NOT NULL,
);
CREATE TABLE IF NOT EXISTS "People" (
	"pe_performance"	VARCHAR(255) NOT NULL,
	"pe_development"	VARCHAR(255) NOT NULL,
);
COMMIT;
