PY := .venv/bin/python

.PHONY: test test-prop check-specs check-tree check check-all clean

test:
	find . -name __pycache__ -type d -exec rm -rf {} +
	$(PY) -m pytest -q

test-prop:
	MAR_HYPOTHESIS=voll $(PY) -m pytest -q tests/property

check-specs:
	$(PY) tools/check_specs.py

check-tree:
	$(PY) tools/check_tree.py

check: check-tree check-specs test

check-all: check-tree check-specs test test-prop

clean:
	find . -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .pytest_cache mensch_als_republik.egg-info
