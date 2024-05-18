create user ${DB_REPL_USER} with replication encrypted password ${DB_REPL_PASSWORD};
select pg_create_physical_replication_slot('replication_slot');

DO $$ 
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'devops') THEN
    CREATE DATABASE pt_db;
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    phone VARCHAR (100) NOT NULL
);

