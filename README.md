# MasterText

Mastertext is a very much **prealpha** small to medium corpus free form text
storage,search, and retrieval engine. It is intended to help in things like
mind mapping, time tracking, research, creative writing... Look I'm just
building the ultimate organizational tool for people with minds like mine. So
if you think having a searchable archive of most of what you've read, over
the past five years is a *good* thing congratulations your neurodivergent.

Anyway this is intended to be wrapper around SQLite's Full Text Search 5
with a few bells, and whistles for large database (~ 2GB or so).
Inserting data via the API provides deduplication support. 

## How to use 

```sh
python3 -m venv <whatever>
source <whatever>/bin/activate
sqlite3 master.db < schema.sql
<edit your .env file and change the path's to your needs> 
./mt.py etl <directory-full-of-text-files>
```
Sorry no installer yet, after etl has run you can explore via web.py or 
the command line.


