# Makefile

# Variables
VENV_DIR := venv
DAGSTER_ENV := dagster/.env
DAGSTER_ENV_EXAMPLE := .env.example
SLING_ENV := infra/.sling/env.yaml
SLING_ENV_EXAMPLE := infra/.sling/env.example.yaml
REQUIREMENTS_FILE := ./requirements/dagster-requirements.txt

.PHONY: lakehouse-setup lakehouse-init lakehouse-serve lakehouse-kill

# Command for setting up the environment
lakehouse-setup:
	@echo "Checking for virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "No virtual environment found, creating one..."; \
		python -m venv $(VENV_DIR); \
		echo "Activating virtual environment..."; \
		source $(VENV_DIR)/bin/activate && \
		echo "Installing requirements..." && \
		pip install -r $(REQUIREMENTS_FILE); \
	elif [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Virtual environment is not activated. Activating..."; \
		source $(VENV_DIR)/bin/activate; \
	else \
		echo "Virtual environment is already activated."; \
	fi

	@echo "Checking .env file in dagster..."
	@if [ ! -f "$(DAGSTER_ENV)" ]; then \
		echo "No .env file found, copying from .env.example..."; \
		cp $(DAGSTER_ENV_EXAMPLE) $(DAGSTER_ENV); \
	fi

	@echo "Checking env.yaml for infra sling..."
	@if [ ! -f "$(SLING_ENV)" ]; then \
		echo "No env.yaml file found, copying from env.example.yaml..."; \
		cp $(SLING_ENV_EXAMPLE) $(SLING_ENV); \
	fi
	@echo "setup complete, ensure environment variables are correctly configured..."

# Command for initializing the lakehouse setup
lakehouse-init: lakehouse-setup
	@echo "Starting Docker containers..."
	@docker-compose up -d

# Command for starting the Dagster development server
lakehouse-serve:
	@echo "Starting Dagster server..."
	@. $(VENV_DIR)/bin/activate && cd ./dagster && dagster dev

# Command for stopping Docker containers
lakehouse-kill:
	@echo "Stopping Docker containers..."
	@docker-compose down
