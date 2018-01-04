from msgpack import packb
from weewx_orm import WeewxDB

import sqlite3

import os
from pprint import pprint as pp

with open('archive_schema.sql') as f:
    conn = sqlite3.connect('weewx.sdb')
    conn.execute(f.read())
    conn.close()

db = WeewxDB('weewx.sdb')
results = db.archive_query_interval(0, 999999999)
#  pp(results)

data = [
    db.tables.archive(dateTime=99, usUnits=0, interval=0, barometer=3),
    db.tables.archive(dateTime=98, usUnits=0, interval=0, barometer=4),
    db.tables.archive(dateTime=97, usUnits=0, interval=0, barometer=5)
]
#  print(data)

data_dump = [db.archive_schema.dump(entry).data for entry in data]
#  pp(data_dump)
#  print()


#  with db.session as session:
#     data = [db.tables.archive(**entry) for entry in data_dump]
#  for entry in data:
#     print(entry.dateTime, entry.barometer)
db.archive_insert_data(packb(data_dump))

os.remove('weewx.sdb')
