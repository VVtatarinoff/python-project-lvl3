import os
import pytest
import tempfile
from tests.fixtures.test_data import HTML_LOAD_PATHS
from tests.fixtures.test_data import PNG_LOAD_PATHS
from tests.fixtures.test_data import CSS_LOAD_PATHS
from tests.fixtures.naming_data import NAMES


def get_fixture_path(file_name):
    current = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current, 'fixtures', file_name)


def get_data(path, mode="r"):
    path = get_fixture_path(path)
    with open(path, mode) as file:
        data = file.read()
    return data


class FakeRequestData(object):
    def __init__(self, data_paths):
        for name, value in data_paths.items():
            setattr(self, name, value)
        self.file_content = get_data(self.file_content, self.read_mode)
        self.initial_html = get_data(self.initial_html)
        self.modified_html = get_data(self.modified_html)

    @property
    def mock_page_data(self):
        return {'headers': {'content-type':
                            'text/html; charset=utf-8',
                            'content-length': '100'},
                'text': self.initial_html}

    @property
    def mock_domain_data(self):
        if self.read_mode == 'r':
            attr = 'text'
        else:
            attr = 'content'
        return {'headers': {'content-type': self.file_type,
                            'content-length': '100'},
                attr: self.file_content}


@pytest.fixture(scope="session", params=(HTML_LOAD_PATHS,
                                         PNG_LOAD_PATHS,
                                         CSS_LOAD_PATHS))
def fake_urls(request):
    return FakeRequestData(request.param)


@pytest.fixture()
def temp_directory():
    return tempfile.TemporaryDirectory()


@pytest.fixture(scope="session", params=NAMES)
def name_matching(request):
    return request.param
