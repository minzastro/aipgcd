--Renaming key_class to subkey:
CREATE TABLE  keys_new  (
    key CHAR(25) NOT NULL,
    subkey  CHAR(25),
    description VARCHAR(400),
    data_format VARCHAR(10)
);

insert into keys_new(key, subkey, description, data_format)
select key, key_class, description, data_format
  from keys;
drop table keys;
alter table keys_new rename to keys;


CREATE TABLE  reference_tables_keys_new  (
     key    TEXT NOT NULL,
     subkey     TEXT,
     reference_table    TEXT NOT NULL,
     reference_column   TEXT NOT NULL,
     is_string  INTEGER NOT NULL DEFAULT '0',
     error_column_low   TEXT,
     error_column_high  TEXT,
     comment    TEXT,
     uid    INTEGER PRIMARY KEY AUTOINCREMENT,
     comment_column     TEXT
);
insert into reference_tables_keys_new
select * from reference_tables_keys;
drop table reference_tables_keys;
alter table reference_tables_keys_new rename to reference_tables_keys;

drop table per_cluster_keys;
CREATE TABLE  per_cluster_keys  (
     uid    INTEGER NOT NULL,
     key    TEXT NOT NULL,
     subkey     TEXT,
     value  TEXT,
     comment    TEXT,
     value_error_high   TEXT,
     value_error_low    TEXT
);


-- Add obs_flag to clusters
alter table clusters add column obs_flag integer not null default 0;
