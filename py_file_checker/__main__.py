import sys
from docstring_checker import analyze_docstrings

FUNCTIONS = [("Docstrings", analyze_docstrings)]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_docstrings.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    issues = []
    for func_title, func in FUNCTIONS:
        result = func(file_path)
        if result:
            issues.append((func_title, result))

    if issues:
        print(f"Issues in {file_path}:")
        for issue in issues:
            print(f" - {issue}")
        sys.exit(1)
    else:
        print(f"No issues in {file_path}.")
        sys.exit(0)
