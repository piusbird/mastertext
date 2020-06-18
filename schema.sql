CREATE TABLE IF NOT EXISTS 'hive_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'hive_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'hive_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3);
CREATE TABLE IF NOT EXISTS 'hive_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'hive_config'(k PRIMARY KEY, v) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS "collisions" (prow int not null, phash varchar(40));
CREATE TABLE IF NOT EXISTS "link" ("phash" VARCHAR(40) NOT NULL PRIMARY KEY, "count" INTEGER NOT NULL);
CREATE VIRTUAL TABLE hive USING fts5(hashid, inject_date, orighost, data)
/* hive(hashid,inject_date,orighost,data) */;
