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

clean-venv:
	@if [ -d .venv ]; then \
		rm -rf .venv; \
	fi

format:
	.venv/bin/black .
	.venv/bin/ruff check . --fix

lint: .venv
	.venv/bin/ruff check .

test: .venv
	.venv/bin/pytest tests/

coverage: .venv
	.venv/bin/pytest --cov=christopher tests/

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache

docker-build:
	docker build -t christopher .

docker-run:
	docker compose up --build

precommit-install: .venv
	.venv/bin/pre-commit install

