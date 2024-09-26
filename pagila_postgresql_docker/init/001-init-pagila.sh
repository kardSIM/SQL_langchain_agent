#!/bin/bash
set -e

echo "Starting Pagila database initialization..."

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE pagila;
    \c pagila
    \i /docker-entrypoint-initdb.d/002-pagila-schema.sql
    \i /docker-entrypoint-initdb.d/003-pagila-data.sql    
    CREATE ROLE pagila_dba;
    GRANT ALL ON DATABASE pagila TO pagila_dba;
    GRANT ALL ON SCHEMA public TO pagila_dba;
    GRANT ALL ON ALL TABLES IN SCHEMA public TO pagila_dba;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO pagila_dba;    
EOSQL
