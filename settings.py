import os
import enum


class Credentials(enum.StrEnum):
    user = 'postgres'
    pswd = 'root'
    host = 'localhost'
    port = '5432'
    dbnm = 'apple'

    connection = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'


class Data(enum.StrEnum):
    filename = 'apple-stocks-2023-2024.csv'
    table = 'stocks'


class Path(enum.StrEnum):
    directory = os.path.dirname(__file__)
    data = os.path.join(directory, 'data')


class Columns(enum.StrEnum):
    date = 'Date'
    open = 'Open'
    high = 'High'
    low = 'Low'
    close = 'Close'
    adjusted = 'Adj Close'
    volume = 'Volume'
