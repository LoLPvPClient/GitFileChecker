#!/bin/bash

# Path to the Python script
SCRIPT="check_docstrings.py"

# Check Python files staged for commit
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$FILES" ]; then
    echo "No Python files to check."
    exit 0
fi

# Run the Python script for each staged file
ERRORS=0
for FILE in $FILES; do
    echo "Checking $FILE for docstring issues..."
    python3 $SCRIPT "$FILE"
    if [ $? -ne 0 ]; then
        ERRORS=1
    fi
done

if [ $ERRORS -ne 0 ]; then
    echo "Docstring issues found. Commit aborted."
    exit 1
fi

echo "All checks passed."
exit 0
