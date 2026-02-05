.PHONY: install dev start test clean help

help:
	@echo "GenInit - Available Commands:"
	@echo "  make install    - Install the package in development mode"
	@echo "  make dev        - Install with development dependencies"
	@echo "  make start      - Run GenInit (after installation)"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean build artifacts"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make install"
	@echo "  2. make start"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

start:
	geninit

test:
	pytest tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
