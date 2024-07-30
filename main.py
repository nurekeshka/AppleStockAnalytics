from typing import cast, get_args
import sys

from presentation import Presentation
from data import DataManager


def present(type: Presentation.options):
    presentation = Presentation()
    presentation.visualize(type)


def setup():
    manager = DataManager()
    manager.setup()


def main():
    task = sys.argv[1] if len(sys.argv) > 1 else ''

    match task:
        case 'present':
            presentation = sys.argv[2] if len(sys.argv) > 2 else ''

            if presentation not in get_args(Presentation.options):
                print('Such a presentation doesn\'t exist.')
                return

            present(cast(Presentation.options, presentation))
        case 'setup':
            setup()
        case _:
            print('Such a command doesn\'t exist.')


if __name__ == '__main__':
    main()
