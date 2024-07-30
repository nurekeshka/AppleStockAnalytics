from typing import Tuple, Literal, Dict, Type
from settings import Path, Columns
from data import DataManager

import visualizations


class Presentation():
    paths = Path
    columns = Columns

    options = Literal[
        'prices', 'candles',
        'describe', 'averages',
        'daily_returns', 'cumulative_returns',
        'volume', 'bollinger', 'rsi']

    mapping: Dict[str, Type[visualizations.AbstractVisualization]] = {
        'prices': visualizations.PriceFigureVisualization,
        'candles': visualizations.PriceCandleVisualization,
        'describe': visualizations.DescribeVisualization,
        'averages': visualizations.MovingAveragesVisualization,
        'daily_returns': visualizations.DailyReturnsVisualization,
        'cumulative_returns': visualizations.CumulativeReturnVisualization,
        'volume': visualizations.VolumeAnalysisVisualization,
        'bollinger': visualizations.BollingerBandsVisualization,
        'rsi': visualizations.RelativeStrengthIndexVisualization}

    manager: DataManager

    title: str = 'Apple Stock Close Price'
    context: str = 'Close Price'
    xlabel: str = 'Date'
    ylabel: str = 'Close Price (USD)'
    size: Tuple[int, int] = (10, 6)

    def __init__(self) -> None:
        self.manager = DataManager()

    def visualize(self, name: options) -> None:
        clazz = self.mapping.get(name)

        if clazz is None:
            raise ModuleNotFoundError('Visualization cannot be found.')

        visualization = clazz(self.manager.dataframe)
        visualization.visualize()
