from typing import Tuple, Literal, Dict, Type, get_args
from settings import Path, Columns
from data import DataManager

import matplotlib.pyplot as plt
import visualizations
import os


class Presentation():
    paths = Path
    columns = Columns

    options = Literal[
        'prices', 'candles',
        'describe', 'averages',
        'daily_returns', 'cumulative_returns',
        'volume', 'bollinger', 'rsi', 'volatility']

    mapping: Dict[str, Type[visualizations.AbstractVisualization]] = {
        'prices': visualizations.PriceFigureVisualization,
        'candles': visualizations.PriceCandleVisualization,
        'describe': visualizations.DescribeVisualization,
        'averages': visualizations.MovingAveragesVisualization,
        'daily_returns': visualizations.DailyReturnsVisualization,
        'cumulative_returns': visualizations.CumulativeReturnVisualization,
        'volume': visualizations.VolumeAnalysisVisualization,
        'bollinger': visualizations.BollingerBandsVisualization,
        'rsi': visualizations.RelativeStrengthIndexVisualization,
        'volatility': visualizations.VolatilityAnalysis}

    manager: DataManager

    title: str = 'Apple Stock Close Price'
    context: str = 'Close Price'
    xlabel: str = 'Date'
    ylabel: str = 'Close Price (USD)'
    size: Tuple[int, int] = (10, 6)

    def __init__(self) -> None:
        self.manager = DataManager()

    def visualize(self, name: options) -> None:
        visualization = self.get(name)

        if isinstance(visualization, visualizations.MatplotLibVisualization):
            visualization.visualize()
            plt.show()
        elif isinstance(visualization, visualizations.PlotlyVisualization):
            fig = visualization.visualize()
            fig.show()
        elif visualization is None:
            return
        else:
            raise TypeError('Unhandled type was returned.')

    def save(self) -> None:
        for name in get_args(self.options):
            instance = self.get(name)
            path = os.path.join(self.paths.images.value, f'{name}.png')

            if isinstance(instance, visualizations.MatplotLibVisualization):
                instance.visualize()
                plt.savefig(path)
            elif isinstance(instance, visualizations.PlotlyVisualization):
                fig = instance.visualize()
                fig.write_image(path)

    def get(self, name: options) -> visualizations.AbstractVisualization:
        clazz = self.mapping.get(name)

        if clazz is None:
            raise ModuleNotFoundError('Visualization cannot be found.')

        return clazz(self.manager.dataframe)
