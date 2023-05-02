from io import TextIOWrapper
import sys
from os.path import splitext


class Cli:

    @staticmethod
    def help():
        print('Sbam!')
        print('[sbam/sbam.py]                       Get Version')
        print('[sbam/sbam.py build filename.sbam]   Compile the file and get the cpp')

    @staticmethod
    def init() -> TextIOWrapper | None:
        commands = ('help', 'build')

        try:
            command = sys.argv[1]

        except BaseException:
            print('Sbam! 1.0')
            exit()

        if command not in commands:
            print(f'Error: {command}, Command not valid')
            exit()

        elif command == 'help':
            Cli.help()

        elif command == 'build':
            file = sys.argv[2]

            f = open(file, 'r+')

            _, extension = splitext(f.name)

            if extension != '.sbam':
                print(f'Error: "{extension}" does not match ".sbam"')
                exit()

            return f
