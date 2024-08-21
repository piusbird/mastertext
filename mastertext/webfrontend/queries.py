"""Misc Database Queries for webfrontend"""

from peewee import OperationalError
from mastertext.models import Hive, Bookmark
from mastertext.utils import MasterTextError


PERPAGE = 15


def get_bookmarks(numents):
    rl = []
    for e in Bookmark.select().limit(numents):
        ir = Hive.select(Hive.inject_date).where(Hive.hashid == e.phash).limit(1)
        il = [i.inject_date for i in ir]
        rl.append({"name": e.name, "id": e.phash, "date": il[0]})
    return rl


def get_latest(numents):
    results = []
    for e in Hive.select().order_by(Hive.inject_date.desc()).limit(numents):
        sampledata = e.data[0:399]
        try:
            sampledata = sampledata.decode()
        except (UnicodeDecodeError, AttributeError):
            pass
        results.append({"id": e.hashid, "date": e.inject_date, "sample": sampledata})
    return results


def total_pages(fts5term, items=PERPAGE):
    try:
        count_total = Hive.search(fts5term).count()
    except OperationalError as e:
        raise MasterTextError(str(e)) from e
    return count_total // items


# We have a different search function because the webapp needs the data in a different
# way


def fulltext_search(fts5term, page=1, items=PERPAGE):
    count_total = Hive.search(fts5term).count()
    try:
        sq = (
            Hive.search(fts5term)
            .order_by(Hive.inject_date.desc())
            .paginate(page, items)
        )
    except OperationalError as e:
        raise MasterTextError(str(e)) from e
    result = []
    for e in sq:
        sampledata = e.data[0:399]
        try:
            sampledata = sampledata.decode()
        except (UnicodeDecodeError, AttributeError):
            pass
        result.append(
            {
                "total": count_total,
                "id": e.hashid,
                "date": e.inject_date,
                "sample": sampledata,
            }
        )

    return result
