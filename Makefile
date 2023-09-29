SHELL := /bin/bash
PY := poetry run python
PYTEST := ${PY} -m pytest

.PHONY: test
test:
	@ ${PYTEST} test/
