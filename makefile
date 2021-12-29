install:
	poetry install
	
page-loader:
	poetry run page-loader -h

fake:
	poetry run page-loader https://www.jetbrains.com/ru-ru/pycharm/whatsnew/ --output tests/temp

hexlet:
	poetry run page-loader -o tests/temp https://page-loader.hexlet.repl.co/
tests:
	poetry run pytest -vv
 
coverage:
	poetry run pytest --cov=page_loader

build:
	poetry build
package-install:
	python3 -m pip install --user dist/*.whl
package-uninstall:
	python3 -m pip uninstall hexlet-code
lint:
	poetry run flake8 page_loader

command_prompt:
	export PS1="\W ($(git branch 2>/dev/null | grep '^*' | colrm 1 2)) $ "
.PHONY: install page-loader build package-install tests coverage venv
