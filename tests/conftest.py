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

    def mock_adresses(self, func):
        def inner():
            func(self.url, headers={'content-type': 'text/html; charset=utf-8',
                                    'content-length': '100'},
                 text=self.initial_html)
            if self.read_mode == 'r':
                func(self.url_file, headers={'content-type': self.file_type,
                                             'content-length': '100'},
                     text=self.file_content)
            else:
                func(self.url_file, headers={'content-type': self.file_type,
                                             'content-length': '100'},
                     content=self.file_content)
        return inner


@pytest.fixture(scope="session", params=(HTML_LOAD_PATHS,
                                         PNG_LOAD_PATHS,
                                         CSS_LOAD_PATHS))
def fake_urls(request):
    return FakeRequestData(request.param)


@pytest.fixture()
def temp_directory():
    return tempfile.TemporaryDirectory()


@pytest.fixture(scope="session")
def wrong_domain_subadress():
    result = {
        'html': """<html>
    <head>
        <link href="/courses" rel="canonical">
    </head>
</html>""",
        'url': 'http://www.post.com',
        'url_file': 'http://www.post.com/courses',
        'directory': 'www-post-com_files',
        'main-file': 'www-post-com.html',
        'file': 'www-post-com-course.html',
        'response_code': 404}
    return result


@pytest.fixture(scope="session", params=NAMES)
def name_matching(request):
    return request.param
