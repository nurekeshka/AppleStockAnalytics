import abc
import copy
import pandas

import matplotlib.pyplot as plt
import plotly.graph_objects as go  # type: ignore


from typing import Tuple
from settings import Columns


class AbstractVisualization(abc.ABC):
    dataframe: pandas.DataFrame
    columns = Columns

    def __init__(self, dataframe: pandas.DataFrame) -> None:
        self.dataframe = self.clean(dataframe)

    @ abc.abstractmethod
    def visualize(self) -> None:
        ''' Please include visualization logic here. '''

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        ''' Please include data cleaning logic here. '''
        return copy.deepcopy(dataframe)


class PriceFigureVisualization(AbstractVisualization):
    title: str = 'Apple Stock Close Price'
    context: str = 'Close Price'
    xlabel: str = 'Date'
    ylabel: str = 'Close Price (USD)'
    size: Tuple[int, int] = (10, 6)

    def visualize(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(self.dataframe[self.columns.close.value], label=self.context)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.date.value] = pandas.to_datetime(
            dataframe[self.columns.date.value])
        dataframe.set_index(self.columns.date.value, inplace=True)

        return dataframe


class PriceCandleVisualization(PriceFigureVisualization):
    def visualize(self) -> None:
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


class MovingAveragesVisualization(AbstractVisualization):
    twenty_days_label: str = '20-Day SMA'
    fifty_days_label: str = '50-Day SMA'

    context: str = 'Close Price'
    title: str = 'Apple Stock Price with Moving Averages'
    xlabel: str = 'Date'
    ylabel: str = 'Price (USD)'
    size: Tuple[int, int] = (10, 6)

    def visualize(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(self.dataframe[self.columns.close.value], label=self.context)
        plt.plot(
            self.dataframe[self.columns.twenty_days_sma.value],
            label=self.twenty_days_label)
        plt.plot(
            self.dataframe[self.columns.fifty_days_sma.value],
            label=self.fifty_days_label)

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe['20_Day_MA'] = dataframe['Close'].rolling(window=20).mean()
        dataframe['50_Day_MA'] = dataframe['Close'].rolling(window=50).mean()

        return dataframe


class DailyReturnsVisualization(AbstractVisualization):
    xlabel: str = 'Date'
    ylabel: str = Columns.daily_return.value
    title: str = 'Apple Stock Daily Returns'
    context: str = 'Daily Return'
    size: Tuple[int, int] = (10, 6)

    def visualize(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(
            self.dataframe[self.columns.daily_return.value],
            label=self.context)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.daily_return.value] = dataframe[
            self.columns.close.value].pct_change()

        return dataframe


class CumulativeReturnVisualization(DailyReturnsVisualization):
    context: str = 'Cumulative Return'
    title: str = 'Apple Stock Cumulative Returns'

    def visualize(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(
            self.dataframe[self.columns.cumulative.value],
            label=self.context)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.context)
        plt.legend()
        plt.grid(True)
        plt.show()

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.cumulative.value] = (
            1 + dataframe[self.columns.daily_return.value]).cumprod()

        return dataframe


class VolumeAnalysisVisualization(PriceFigureVisualization):
    context: str = 'Volume'
    title: str = 'Apple Stock Trading Volume'

    def visualize(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(self.dataframe[self.columns.value], label=self.context)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.columns.volume.value)
        plt.legend()
        plt.grid(True)
        plt.show()


class BollingerBandsVisualization(MovingAveragesVisualization):
    upper_band_label: str = 'Upper Bollinger Band'
    lower_band_label: str = 'Lower Bollinger Band'
    title: str = 'Apple Stock Price with Bollinger Bands'

    def visualize(self) -> None:
        plt.figure(figsize=(10, 6))
        plt.plot(self.dataframe[self.columns.close.value], label=self.context)
        plt.plot(
            self.dataframe[self.columns.twenty_days_sma],
            label=self.twenty_days_label)
        plt.plot(
            self.dataframe[self.columns.upper_band.value],
            label=self.upper_band_label)
        plt.plot(
            self.dataframe[self.columns.lower_band.value],
            label=self.lower_band_label)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.twenty_days_sma.value] = dataframe[
            self.columns.close.value].rolling(window=20).mean()
        dataframe[self.columns.twenty_days_std.value] = dataframe[
            self.columns.close.value].rolling(window=20).std()

        dataframe[self.columns.upper_band.value] = dataframe[
            self.columns.twenty_days_sma.value] + (
                dataframe[self.columns.twenty_days_std.value] * 2)
        dataframe[self.columns.lower_band.value] = dataframe[
            self.columns.twenty_days_sma.value] - (
                dataframe[self.columns.twenty_days_std.value] * 2)

        return dataframe


class RelativeStrengthIndexVisualization(AbstractVisualization):
    size: Tuple[int, int] = (10, 6)
    title: str = 'Apple Stock RSI'

    def visualize(self) -> None:
        plt.figure(figsize=self.size)
        plt.plot(
            self.dataframe[self.columns.rsi.value],
            label=self.columns.rsi.value)
        plt.title(self.title)
        plt.xlabel(self.columns.date.value)
        plt.ylabel(self.columns.rsi.value)
        plt.legend()
        plt.grid(True)
        plt.show()

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.rsi.value] = self.calculate(
            dataframe[self.columns.close.value], 14)

        return dataframe

    def calculate(self, series: pandas.Series, window: int) -> pandas.Series:
        delta = series.diff()

        gain = (delta.where(delta > 0, 0)).fillna(0)  # type: ignore
        loss = (-delta.where(delta < 0, 0)).fillna(0)  # type: ignore

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi


class DescribeVisualization(AbstractVisualization):
    def visualize(self) -> None:
        print(self.dataframe.describe())
