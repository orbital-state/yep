from .base import BaseReflector
import ast


class CodeStructureVisitor(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        print(f'Function name: {node.name}')
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        print(f'Class name: {node.name}')
        self.generic_visit(node)



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
