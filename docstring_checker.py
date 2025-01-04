import ast
import sys
import re


IGNORE_MISSING_MODULE_DOCSTRINGS = True


def analyze_docstrings(file_path):
    """Analyzes the code if it has docstrings

    Args:
        file_path (str): File path

    Returns:
        List: List of results
    """
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    results = []

    # Check for module-level docstring
    if not ast.get_docstring(tree) and not IGNORE_MISSING_MODULE_DOCSTRINGS:
        results.append({
            "message": "Missing module docstring.",
            "line": 1  # Module docstrings should be at the start
        })

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if not docstring:
                results.append({
                    "message": f"Missing Function docstring: {node.name}",
                    "line": node.lineno
                })
            else:
                args = [arg.arg for arg in node.args.args if arg.arg not in (
                    "self", "cls")]
                missing_args = [arg for arg in args if not re.search(
                    rf"\b{arg}\b", docstring)]
                if missing_args:
                    results.append({
                        "message": f"Function {node.name} is missing documentation for arguments: {', '.join(missing_args)}",
                        "line": node.lineno
                    })

        elif isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                results.append({
                    "message": f"Missing Class docstring: {node.name}",
                    "line": node.lineno
                })

    return results


# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python check_docstrings.py <file_path>")
#         sys.exit(1)

#     file_path = sys.argv[1]
#     issues = analyze_docstrings(file_path)
#     if issues:
#         print(f"Issues in {file_path}:")
#         for issue in issues:
#             print(f" - Line {issue['line']}: {issue['message']}")
#         sys.exit(1)
#     else:
#         print(f"No issues in {file_path}.")
#         sys.exit(0)
