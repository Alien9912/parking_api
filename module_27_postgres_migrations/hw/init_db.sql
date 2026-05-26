CREATE TABLE test_psql_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

GRANT ALL PRIVILEGES ON DATABASE skillbox_db TO skillbox_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO skillbox_user;
