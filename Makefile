VENV_DIR = .venv
REQ_FILE = requirements.txt
PYTHON = /usr/bin/python3

all: setup install

setup: ## Set up the virtual environment
	$(PYTHON) -m venv $(VENV_DIR)

install: ## Install Python dependencies
	$(VENV_DIR)/bin/pip install -r $(REQ_FILE)

clean: ## Clean up by removing the virtual environment
	rm -rf $(VENV_DIR)

help: ## Display this help message
	@echo "Available options:"
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk ' \
		BEGIN {FS = ":.*?## "} \
		{printf "  %-20s %s\n", $$1, $$2}'

# Inform users how to activate the virtual environment in their shell
	@echo ""
	@echo "To activate the virtual environment, run:"
	@echo "  source $(VENV_DIR)/bin/activate"
