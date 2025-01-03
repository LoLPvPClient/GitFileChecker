# Makefile Template for py-filechecker-patch

# Variables
PYTHON := python3       # Specify the Python interpreter
PATCH_SCRIPT := patch_filechecker.py  # Name of the patch script
TARGET := py-filechecker-patch  # The make target name
LOG_FILE := patch_log.txt  # Log file for patch output
PATCH_ARGS :=              # Add any arguments needed for the patch script


.PHONY: deploy-pre-commit-script

deploy-pre-commit-script:
	@echo Deploying pre-commit script...
	cp pre-commit.sh ./.git/hooks/pre-commit
	@echo Making the pre-commit executable
	sudo chmod +x ./.git/hooks/pre-commit
	@echo Done!

# # Default target
# .PHONY: all
# all: $(TARGET)

# # Target: Run the patch script
# .PHONY: $(TARGET)
# $(TARGET):
# 	@echo "Running patch script for py-filechecker..."
# 	@$(PYTHON) $(PATCH_SCRIPT) $(PATCH_ARGS) > $(LOG_FILE) 2>&1 || \
# 		(echo "Patch failed. Check $(LOG_FILE) for details."; exit 1)
# 	@echo "Patch applied successfully. Logs saved in $(LOG_FILE)."

# # Clean up log file
# .PHONY: clean
# clean:
# 	@echo "Cleaning up log file..."
# 	@rm -f $(LOG_FILE)
# 	@echo "Done."
