from traceback import print_exc

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine


class WeewxDB:
    def __init__(self, database_file):
        '''
        :param database_file: Path to the sqlite database
        '''
        self._database_file = 'sqlite:///' + database_file

        self._engine = create_engine(self._database_file)
        self._Base = automap_base()
        self._Base.prepare(self._engine, reflect=True)
        self.session = Session(sessionmaker(bind=self._engine))

        self.tables = self._Base.classes

    def archive_query_interval(self, _from, to):
        '''
        :param _from: Start of interval (int)
        :param to: End of interval (int)
        '''
        with self.session as session:
            table = self.tables.archive

            try:
                return session.query(table)\
                    .filter(table.dateTime >= _from)\
                    .filter(table.dateTime < to)\
                    .all()
            except Exception as e:
                print_exc()
                session.rollback()


class Session:
    def __init__(self, session_maker):
        self._session_maker = session_maker
        self._session = None

    def __enter__(self):
        self._session = self._session_maker()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()
