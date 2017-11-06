from weewx_orm import WeewxDB


db = WeewxDB('weewx.sdb')
results = db.archive_query_interval(1, 12)
print([result.dateTime for result in results])
