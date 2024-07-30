import abc
import pandas


class AbstractVisualization(abc.ABC):
    dataframe: pandas.DataFrame

    def __init__(self, dataframe: pandas.DataFrame) -> None:
        self.dataframe = self.clean(dataframe)

    @ abc.abstractmethod
    def visualize(self) -> None:
        ''' Please include visualization logic here. '''

    @ abc.abstractmethod
    def clean(self, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        ''' Please include data cleaning logic here. '''
