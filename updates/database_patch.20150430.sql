CREATE TABLE  mocs  (
   moc_name   CHAR(20),
   moc_file   CHAR(30),
   description   TEXT,
   vizier_catalog   TEXT,
   is_full_sky   BOOLEAN NOT NULL DEFAULT (0)
);

CREATE TABLE  cluster_in_moc  (
   uid   INTEGER NOT NULL,
   moc_name   TEXT NOT NULL
);
