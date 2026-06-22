.PHONY: test lint install

install:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

lint:
	python -m flake8 src/ tests/
