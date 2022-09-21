/* Updated 9-21-2022 
  Some of these tables aren't used yet some
  Are temp tables used by the the fsck tools, and friends. 
  Best to leave them all here until we get further in the 
  Dev cycle
   */
CREATE TABLE IF NOT EXISTS 'hive_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'hive_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'hive_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3);
CREATE TABLE IF NOT EXISTS 'hive_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'hive_config'(k PRIMARY KEY, v) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS "collisions" (prow int not null, phash varchar(40));
CREATE TABLE IF NOT EXISTS "link" ("phash" VARCHAR(40) NOT NULL PRIMARY KEY, "count" INTEGER NOT NULL);
CREATE VIRTUAL TABLE hive USING fts5(hashid, inject_date, orighost, data)
/* hive(hashid,inject_date,orighost,data) */;
CREATE TABLE IF NOT EXISTS "bookmark" ("name" VARCHAR(250) NOT NULL PRIMARY KEY, "phash" VARCHAR(40) NOT NULL);
CREATE TABLE metadata (
phash varchar(40)
,
size int
);
CREATE TABLE IF NOT EXISTS "newuser" ("id" INTEGER NOT NULL PRIMARY KEY, "username" VARCHAR(64) NOT NULL, "email" TEXT NOT NULL, "password_hash" VARCHAR(128) NOT NULL);
CREATE UNIQUE INDEX "newuser_username" ON "newuser" ("username");
CREATE UNIQUE INDEX "newuser_email" ON "newuser" ("email");
