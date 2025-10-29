from enum import Enum


class TokenTypes(Enum):
    FLOAT = "float"
    INTEGER = "integer"
    # operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    ASSIGN = "="
    GREATER = ">"
    LESS = "<"
    GREATEREQUAL = ">="
    LESSEQUAL = "<="
    DOT = "."
    POW = "^"

    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    SEMICOLON = ";"
    COLON = ":"
    COMMA = ","

    NAMESPACE = "namespace"
    CLASS = "class"
    MACRO = "macro"
    IF = "if"
    ELSE = "else"
    FN = "fn"

    IDENTIFIER = "identifier"
    EOF = "EOF"

    LINE = "LINE"


class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value: str = value
        self.line = line
        self.col = col

    def __str__(self):
        return f"{self.type} token '{self.value.replace('\n', '\\n')}' at position {self.line},{self.col}"


TOKEN_PATTERNS = {
    "FLOAT": r"\d+\.\d+",
    "INTEGER": r"\d+",
    # Multi-character operators (must come before single-character versions)
    "GREATEREQUAL": r">=",
    "LESSEQUAL": r"<=",
    # Keywords (must come before IDENTIFIER)
    "NAMESPACE": r"namespace",
    "CLASS": r"class",
    "MACRO": r"macro",
    "IF": r"if",
    "ELSE": r"else",
    "FN": r"fn",
    # Single-character operators
    "PLUS": r"\+",
    "MINUS": r"-",
    "MULTIPLY": r"\*",
    "DIVIDE": r"/",
    "ASSIGN": r"=",
    "GREATER": r">",
    "LESS": r"<",
    "DOT": r"\.",
    "POW": r"\^",
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "LBRACE": r"\{",
    "RBRACE": r"\}",
    "LBRACKET": r"\[",
    "RBRACKET": r"\]",
    "SEMICOLON": r";",
    "COLON": r":",
    "COMMA": r",",
    "LINE": r"\n",
    "WHITESPACE": r"[ \t\r]+",
    # Identifier (must come after keywords)
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
}
