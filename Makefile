.EXPORT_ALL_VARIABLES: ; 
.PHONY: all
.DEFAULT_GOAL: help

UV = uv
UVR = @$(UV) run --extra "dev"
RUFF = $(UVR) ruff
PYTEST = $(UVR) pytest

help:
	@echo '================================================='
	@echo '~~ List of available commands for this project ~~'
	@echo '================================================='
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
	 
all: format lint test ## Lint, test and build package

test: ## Test package
	$(PYTEST) -x -vv \
		--junitxml=.test_results/test-results.xml \
		--cov=src \
		--cov-report=xml:.test_results/coverage.xml \
		--cov-report=term

build: ## Build package
	@$(UV) build 

start: ## Run package
	@$(UV) pip install -e .
	@$(UVR) nbcat

deploy: build ## Publish package
	$(UV) publish --token $(token)

lint: ## Run linter over code base and auto resole minor issues
	$(RUFF) check

format: ## Format the source code according to defined coding style
	$(RUFF) check --fix-only
	$(RUFF) format

clean: ## Remove all file artifacts
	@rm -rf .venv/ dist/ build/ *.egg-info .pytest_cache/ .coverage coverage.xml
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -name '*~' -delete
