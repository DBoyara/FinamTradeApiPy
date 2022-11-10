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
