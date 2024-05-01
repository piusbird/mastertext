"""Misc Database Queries for webfrontend"""
from peewee import OperationalError
from mastertext.models import Hive
from mastertext.utils import MasterTextError

PERPAGE = 15


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
            sampledata =  sampledata.decode()
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
