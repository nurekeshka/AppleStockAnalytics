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
    images = os.path.join(directory, 'images')


class Columns(enum.StrEnum):
    date = 'Date'
    open = 'Open'
    high = 'High'
    low = 'Low'
    close = 'Close'
    adjusted = 'Adj Close'
    volume = 'Volume'

    twenty_days_sma = '20_Day_SMA'
    fifty_days_sma = '50_Day_SMA'

    twenty_days_std = '20_Day_STD'
    fifty_days_std = '50_Day_STD'

    upper_band = 'Upper_Band'
    lower_band = 'Lower_Band'

    daily_return = 'Daily_Return'
    cumulative = 'Cumulative_Return'
    rsi = 'RSI'

    volatility = 'Volatility'
