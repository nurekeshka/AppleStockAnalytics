import copy
import pandas
import matplotlib.pyplot as plt
import plotly.graph_objects as go  # type: ignore

from typing import Optional, Tuple
from settings import Path, Columns
from data import DataManager


class Presentation():
    paths = Path
    columns = Columns

    options = ['matplotlib', 'plotly']

    manager: DataManager

    __dataframe: Optional[pandas.DataFrame] = None

    title: str = 'Apple Stock Close Price'
    context: str = 'Close Price'
    xlabel: str = 'Date'
    ylabel: str = 'Close Price (USD)'
    size: Tuple[int, int] = (10, 6)

    def __init__(self) -> None:
        self.manager = DataManager()

    def plotly(self) -> None:
        fig = go.Figure(data=[
            go.Candlestick(
                x=self.dataframe.index,
                open=self.dataframe[self.columns.open.value],
                high=self.dataframe[self.columns.high.value],
                low=self.dataframe[self.columns.low.value],
                close=self.dataframe[self.columns.close.value],
                name=self.context)])
        fig.update_layout(
            title=self.title,
            xaxis_title=self.xlabel,
            yaxis_title=self.ylabel,
            xaxis_rangeslider_visible=False)
        fig.show()

    def matplotlib(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(self.dataframe[self.columns.close.value], label=self.context)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    @property
    def dataframe(self) -> pandas.DataFrame:
        if self.__dataframe is not None:
            return self.__dataframe

        self.__dataframe = self.clean(self.manager.dataframe)
        return self.__dataframe

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        df = copy.deepcopy(dataframe)

        df[self.columns.date.value] = pandas.to_datetime(
            df[self.columns.date.value])
        df.set_index(self.columns.date.value, inplace=True)

        return df
