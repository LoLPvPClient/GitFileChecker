import sys
from .main import PyFileChecker
from .modules.docstring_validator import DocstringValidator

FUNCTIONS = [("Docstrings", lambda node: DocstringValidator(node).validate())]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_docstrings.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    file_checker = PyFileChecker(filepath=file_path)
    file_checker.validating_functions = FUNCTIONS
    file_checker.start()

    issues = file_checker.result  # Issue result content
    has_issues = bool([issue_content for _,
                      issue_content in issues if issue_content])  # Will return true or false depending on result of issue

    if has_issues:
        print(f"Validation failed occured in {file_path}:")
        for issue_type, issue in issues:
            print(f"{issue_type}: ")
            for issue_content in issue:
                print(
                    f" - {issue_content['message']} ({file_path}:{issue_content['line']})")
        print()
        sys.exit(1)
    else:
        print(f"No issues in {file_path}.")
        print()
        sys.exit(0)
