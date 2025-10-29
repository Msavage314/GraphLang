"""File for lexing an input"""

from typing import Generator
from tokens import TokenTypes, Token, TOKEN_PATTERNS
import re
import copy


class Lexer(object):
    """Class for a standard graphlang lexer"""

    def __init__(self, code: str) -> None:
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1

        pattern_parts = []
        for name, pattern in TOKEN_PATTERNS.items():
            pattern_parts.append(f"(?P<{name}>{pattern})")

        self.pattern = re.compile("|".join(pattern_parts))

    def lex(self) -> list:
        tokens = []
        while self.position < len(self.code):
            match = self.pattern.match(self.code, self.position)
            if match is None:
                raise SyntaxError(
                    f"Invalid character {self.code[self.position]} at line {self.line}, column {self.column}"
                )

            token_type = match.lastgroup
            token_value = match.group()

            if token_type != "WHITESPACE":
                tokens.append(
                    Token(TokenTypes[token_type], token_value, self.line, self.column)
                )
            self.position = match.end()
            if token_type == "LINE":
                self.line += 1
                self.column = 1
            else:
                self.column += len(token_value)
        return tokens
