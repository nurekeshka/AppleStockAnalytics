import abc
import copy
import pandas

import matplotlib.pyplot as plt
import plotly.graph_objects as go  # type: ignore

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from typing import Tuple
from settings import Columns


class AbstractVisualization(abc.ABC):
    dataframe: pandas.DataFrame
    columns = Columns

    def __init__(self, dataframe: pandas.DataFrame) -> None:
        self.dataframe = self.clean(dataframe)

    @abc.abstractmethod
    def visualize(self) -> Tuple[Figure, Axes] | go.Figure:
        ''' Please include visualization logic here. '''

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        ''' Please include data cleaning logic here. '''
        return copy.deepcopy(dataframe)


class MatplotLibVisualization(AbstractVisualization):
    size: Tuple[int, int] = (10, 6)

    @abc.abstractmethod
    def visualize(self) -> Tuple[Figure, Axes]:
        ''' Should return tuple with figure and axes. '''

    def plot(self) -> Tuple[Figure, Axes]:
        return plt.subplots(figsize=self.size)


class PlotlyVisualization(AbstractVisualization):
    @abc.abstractmethod
    def visualize(self) -> go.Figure:
        ''' You have to return go.Figure type. '''


class PriceFigureVisualization(MatplotLibVisualization):
    title: str = 'Apple Stock Close Price'
    context: str = 'Close Price'
    xlabel: str = 'Date'
    ylabel: str = 'Close Price (USD)'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(self.dataframe[self.columns.close.value], label=self.context)
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.legend()
        ax.grid(True)
        return fig, ax

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.date.value] = pandas.to_datetime(
            dataframe[self.columns.date.value])
        dataframe.set_index(self.columns.date.value, inplace=True)

        return dataframe


class PriceCandleVisualization(PlotlyVisualization):
    title: str = 'Apple Stock Price'
    context: str = 'Price'
    xlabel: str = 'Date'
    ylabel: str = 'Price (USD)'

    def visualize(self) -> go.Figure:
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
        return fig

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.date.value] = pandas.to_datetime(
            dataframe[self.columns.date.value])
        dataframe.set_index(self.columns.date.value, inplace=True)

        return dataframe


class MovingAveragesVisualization(MatplotLibVisualization):
    twenty_days_label: str = '20-Day SMA'
    fifty_days_label: str = '50-Day SMA'

    context: str = 'Close Price'
    title: str = 'Apple Stock Price with Moving Averages'
    xlabel: str = 'Date'
    ylabel: str = 'Price (USD)'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(self.dataframe[self.columns.close.value], label=self.context)
        ax.plot(
            self.dataframe[self.columns.twenty_days_sma.value],
            label=self.twenty_days_label)
        ax.plot(
            self.dataframe[self.columns.fifty_days_sma.value],
            label=self.fifty_days_label)

        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.legend()
        ax.grid(True)
        return fig, ax

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.twenty_days_sma.value] = dataframe[
            self.columns.close.value].rolling(window=20).mean()
        dataframe[self.columns.fifty_days_sma.value] = dataframe[
            self.columns.close.value].rolling(window=50).mean()

        return dataframe


class DailyReturnsVisualization(MatplotLibVisualization):
    xlabel: str = 'Date'
    ylabel: str = Columns.daily_return.value
    title: str = 'Apple Stock Daily Returns'
    context: str = 'Daily Return'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(
            self.dataframe[self.columns.daily_return.value],
            label=self.context)
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.legend()
        ax.grid(True)

        return fig, ax

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.daily_return.value] = dataframe[
            self.columns.close.value].pct_change()

        return dataframe


class CumulativeReturnVisualization(DailyReturnsVisualization):
    context: str = 'Cumulative Return'
    title: str = 'Apple Stock Cumulative Returns'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(
            self.dataframe[self.columns.cumulative.value],
            label=self.context)
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.context)
        ax.legend()
        ax.grid(True)
        return fig, ax

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)

        dataframe[self.columns.cumulative.value] = (
            1 + dataframe[self.columns.daily_return.value]).cumprod()

        return dataframe


class VolumeAnalysisVisualization(PriceFigureVisualization):
    context: str = 'Volume'
    title: str = 'Apple Stock Trading Volume'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(self.dataframe[self.columns.volume.value], label=self.context)
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.columns.volume.value)
        ax.legend()
        ax.grid(True)
        return fig, ax


class BollingerBandsVisualization(MovingAveragesVisualization):
    upper_band_label: str = 'Upper Bollinger Band'
    lower_band_label: str = 'Lower Bollinger Band'
    title: str = 'Apple Stock Price with Bollinger Bands'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(self.dataframe[self.columns.close.value], label=self.context)
        ax.plot(
            self.dataframe[self.columns.twenty_days_sma],
            label=self.twenty_days_label)
        ax.plot(
            self.dataframe[self.columns.upper_band.value],
            label=self.upper_band_label)
        ax.plot(
            self.dataframe[self.columns.lower_band.value],
            label=self.lower_band_label)
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.legend()
        ax.grid(True)
        return fig, ax

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


class RelativeStrengthIndexVisualization(MatplotLibVisualization):
    title: str = 'Apple Stock RSI'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(
            self.dataframe[self.columns.rsi.value],
            label=self.columns.rsi.value)
        ax.set_title(self.title)
        ax.set_xlabel(self.columns.date.value)
        ax.set_ylabel(self.columns.rsi.value)
        ax.legend()
        ax.grid(True)

        return fig, ax

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


class DescribeVisualization(PlotlyVisualization):
    title: str = 'Summary Statistics Table'

    def visualize(self) -> go.Figure:
        desc = self.dataframe.describe().transpose()
        desc = desc.round(3)
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Property'] + list(desc.columns),
                fill_color='paleturquoise',
                align='left',
                height=30,
                font_size=12
            ),
            cells=dict(
                values=[desc.index] +
                [desc[col].values for col in desc.columns],
                fill_color='lavender',
                align='left',
                height=30,
                font_size=12
            )
        )])

        fig.update_layout(
            title=self.title,
            width=1200,
            height=600)
        return fig


class VolatilityAnalysis(DailyReturnsVisualization):
    context: str = '20-Day Rolling Volatility'
    title: str = 'Apple Stock Volatility'

    def visualize(self) -> Tuple[Figure, Axes]:
        fig, ax = self.plot()
        ax.plot(self.dataframe[self.columns.volatility.value],
                label=self.context)
        ax.set_title(self.title)
        ax.set_xlabel(self.columns.date.value)
        ax.set_ylabel(self.columns.volume.value)
        ax.legend()
        ax.grid(True)
        return fig, ax

    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        dataframe = super().clean(dataframe)
        dataframe[self.columns.volatility.value] = dataframe[
            self.columns.daily_return.value].rolling(window=20).std()

        return dataframe
