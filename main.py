from typing import Literal, Callable, cast
import sys

from presentation import Presentation
from data import DataManager


def present(type: Literal['matplotlib', 'plotly']):
    presentation = Presentation()

    try:
        visualization: Callable = (getattr(presentation, type))
    except AttributeError:
        print('Such a visualization doesn\'t exist.')

    visualization()


def setup():
    manager = DataManager()
    manager.setup()


def main():
    task = sys.argv[1] if len(sys.argv) > 1 else ''

    match task:
        case 'present':
            presentation = sys.argv[2] if len(sys.argv) > 2 else ''

            if presentation not in Presentation.options:
                print('Such a presentation doesn\'t exist.')
                return

            present(cast(Literal['matplotlib', 'plotly'], presentation))
        case 'setup':
            setup()
        case _:
            print('Such a command doesn\'t exist.')


if __name__ == '__main__':
    main()
