.PHONY: test

run:
	cd ./src && python -m presentation.cli

test:
	pytest
	
venv:
	python -m venv env