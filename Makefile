PY ?= venv/bin/python

test:
	$(PY) test.py

run-all:
	$(PY) down.py --yes && $(PY) up.py && $(PY) seed.py && $(PY) triggers.py && echo "Success ✅"

query:
	$(PY) query.py

export:
	$(PY) query.py --export && $(PY) print_tables.py --export
