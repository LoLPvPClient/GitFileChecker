import ast
import re


def analyze_docstrings(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    results = []

    # Check for module-level docstring
    if not ast.get_docstring(tree):
        results.append("Missing module docstring.")

    for node in ast.walk(tree):
        # Check for function docstrings
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if not docstring:
                results.append(f"Missing Function docstring: {node.name}")
            else:
                # Extract argument names
                args = [arg.arg for arg in node.args.args if arg.arg not in (
                    "self", "cls")]
                missing_args = []
                for arg in args:
                    # Check if the argument is mentioned in the docstring
                    if not re.search(rf"\b{arg}\b", docstring):
                        missing_args.append(arg)
                if missing_args:
                    results.append(
                        f"Function {node.name} is missing documentation for arguments: {', '.join(missing_args)}")

        # Check for class docstrings
        elif isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                results.append(f"Missing Class docstring: {node.name}")

    return results


# Example usage
if __name__ == "__main__":
    file_path = "a.py"  # Replace with the path to your Python file
    issues = analyze_docstrings(file_path)
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("All docstrings are present and complete.")
