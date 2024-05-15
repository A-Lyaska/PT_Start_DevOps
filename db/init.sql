-- Создание пользователя для репликации
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'Qq123456';
SELECT pg_create_physical_replication_slot('replication_slot');

-- Создание базы данных devops, если она не существует
SELECT 'CREATE DATABASE devops'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'devops')\gexec

-- Создание таблиц для хранения email и телефонных номеров
CREATE TABLE IF NOT EXISTS Emails (
    ID SERIAL PRIMARY KEY,
    Email VARCHAR (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS PhoneNums (
    ID SERIAL PRIMARY KEY,
    PhoneNum VARCHAR (100) NOT NULL
);

