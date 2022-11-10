PROGRAM_NAME = finam-trade-api

.PHONY: help clean dep test build build-docker

.DEFAULT_GOAL := help

help: ## Display this help screen.
	@echo "Makefile available targets:"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  * \033[36m%-15s\033[0m %s\n", $$1, $$2}'

dep:
	pip install -r requirements.txt

dep-test:
	pip install -r requirements-test.txt

sort:
	isort finam

mypy:
	mypy finam

flake8:
	flake8 finam
