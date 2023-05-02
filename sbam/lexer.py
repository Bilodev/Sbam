from io import TextIOWrapper
from utils.tkn import Token


class Lexer:
    def __init__(self, source: TextIOWrapper) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.special_symbols = ('!', '.', '-', '_')
        self.splitted_lines: list[list[str]] = []
        self.lex_file()

    def lex_line(self, row: int, line: str):

        if line.strip().startswith('--'):
            return

        current_token = ''
        opened_apices = False

        for c in line:

            # handle di fine linea apice non chiuso

            if c == '\n' and opened_apices:
                self.tokens.append(
                    Token(self.source.name, row, current_token))
                current_token = ""
                opened_apices = False
                continue

            if c == "'":
                if not opened_apices:
                    opened_apices = True
                    current_token = "'"

                elif opened_apices:
                    opened_apices = False
                    self.tokens.append(
                        Token(self.source.name, row, current_token + "'"))
                    current_token = ""
                continue

            if opened_apices:
                current_token += c
                continue

            if c in (' ', '', '\t', '\n'):
                if current_token:
                    self.tokens.append(
                        Token(self.source.name, row, current_token))
                    current_token = ''
                continue

            elif c not in self.special_symbols and not c.isalnum():

                if current_token:
                    self.tokens.append(
                        Token(self.source.name, row,
                              current_token))
                    current_token = ''

                self.tokens.append(Token(self.source.name, row, c))

                continue
            else:
                current_token += c

    def lex_file(self):

        for row, line in enumerate(self.source.readlines()):
            self.lex_line(row, line)

            self.splitted_lines.append([])

            for t in self.tokens:
                if t.line == row:
                    self.splitted_lines[row].append(t.token)
        self.source.close()
