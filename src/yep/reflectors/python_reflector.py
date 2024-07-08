from .base import BaseReflector
import ast


class CodeStructureVisitor(ast.NodeVisitor):

    def __init__(self):
        self.current_depth = 0

    def generic_visit(self, node):
        # print(f'{"    " * self.current_depth}Node: {type(node).__name__} at depth {self.current_depth}')
        self.current_depth += 1
        super().generic_visit(node)
        self.current_depth -= 1

    def visit_FunctionDef(self, node):
        args = [arg.arg for arg in node.args.args]
        print(f'{"    " * self.current_depth}Function name: {node.name} with args: {args} at depth {self.current_depth}')
        self.current_depth += 1
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_ClassDef(self, node):
        print(f'{"    " * self.current_depth}Class name: {node.name} at depth {self.current_depth}')
        self.current_depth += 1
        self.generic_visit(node)
        self.current_depth -= 1


class PythonReflector(BaseReflector):
    """Python reflector implementation."""

    def parse(self):
        """Parse python source code in pipeline_path."""
        with open(self.yep_pipeline.file_path, 'r') as file:
            source_code = file.read()
        return ast.parse(source_code, filename=self.yep_pipeline.file_path)

    def analyze(self):
        """Analyze the parsed python source code to deduce its main structure."""
        parsed_tree = self.parse()
        visitor = CodeStructureVisitor()
        visitor.visit(parsed_tree)
