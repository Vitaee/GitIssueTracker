FROM postgres:13


RUN echo "SELECT 'CREATE DATABASE issuetracker' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'issuetracker');" >> /docker-entrypoint-initdb.d/init.sql
RUN echo "CREATE EXTENSION IF NOT EXISTS unaccent;" >> /docker-entrypoint-initdb.d/init.sql
