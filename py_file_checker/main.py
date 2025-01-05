import ast
import fnmatch
from copy import copy
from typing import List, Tuple, Callable, Any, Dict
from .modules.file_reader import FileReader
from .modules.resource_configuration_reader import ResourceConfigurationReader


class PyFileChecker:
    """
    This class checks a specific Python file to determine if it satisfies certain validation criteria.
    """

    def __init__(self, filepath: str, rc_filepath: str = ".pfcrc") -> None:
        """
        Initializes the `PyFileChecker` with the given file path and RC file path.

        Args:
            filepath (str): The file path of the Python file to be checked.
            rc_filepath (str): The file path of the RC file to refer to for specific configurations. Defaults to ".pfcrc".
        """
        self.validating_functions: List[Tuple[str,
                                              Callable[[ast.AST], Any]]] = []
        self.__result: List[Tuple[str, Any]] = []
        self.__filepath: str = filepath
        self.__rc_filepath: str = rc_filepath

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

    def __read_rc(self) -> Dict[str, Any]:
        """
        Reads the resource configuration (RC) file and extracts configuration options.

        Returns:
            Dict[str, Any]: A dictionary containing RC configuration options such as include, exclude, settings, and base directory.
        """
        rcr = ResourceConfigurationReader(self.__rc_filepath)
        return {
            "include": rcr.get_config_options("INCLUDE"),
            "exclude": rcr.get_config_options("EXCLUDE"),
            "settings": rcr.get_config_options("SETTINGS"),
            "base_dir": rcr.get_value_from_section("SETTINGS", "base_directory", "./"),
        }

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

    def __validate_filepath_pattern(self, filepath: str, patterns: List[str]) -> bool:
        """
        Validates whether the file path matches any of the given patterns.

        Args:
            filepath (str): The file path to check.
            patterns (List[str]): A list of patterns to match the file path against.

        Returns:
            bool: True if the file path matches any pattern; otherwise, False.
        """
        for pattern in patterns:
            if fnmatch.fnmatch(filepath, pattern):
                return True
        return False

    def start(self) -> None:
        """
        Initiates the file validation process.

        Steps:
            1. Reads the content of the file.
            2. Reads the RC configuration to determine include/exclude rules.
            3. Validates the file path against the RC configuration rules.
            4. Parses the content into an AST module node.
            5. Validates the AST module node using registered validation functions.

        If the file is excluded based on RC rules, the validation process is skipped.
        """
        # 1. Read the file
        file_content = self.__read_file()

        # 2. Read the RC
        rc_config = self.__read_rc()

        # 3. Validate file path against RC rules
        is_included = not rc_config["include"] or self.__validate_filepath_pattern(
            self.__filepath, rc_config["include"]
        )
        is_excluded = self.__validate_filepath_pattern(
            self.__filepath, rc_config["exclude"]
        )

        if not is_included or is_excluded:
            print(
                f"{self.__filepath} has been skipped checking due to RC configuration"
            )
            return

        # 4. Parse it to AST
        module_node = self.__parse_ast(file_content)

        # 5. Handle the validation
        self.__result = self.__handle_validation(module_node)
