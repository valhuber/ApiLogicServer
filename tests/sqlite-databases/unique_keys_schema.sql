CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "SampleDBVersion"
(
    Id    integer
        constraint SampleDBVersion_pk
            primary key autoincrement,
    Notes varchar(800)
);
CREATE TABLE IF NOT EXISTS "KeyTest_unique"
(
    KeyName varchar(16)
);
CREATE UNIQUE INDEX index_name
    on "KeyTest_unique" (KeyName);
CREATE TABLE IF NOT EXISTS "NoKey_no_unqiue"
(
    just_text text
);
CREATE TABLE IF NOT EXISTS "unique_with_key"
(
    name_unique_with_pkey TEXT
        constraint users_with_key_pk
            primary key
        unique
);
CREATE TABLE IF NOT EXISTS "unique_no_key"
(
    unique_no_key_name TEXT
        unique
, created integer, pass_hash test);
CREATE TABLE IF NOT EXISTS "user_notes"
(
    user_name TEXT
        constraint user_notes_users_name_fk
            references unique_no_key (unique_no_key_name),
    note      TEXT,
    id        INTEGER not null
        constraint user_notes_pk
            primary key
);
CREATE TABLE users( name TEXT, password_hash TEXT, created BIGINT, UNIQUE(name) );
CREATE TABLE IF NOT EXISTS "unique_no_key_alt" (unique_no_key_name TEXT, created integer, pass_hash test, UNIQUE(unique_no_key_name));
