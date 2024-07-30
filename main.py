from typing import Optional
import sys

from presentation import Presentation
from data import DataManager


def present():
    presentation = Presentation()
    presentation.visualize()


def setup():
    manager = DataManager()
    manager.setup()


if __name__ == '__main__':
    cmd: Optional[str] = sys.argv[1] if len(sys.argv) > 1 else None

    match cmd:
        case 'present':
            present()
        case 'setup':
            setup()
        case _:
            print('Such a command doesn\'t exist.')
