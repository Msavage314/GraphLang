import pyperclip
import json
import sys
from rich import print
from lex import Lexer
from parse import Parser
from interpret import Interpreter
from state import DesmosState
from sys import exit

try:
    print(f"[bold cyan]Looking for file {sys.argv[1]}[/]\n")
except IndexError:
    print("[bold red]Please pass in your file as an argument - quitting[/]")
    exit()


print("[bold green]File Found![/]\n")
try:
    file = open(sys.argv[1])
except FileNotFoundError:
    print("[bold red]file not found- quitting[/]")
    exit()

with file as f:
    code = file.read()

    lexer = Lexer(code)
    tokens = lexer.lex()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)

    # Generate JSON
    desmos_json = interpreter.state.to_json()
    pyperclip.copy(json.dumps(desmos_json, indent=2))

    print("[bold green]Desmos json copied to clipboard![/]")
    input("Press any key to exit...")
