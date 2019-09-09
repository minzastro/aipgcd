CREATE TABLE `data_references` (
	`cluster_uid`	INTEGER NOT NULL,
	`reference_table`	TEXT NOT NULL,
	`reference_uid`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "reference_tables_columns" (
	`reference_table`	TEXT,
	`column_name`	TEXT,
	`data_type`	TEXT,
	`data_unit`	TEXT,
	`output_format`	TEXT,
	`description`	TEXT,
	`uid`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ucd`	TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE `cluster_in_moc` (
	`uid`	INTEGER NOT NULL,
	`moc_name`	TEXT NOT NULL
);
CREATE TABLE [reference_tables] ([table_name] TEXT NOT NULL, [uid_column] TEXT NOT NULL, [is_string_uid] INTEGER NOT NULL DEFAULT '0', [extra_column] TEXT, [description] TEXT, [ra_column] TEXT, [dec_column] TEXT, [brief_columns] TEXT, [obs_class_global] BOOLEAN, [obs_class_value] INTEGER);
CREATE INDEX [idx_data_references] ON [data_references] ([cluster_uid]);
CREATE TABLE IF NOT EXISTS "keys"  (
    key CHAR(25) NOT NULL,
    subkey  CHAR(25),
    description VARCHAR(400),
    data_format VARCHAR(10)
);
CREATE TABLE IF NOT EXISTS "reference_tables_keys"  (
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
CREATE TABLE per_cluster_keys  (
     uid    INTEGER NOT NULL,
     key    TEXT NOT NULL,
     subkey     TEXT,
     value  TEXT,
     comment    TEXT,
     value_error_high   TEXT,
     value_error_low    TEXT
);
CREATE TABLE mocs  (
   moc_name   CHAR(20),
   moc_file   CHAR(30),
   description   TEXT,
   vizier_catalog   TEXT,
   is_full_sky   BOOLEAN NOT NULL DEFAULT (0)
);
CREATE TABLE clusters (
  uid   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  ra    REAL NOT NULL,
  dec   REAL NOT NULL,
  gal_l REAL,
  gal_b REAL,
  source    CHAR(25) NOT NULL,
  source_id TEXT,
  dec_int   INT,
  comment   TEXT,
  xid_flag  INTEGER NOT NULL DEFAULT 0,
  xid_flag_source char(25),
  xid_flag_comment text,
  obs_flag  integer NOT NULL DEFAULT 0,
  obs_flag_source char(25),
  obs_flag_comment text
);
