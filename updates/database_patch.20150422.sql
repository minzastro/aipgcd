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
