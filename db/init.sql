CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'Qq123456';
SELECT pg_create_physical_replication_slot('replication_slot');

SELECT 'CREATE DATABASE devops'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'devops')\gexec

CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    phone VARCHAR (100) NOT NULL
);

