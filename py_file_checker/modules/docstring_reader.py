import ast
from typing import Union


class DocstringReader:
    """Class that reads the docstring via ast node
    """

    def __init__(self, ast_node: Union[ast.Module, ast.FunctionDef, ast.ClassDef]) -> None:
        """Class Initialization

        Args:
            ast_node (Union[ast.Module, ast.FunctionDef, ast.ClassDef]): ast node
        """
        self.__ast_node = ast_node

    def read(self) -> Union[str, None]:
        """Reads the ast node and returns the docstring if any.

        Returns:
            Union[str, None]: Docstring result
        """
        return ast.get_docstring(self.__ast_node)
