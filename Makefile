PROGRAM_NAME = finam-trade-api

.PHONY: help clean dep dep-test sort mypy flake8

.DEFAULT_GOAL := help

help: ## Display this help screen.
	@echo "Makefile available targets:"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  * \033[36m%-15s\033[0m %s\n", $$1, $$2}'

dep:
	pip install -r requirements.txt

dep-test:
	pip install -r requirements-test.txt

sort:
	isort finam_trade_api

mypy:
	mypy finam_trade_api

flake8:
	flake8 finam_trade_api
