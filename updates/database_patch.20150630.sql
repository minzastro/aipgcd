alter table clusters rename to clusters_old;
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
insert into clusters(uid, ra, dec, gal_l, gal_b, source, source_id, dec_int, comment,
xid_flag, obs_flag)
select uid, ra, dec, gal_l, gal_b, source, source_id, dec_int, comment,
xidflag, obs_flag
from clusters_old;
drop table clusters_old;