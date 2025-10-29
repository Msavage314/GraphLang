from AST import (
    ASTNode,
    Program,
    Namespace,
    IfStatement,
    BinaryOp,
    Number,
    Identifier,
    Assignment,
)
from state import DesmosState


class Interpreter:
    """Interprets AST and generates Desmos expressions"""

    def __init__(self):
        self.state = DesmosState()

    def format_identifier(self, name: str) -> str:
        """Format identifier for Desmos (subscript for multi-char names)"""
        if len(name) <= 1:
            return name
        # Convert 'result' to 'r_{esult}'

        return f"{name[0]}_{{{name[1:]}}}"

    def interpret(self, node: ASTNode):
        if isinstance(node, Program):
            self.interpret_program(node)
        elif isinstance(node, Namespace):
            self.interpret_namespace(node)
        elif isinstance(node, Assignment):
            return self.interpret_assignment(node)
        elif isinstance(node, IfStatement):
            return self.interpret_if(node)
        elif isinstance(node, BinaryOp):
            return self.interpret_binary_op(node)
        elif isinstance(node, Number):
            return str(node.value)
        elif isinstance(node, Identifier):
            return self.format_identifier(node.name)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def interpret_program(self, node: Program) -> str:
        """Process all statements in the program"""
        for stmt in node.statements:
            self.interpret(stmt)
        return ""

    def interpret_namespace(self, node: Namespace) -> str:
        """Create a folder for the namespace"""
        self.state.add_folder(node.name)
        for stmt in node.block:
            self.interpret(stmt)
        self.state.current_folder = None
        return ""

    def interpret_assignment(self, node: Assignment) -> str:
        """Convert assignment to Desmos latex"""
        target_latex = self.format_identifier(node.target)
        value_latex = self.interpret(node.value)
        latex = f"{target_latex}={value_latex}"

        kwargs = {}
        if self.state.current_folder:
            kwargs["folderId"] = self.state.current_folder

        self.state.add_expression(latex, **kwargs)
        return latex

    def interpret_if(self, node: IfStatement):
        """convert if to piecewise notation"""
        condition = self.interpret(node.condition)
        then_exprs = []
        for stmt in node.then_block:
            if isinstance(stmt, Assignment):
                value = self.interpret(stmt.value)
                then_exprs.append((stmt.target, value))
        else_exprs = []
        if node.else_block:
            for stmt in node.else_block:
                if isinstance(stmt, Assignment):
                    value = self.interpret(stmt.value)
                    else_exprs.append((stmt.target, value))
        all_vars = set(var for var, _ in then_exprs + else_exprs)
        for var in all_vars:
            then_val = next((val for v, val in then_exprs if v == var), None)
            else_val = next((val for v, val in else_exprs if v == var), None)
            var_latex = self.format_identifier(var)
            if then_val and else_val:
                latex = f"{var_latex}=\\left\\{{{condition}:{then_val},{else_val}\\right\\}}"
            elif then_val:
                latex = f"{var_latex}=\\left\\{{{condition}:{then_val}\\right\\}}"
            else:
                latex = (
                    f"{var_latex}=\\left\\{{\\neg({condition}):{else_val}\\right\\}}"
                )
            kwargs = {}
            if self.state.current_folder:
                kwargs["folderId"] = self.state.current_folder
            self.state.add_expression(latex, **kwargs)

        return ""

    def interpret_binary_op(self, node: BinaryOp) -> str:
        """Convert binary operation to latex"""
        left = self.interpret(node.left)
        right = self.interpret(node.right)

        op_map = {
            "+": "+",
            "-": "-",
            "*": "\\cdot",
            "/": "\\frac",
            ">": ">",
            "<": "<",
            ">=": "\\ge",
            "<=": "\\le",
        }

        op = op_map.get(node.op, node.op)

        if node.op == "/":
            return f"\\frac{{{left}}}{{{right}}}"

        return f"{left}{op}{right}"
