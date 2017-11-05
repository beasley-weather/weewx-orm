from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy import create_engine


class WeewxDB:
    def __init__(self, database_file):
        self._Base = automap_base()
        self._engine = create_engine(database_file)
        self._Base.prepare(self._engine, reflect=True)
        self._session = Session(self._engine)
        self.archive = self._Base.classes.archive
