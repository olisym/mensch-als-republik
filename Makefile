PY := .venv/bin/python
RUFF := .venv/bin/ruff

.PHONY: test test-prop check-specs check-tree check-lint check check-all clean

test:
	find . -name __pycache__ -type d -not -path "./.venv/*" -exec rm -rf {} +
	$(PY) -m pytest -q

test-prop:
	MAR_HYPOTHESIS=voll $(PY) -m pytest -q tests/property

check-specs:
	$(PY) tools/check_specs.py

check-tree:
	$(PY) tools/check_tree.py

check-lint:
	$(RUFF) check mensch_als_republik tests tools

check: check-tree check-specs check-lint test

check-all: check-tree check-specs check-lint test test-prop

clean:
	find . -name __pycache__ -type d -not -path "./.venv/*" -exec rm -rf {} +
	rm -rf .pytest_cache mensch_als_republik.egg-info
