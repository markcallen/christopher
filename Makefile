.PHONY: install develop clean-venv format lint test coverage clean docker-build docker-run precommit-install

PYTHON = .venv/bin/python
PIP = .venv/bin/pip

# Create virtual environment if not exists
.venv:
	@if [ ! -d .venv ]; then \
		python3 -m venv .venv; \
		$(PIP) install --upgrade pip; \
	fi

install: .venv
	$(PIP) install -r requirements.txt
	$(PIP) install -r dev-requirements.txt

develop: install
	$(PIP) install -e .

clean-venv:
	@if [ -d .venv ]; then \
		rm -rf .venv; \
	fi

format:
	.venv/bin/black .
	.venv/bin/ruff check . --fix

lint:
	.venv/bin/ruff check .

test:
	.venv/bin/pytest $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

coverage:
	.venv/bin/pytest --cov-report xml:coverage.xml

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache

docker-build:
	docker build -t christopher .

docker-run:
	docker compose up --build

precommit-install:
	.venv/bin/pre-commit install

