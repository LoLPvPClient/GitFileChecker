import ast
from copy import copy
from typing import List, Tuple, Callable, Any
from .modules.file_reader import FileReader


class PyFileChecker:
    """
    This class checks a specific Python file to determine if it satisfies certain validation criteria.
    """

    def __init__(self, filepath: str) -> None:
        """
        Initializes the `PyFileChecker` with the given file path.

        Args:
            filepath (str): The file path of the Python file to be checked.
        """
        self.validating_functions: List[Tuple[str,
                                              Callable[[ast.AST], Any]]] = []
        self.__result: List[Tuple[str, Any]] = []
        self.__filepath: str = filepath

    @property
    def result(self) -> List[Tuple[str, Any]]:
        """
        Retrieves the results of the validation.

        Returns:
            List[Tuple[str, Any]]: A list of tuples containing function descriptions and their validation results.
        """
        return copy(self.__result)

    def __read_file(self) -> str:
        """
        Reads the content of the Python file.

        Returns:
            str: The content of the file as a string.
        """
        return FileReader(self.__filepath).read()

    def __read_rc(self) -> str:
        """
        Placeholder for reading RC (resource configuration) content.

        Raises:
            NotImplementedError: If the method is called, as RC handling is not yet implemented.
        """
        raise NotImplementedError("RC is not yet implemented")

    def __handle_validation(self, ast_module_node: ast.AST) -> List[Tuple[str, Any]]:
        """
        Performs validation on the given AST module node using the registered validation functions.

        Args:
            ast_module_node (ast.AST): The root node of the AST to validate.

        Returns:
            List[Tuple[str, Any]]: A list of tuples containing function descriptions and their validation results.
        """
        result: List[Tuple[str, Any]] = []
        for function_description, validating_function in self.validating_functions:
            result.append(
                (function_description, validating_function(ast_module_node)))
        return result

    def __parse_ast(self, str_content: str) -> ast.AST:
        """
        Parses the given string content into an AST module node.

        Args:
            str_content (str): The Python source code as a string.

        Returns:
            ast.AST: The parsed abstract syntax tree (AST) of the source code.
        """
        return ast.parse(str_content)

    def start(self) -> None:
        """
        Initiates the file validation process.

        Steps:
            1. Reads the content of the file.
            2. Reads the RC (currently not implemented).
            3. Parses the content into an AST module node.
            4. Validates the AST module node using registered validation functions.
        """
        # 1. Read the file
        file_content = self.__read_file()

        # 2. Read the RC (currently skipped)
        # 3. Parse it to AST
        module_node = self.__parse_ast(file_content)

        # 4. Handle the validation
        self.__result = self.__handle_validation(module_node)
