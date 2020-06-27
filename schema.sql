CREATE TABLE IF NOT EXISTS "collisions" (prow int not null, phash varchar(40));
CREATE TABLE IF NOT EXISTS "link" ("phash" VARCHAR(40) NOT NULL PRIMARY KEY, "count" INTEGER NOT NULL);
CREATE VIRTUAL TABLE hive USING fts5(hashid, inject_date, orighost, data)
/* hive(hashid,inject_date,orighost,data) */;
