install: 
	@echo "Installing..."
	poetry install
	poetry run pre-commit install

activate:
	@echo "Activating virtual environment"
	poetry shell

test:
	pytest --cov b3_api --cov-report term-missing --cov-report html
	open htmlcov/index.html

build:
	poetry run pytest
	poetry version patch
	poetry build

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist