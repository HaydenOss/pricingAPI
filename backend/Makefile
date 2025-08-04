# === Configurable Variables ===
BASE = poetry run
LINT = ruff
FORMAT = black
SORT = isort
RUNSERVER = uvicorn app.main:app --reload

# === Commands ===

.PHONY: help lint format sort check run

help:
	@echo "make lint      - Run Ruff to lint code"
	@echo "make format    - Format code with Black"
	@echo "make sort      - Sort imports with isort"
	@echo "make check     - Run Ruff, Black, and isort in check mode"
	@echo "make run       - Run FastAPI app with Uvicorn"

lint:
	$(BASE) $(LINT) check .
lint-fix:
	$(BASE) $(LINT) check . --fix
format:
	$(BASE) $(FORMAT) .

sort:
	$(BASE) $(SORT) .

check:
	$(BASE) $(LINT) $(SRC) --check
	$(BASE) $(FORMAT) $(SRC) --check
	$(BASE) $(SORT) $(SRC) --check-only

run:
	$(BASE) $(RUNSERVER)