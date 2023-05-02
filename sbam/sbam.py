#!/usr/bin/env python3

from lexer import Lexer
from cli import Cli
from parser import Parser

if __name__ == '__main__':

    file = Cli.init()

    if not file:
        exit()

    l = Lexer(file)
    p = Parser(file, l.tokens, l.splitted_lines)
