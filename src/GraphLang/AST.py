"""
Contains AST classes for the language.

If you don't know how this works, basically each node has
a reference to other nodes that create it. It makes the
stream of tokens from the lexer into a cohesive structure
E.g. a Program consists of statements

"""

from dataclasses import dataclass


@dataclass
class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: list[ASTNode]


@dataclass
class Namespace(ASTNode):
    name: str
    block: list[ASTNode]


@dataclass
class ClassDef(ASTNode):
    name: str
    body: list[ASTNode]


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: list[ASTNode]
    else_block: list[ASTNode] | None = None


@dataclass
class Assignment(ASTNode):
    target: str
    value: ASTNode


@dataclass
class BinaryOp(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class Number(ASTNode):
    value: int | float
