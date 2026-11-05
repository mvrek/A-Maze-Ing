PYTHON  ?= python3
VENV    := .venv
PY      := $(VENV)/bin/python
INSTALLED := $(VENV)/.installed
MAIN    := a_maze_ing.py
CONFIG  := config.txt
 
.PHONY: install run debug clean fclean lint lint-strict test
 
$(PY):
	$(PYTHON) -m venv $(VENV)
 
$(INSTALLED): $(PY)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install flake8 mypy pytest build
	touch $(INSTALLED)
 
install: $(INSTALLED)
 
run: $(PY)
	$(PY) $(MAIN) $(CONFIG)
 
debug: $(PY)
	$(PY) -m pdb $(MAIN) $(CONFIG)
 
clean:
	find . -type d -name __pycache__ -not -path "./$(VENV)/*" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info
 
fclean: clean
	rm -rf $(VENV)
 
lint: $(INSTALLED)
	$(PY) -m flake8 .
	$(PY) -m mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
 
lint-strict: $(INSTALLED)
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict
 
test: $(INSTALLED)
	$(PY) -m pytest