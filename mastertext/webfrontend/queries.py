from mastertext.models import *
from peewee import OperationalError
from mastertext.utils import MasterTextError

PERPAGE = 15


def get_latest(numents):

    results = []
    for e in Hive.select().order_by(Hive.inject_date.desc()).limit(numents):
        results.append(
            {'id': e.hashid, 'date': e.inject_date, 'sample': e.data[0:399]})
    return results


def total_pages(fts5term, items=PERPAGE):
    try:
        count_total = Hive.search(fts5term).count()
    except OperationalError as e:
        raise MasterTextError(str(e))
    return count_total // items

# We have a different search function because the webapp needs the data in a different
# way


def fulltext_search(fts5term, page=1, items=PERPAGE):
    count_total = Hive.search(fts5term).count()
    try:
        sq = Hive.search(fts5term).order_by(
            Hive.inject_date.desc()).paginate(page, items)
    except OperationalError as e:
        raise MasterTextError(str(e))
    result = []
    for e in sq:
        result.append({"total": count_total, "id": e.hashid,
                      "date": e.inject_date, "sample": e.data[0:399]})

    return result
