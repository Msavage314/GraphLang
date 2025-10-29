"""Recursive descent parser"""

from AST import (
    ASTNode,
    Assignment,
    BinaryOp,
    IfStatement,
    Namespace,
    Program,
    Number,
    Identifier,
)
from tokens import Token, TokenTypes
from lex import Lexer


class Parser:
    def __init__(self, tokens: list[Token]):
        self.position = 0
        self.tokens = tokens

    def peek(self, offset: int = 1) -> Token | None:
        idx = self.position + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def consume(self, expected_type: TokenTypes) -> Token:
        token = self.current
        if token is None or token.type != expected_type:
            raise SyntaxError(
                f"Expected {expected_type}, got {token.type if token else 'EOF'}"
            )
        self.position += 1
        return token

    def match(self, *types: TokenTypes) -> bool:
        token = self.current
        return token is not None and token.type in types

    def skip_lines(self):
        while self.match(TokenTypes.LINE):
            self.consume(TokenTypes.LINE)

    def parse(self) -> Program:
        statements = []
        while self.current is not None:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements)

    def parse_statement(self) -> ASTNode | None:
        self.skip_lines()
        if self.current is None:
            return None
        if self.match(TokenTypes.NAMESPACE):
            return self.parse_namespace()
        elif self.match(TokenTypes.IF):
            return self.parse_if()
        elif self.match(TokenTypes.IDENTIFIER):
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token: {self.current}")

    def parse_namespace(self) -> Namespace:
        self.consume(TokenTypes.NAMESPACE)
        name = self.consume(TokenTypes.IDENTIFIER).value
        block = []
        self.consume(TokenTypes.LBRACE)
        self.skip_lines()
        while not self.match(TokenTypes.RBRACE):
            block.append(self.parse_statement())
            self.skip_lines()
        self.consume(TokenTypes.RBRACE)
        return Namespace(name, block)

    def parse_if(self) -> IfStatement:
        self.consume(TokenTypes.IF)
        self.consume(TokenTypes.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenTypes.RPAREN)
        self.consume(TokenTypes.LBRACE)
        then_block = []
        while not self.match(TokenTypes.RBRACE):
            then_block.append(self.parse_statement())
        self.consume(TokenTypes.RBRACE)

        else_block = None
        if self.match(TokenTypes.ELSE):
            self.consume(TokenTypes.ELSE)
            self.consume(TokenTypes.LBRACE)
            else_block = []
            while not self.match(TokenTypes.RBRACE):
                else_block.append(self.parse_statement())
                self.skip_lines()
            self.consume(TokenTypes.RBRACE)
        return IfStatement(condition, then_block, else_block)

    def parse_assignment(self) -> Assignment:
        target = self.consume(TokenTypes.IDENTIFIER).value
        self.consume(TokenTypes.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenTypes.LINE)
        return Assignment(target=target, value=value)

    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()

    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        while self.match(
            TokenTypes.GREATER,
            TokenTypes.LESSEQUAL,
            TokenTypes.LESS,
            TokenTypes.GREATEREQUAL,
        ):
            if self.current is None:
                raise SyntaxError()
            op = self.current.value
            self.position += 1
            right = self.parse_additive()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        while self.match(TokenTypes.PLUS, TokenTypes.MINUS):
            if self.current is None:
                raise SyntaxError()
            op = self.current.value
            self.position += 1
            right = self.parse_multiplicative()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_primary()
        while self.match(TokenTypes.MULTIPLY, TokenTypes.DIVIDE):
            if self.current is None:
                raise SyntaxError()
            op = self.current.value
            self.position += 1
            right = self.parse_primary()
            left = BinaryOp(op=op, left=left, right=right)
        return left

    def parse_primary(self) -> ASTNode:
        if self.current is None:
            raise SyntaxError()
        if self.match(TokenTypes.INTEGER):
            value = int(self.current.value)
            self.position += 1
            return Number(value=value)
        elif self.match(TokenTypes.FLOAT):
            value = float(self.current.value)
            self.position += 1
            return Number(value=value)
        elif self.match(TokenTypes.IDENTIFIER):
            name = self.current.value
            self.position += 1
            return Identifier(name=name)
        elif self.match(TokenTypes.LPAREN):
            self.consume(TokenTypes.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenTypes.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current()}")

    @property
    def current(self) -> Token | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None
