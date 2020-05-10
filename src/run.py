

import argparse
import importlib
import inspect
import textwrap


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapter', type=int, required=True)
    parser.add_argument('--practice', type=int, required=True)
    arguments = parser.parse_args()

    chapter_name = 'chapter{}'.format(arguments.chapter)
    practice_name = 'practice{:0=2}'.format(arguments.practice)
    return [chapter_name, practice_name]


def import_chapter_module(chapter_name):
    return importlib.import_module(chapter_name)


def get_practice_function(chapter_module, practice_name):
    functions = inspect.getmembers(chapter_module, inspect.isfunction)
    return dict(functions)[practice_name]


def print_docstring(target):
    docstring = textwrap.dedent(target.__doc__)

    for line in docstring.splitlines():
        print('# ' + line)
    else:
        print('# ')


def main():
    chapter_name, practice_name = get_arguments()
    chapter_module = import_chapter_module(chapter_name)
    practice_function = get_practice_function(chapter_module, practice_name)
    print_docstring(practice_function)
    practice_function()


if __name__ == '__main__':
    main()

