VENV := venv

develop:
	python3 -m venv $(VENV); \
    source  ./$(VENV)/bin/activate; \
    pip install -r requirement.txt ; \

test:
	source  ./$(VENV)/bin/activate; \
