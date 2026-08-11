PY := .venv/bin/python

.PHONY: test clean

test:
	find . -name __pycache__ -type d -exec rm -rf {} +
	$(PY) -m pytest -q

clean:
	find . -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .pytest_cache mensch_als_republik.egg-info
