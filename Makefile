SHELL := /bin/bash
PY := poetry run python
PYTEST := ${PY} -m pytest
MYPY := ${PY} -m mypy

.PHONY: test/code
test/code:
	@ ${MYPY} --strict src/

.PHONY: test
test: test/code
	@ ${PYTEST} test/
