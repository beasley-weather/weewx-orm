from traceback import print_exc

from weewx_orm import WeewxDB


db = WeewxDB('weewx.sdb')
with db.session as session:
    table = db.tables.archive

    try:
        result = session.query(table)\
            .order_by(table.dateTime.desc())\
            .first()
        print(result.dateTime)
    except Exception as e:
        print_exc()
        session.rollback()
