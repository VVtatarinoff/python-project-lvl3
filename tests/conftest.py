import os

import pytest
import tempfile
# import requests_mock


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_fixture_path(file_name):
    return os.path.join(CURRENT_DIR, 'fixtures', file_name)


@pytest.fixture(scope="function")
def create_temp_dir():
    temp_dir = tempfile.TemporaryDirectory(dir=CURRENT_DIR)
    return temp_dir.name


@pytest.fixture(scope="session")
def get_html():
    file_html = "html/docs-python-org-3-library-venv-html-venv-def.html"
    with open(get_fixture_path(file_html)) as file:
        html_text = file.read()
    return html_text
