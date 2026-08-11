PY := .venv/bin/python

.PHONY: test check-specs check clean

test:
	find . -name __pycache__ -type d -exec rm -rf {} +
	$(PY) -m pytest -q

check-specs:
	$(PY) tools/check_specs.py

check: check-specs test

clean:
	find . -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .pytest_cache mensch_als_republik.egg-info
