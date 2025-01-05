import ast
import re
from typing import List, Union, Dict


class DocstringValidator:
    """
    Validates the presence and completeness of docstrings in classes and functions within a Python module.

    This class uses the `ast` module to traverse the abstract syntax tree (AST) of the given Python module 
    and checks for missing docstrings and undocumented function arguments.
    """

    def __init__(self, ast_module: ast.Module) -> None:
        """
        Initializes the `DocstringValidator` with the given AST module.

        Args:
            ast_module (ast.Module): The AST representation of a Python module to validate.
        """
        self.__ast_module: ast.Module = ast_module

    def __handle_docstring_validation(self, ast_module_node: ast.Module) -> List[Dict[str, Union[str, int]]]:
        """
        Validates docstrings for classes and functions in the given AST module node.

        Args:
            ast_module_node (ast.Module): The AST module node to validate.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of dictionaries containing validation results with 
            error messages and line numbers.
        """
        results: List[Dict[str, Union[str, int]]] = []
        for node in ast.walk(ast_module_node):
            if isinstance(node, ast.FunctionDef):
                function_docstring_validation_result = self.__handle_function_docstring_validation(
                    node)
                if function_docstring_validation_result:
                    results.append(function_docstring_validation_result)
            elif isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    result_template = self.__parse_missing_class_docstring(
                        node)
                    results.append(result_template)
        return results

    def __parse_missing_class_docstring(self, node: ast.ClassDef) -> Dict[str, Union[str, int]]:
        """
        Generates a result template for a class missing a docstring.

        Args:
            node (ast.ClassDef): The AST node for the class.

        Returns:
            Dict[str, Union[str, int]]: A dictionary containing the error message and line number.
        """
        return {
            "message": f"Missing Class docstring: {node.name}",
            "line": node.lineno
        }

    def __handle_function_docstring_validation(self, node: ast.FunctionDef) -> Union[Dict[str, Union[str, int]], None]:
        """
        Validates the docstring of a function and checks for missing argument documentation.

        Args:
            node (ast.FunctionDef): The AST node for the function.

        Returns:
            Union[Dict[str, Union[str, int]], None]: A dictionary with validation errors or None if valid.
        """
        docstring = ast.get_docstring(node)
        if not docstring:
            return self.__parse_missing_function_docstring(node)
        else:
            args = [arg.arg for arg in node.args.args if arg.arg not in (
                "self", "cls")]
            missing_args = [arg for arg in args if not re.search(
                rf"\b{arg}\b", docstring)]
            if missing_args:
                return self.__parse_missing_function_argument_docstring(node, missing_args)
        return None

    def __parse_missing_function_argument_docstring(self, node: ast.FunctionDef, missing_args: List[str]) -> Dict[str, Union[str, int]]:
        """
        Generates a result template for a function missing argument documentation.

        Args:
            node (ast.FunctionDef): The AST node for the function.
            missing_args (List[str]): A list of argument names missing documentation in the function docstring.

        Returns:
            Dict[str, Union[str, int]]: A dictionary containing the error message and line number.
        """
        return {
            "message": f"Function {node.name} is missing documentation for arguments: {', '.join(missing_args)}",
            "line": node.lineno
        }

    def __parse_missing_function_docstring(self, node: ast.FunctionDef) -> Dict[str, Union[str, int]]:
        """
        Generates a result template for a function missing a docstring.

        Args:
            node (ast.FunctionDef): The AST node for the function.

        Returns:
            Dict[str, Union[str, int]]: A dictionary containing the error message and line number.
        """
        return {
            "message": f"Missing Function docstring: {node.name}",
            "line": node.lineno
        }

    def validate(self) -> List[Dict[str, Union[str, int]]]:
        """
        Validates the AST module for missing or incomplete docstrings.

        Returns:
            List[Dict[str, Union[str, int]]]: A list of dictionaries containing validation results with 
            error messages and line numbers.
        """
        return self.__handle_docstring_validation(self.__ast_module)
