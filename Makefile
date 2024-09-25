.PHONY: test build

dev:
	cd ./src && python -m presentation.cli

build:
	make NAME=bkmks no-name-build

no-name-build:
	pyinstaller --onefile -n $(NAME) --path src --paths .venv/lib/python3.12/site-packages src/presentation/cli/__main__.py 

run:
	./dist/bkmks

test:
	pytest
	
venv:
	python -m venv .venv

env:
	source .venv/bin/activate

install:
	pip install -r requirements.txt

req:
	pip freeze > requirements.txt

lint:
	ruff check

fmt:
	ruff format src