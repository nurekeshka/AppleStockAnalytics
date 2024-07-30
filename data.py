import os
import pandas
import sqlalchemy

from typing import Optional
from settings import Credentials, Data, Path


class DataManager():
    credentials = Credentials
    paths = Path
    data = Data

    engine: sqlalchemy.Engine

    __connection: str = credentials.connection.value
    __dataframe: Optional[pandas.DataFrame] = None

    filename: str = data.filename.value
    table: str = data.table.value

    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(self.connection)

    def setup(self) -> None:
        self.dataframe.to_sql(
            self.table, self.engine,
            if_exists='replace', index=False)

        print('PostgreSQL Database Setup is Done.')

    @property
    def dataframe(self) -> pandas.DataFrame:
        if self.__dataframe is not None:
            return self.__dataframe

        if not os.path.exists(self.filepath):
            raise FileNotFoundError('File doesn\'t exist.')

        self.__dataframe = pandas.read_csv(self.filepath)
        return self.__dataframe

    @property
    def filepath(self) -> str:
        return os.path.join(self.paths.data.value, self.filename)

    @property
    def connection(self) -> str:
        return self.__connection.format(
            self.credentials.user.value, self.credentials.pswd.value,
            self.credentials.host.value, self.credentials.port.value,
            self.credentials.dbnm.value)
