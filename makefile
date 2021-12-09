nstall:
	poetry install
page-loader:
	poetry run page_loader -h

tests:
	poetry run coverage run -m pytest -vv

coverage:
	poetry run coverage report

build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
package-uninstall:
	python3 -m pip uninstall hexlet-code
lint:
	poetry run flake8 page_loader
.PHONY: install gendiff build publish package-install tests coverage gentest1 gentest2 gentest3