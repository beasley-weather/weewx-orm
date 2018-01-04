from traceback import print_exc

import msgpack
from sqlalchemy_utils import database_exists
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class WeewxDB:
    _ARCHIVE_SCHEMA_FILENAME = 'archive_schema.sql'

    def __init__(self, database_file):
        '''
        :param database_file: Path to the sqlite database
        '''
        self._database_file = 'sqlite:///' + database_file

        self._engine = create_engine(self._database_file)

        if not database_exists(self._database_file):
            self._init_database(self._database_file)

        self._Base = automap_base()
        self._Base.prepare(self._engine, reflect=True)
        self.session = Session(sessionmaker(bind=self._engine))

        self.tables = self._Base.classes

        class ArchiveSchema(ModelSchema):
            class Meta:
                model = self.tables.archive

        self.archive_schema = ArchiveSchema()

    def archive_query_interval(self, _from, to):
        '''
        :param _from: Start of interval (int) (inclusive)
        :param to: End of interval (int) (exclusive)
        '''
        with self.session as session:
            table = self.tables.archive

            try:
                results = session.query(table)\
                    .filter(table.dateTime >= _from)\
                    .filter(table.dateTime < to)\
                    .all()

                dump = [self.archive_schema.dump(entry).data
                        for entry in results]
                return msgpack.packb(dump)
            except Exception as e:
                print_exc()
                session.rollback()

    def archive_insert_data(self, data_bin):
        '''
        :param data: Archive table data
        :type data: list[archive]
        '''
        data_dump = msgpack.unpackb(data_bin, encoding='utf-8')
        with self.session as session:
            try:
                data = [self.tables.archive(**entry) for entry in data_dump]

                session.add_all(data)
                session.commit()
            except Exception as e:
                print_exc()
                session.rollback()

    def _init_database(self, database_uri):
        with self._engine.connect() as con:
            sql = open(WeewxDB._ARCHIVE_SCHEMA_FILENAME).read()
            con.execute(sql)

    def _database_exists(self, database_uri):
        db = sqlalchemy.create_engine(database_uri)
        try:
            _ = db.connect()
            _.close()
            return True
        except sqlalchemy.exc.OperationalError:
            return False


class Session:
    def __init__(self, session_maker):
        self._session_maker = session_maker
        self._session = None

    def __enter__(self):
        self._session = self._session_maker()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()
