import unittest
import os

from weewx_orm import WeewxDB


class TestWewxDB(unittest.TestCase):
    test_database_filename = '/tmp/unittest_weewx_database.db'

    def _remove_sqlite_database(self):
        try:
            os.unlink(self.test_database_filename)
        except FileNotFoundError:
            pass

    def tearDown(self):
        pass
        # self._remove_sqlite_database()

    def setUp(self):
        self._remove_sqlite_database()
        self.wdb = WeewxDB(self.test_database_filename)

    def _setup_query_database(self):
        self.entries = [
            self.wdb.tables.archive(
                dateTime = 1000,
                usUnits = 1,
                interval = 5,
                inTemp = 63,
            ),
            self.wdb.tables.archive(
                dateTime = 1010,
                usUnits = 1,
                interval = 5,
                inTemp = 64,
            ),
            self.wdb.tables.archive(
                dateTime = 1020,
                usUnits = 1,
                interval = 5,
                inTemp = 65,
            )
        ]
        with self.wdb.session as session:
            session.add_all(self.entries)
            session.commit()

    def test_archive_query_interval(self):
        self._setup_query_database()

        results = self.wdb.archive_query_interval(999, 1019)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['dateTime'], 1000)
        self.assertEqual(results[1]['dateTime'], 1010)

    def test_archive_insert_data(self):
        data = [
            self.wdb.tables.archive(
                dateTime = 1000,
                usUnits = 1,
                interval = 5,
                inTemp = 63,
                ),
            self.wdb.tables.archive(
                dateTime = 1010,
                usUnits = 1,
                interval = 5,
                inTemp = 64,
                ),
            self.wdb.tables.archive(
                dateTime = 1020,
                usUnits = 1,
                interval = 5,
                inTemp = 65,
                )
            ]

        data_dump = [self.wdb.archive_schema.dump(d).data for d in data]
        self.wdb.archive_insert_data(data_dump)

        with self.wdb.session as session:
            results = session.query(self.wdb.tables.archive).all()

        self.assertEqual(len(results), 3)
