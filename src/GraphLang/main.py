import pyperclip
import json
from lex import Lexer
from parse import Parser
from interpret import Interpreter
from state import DesmosState

code = """
namespace MyApp {
    x = 5
    y = 10
    
    if (x >= 10) {
        result = x + 3.14
    } else {
        result = 42 - y
    }
}
"""

lexer = Lexer(code)
tokens = lexer.lex()
parser = Parser(tokens)
ast = parser.parse()

interpreter = Interpreter()
interpreter.interpret(ast)

# Generate JSON
desmos_json = interpreter.state.to_json()
pyperclip.copy(json.dumps(desmos_json, indent=2))
print(json.dumps(desmos_json, indent=2))
