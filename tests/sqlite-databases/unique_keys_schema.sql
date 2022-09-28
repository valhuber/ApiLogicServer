(venv) val@Vals-MPB-14 sqlite-databases % sqlite3 unique_keys.sqlite
SQLite version 3.39.0 2022-06-30 02:14:17
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "SampleDBVersion"
(
    Id    integer
        constraint SampleDBVersion_pk
            primary key autoincrement,
    Notes varchar(800)
);
CREATE TABLE users( name TEXT, password_hash TEXT, created BIGINT, UNIQUE(name) );
CREATE TABLE IF NOT EXISTS "user_notes"
(
    user_name TEXT
        constraint user_notes_users_name_fk
            references users (name),
    note      TEXT,
    id        INTEGER not null
        constraint user_notes_pk
            primary key
);
CREATE TABLE IF NOT EXISTS "KeyTest"
(
    KeyName varchar(16)
);
CREATE UNIQUE INDEX index_name
    on KeyTest (KeyName);
CREATE TABLE NoKey
(
    just_text text
);
CREATE TABLE IF NOT EXISTS "users_with_key"
(
    name_unique_with_pkey TEXT
        constraint users_with_key_pk
            primary key
        unique
);
