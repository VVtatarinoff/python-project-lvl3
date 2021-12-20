import os
import pytest
from tests.fixtures.test_data import HTML_LOAD_PATHS
from tests.fixtures.test_data import PNG_LOAD_PATHS
from tests.fixtures.test_data import CSS_LOAD_PATHS
from tests.fixtures.naming_data import NAMES


class FakeRequest(object):
    def __init__(self, data_paths):
        self.mode = data_paths['read_mode']
        self.content = self.get_data(data_paths['file_directory'], self.mode)
        self.initital_html = self.get_data(data_paths['initial_html'])
        self.modified_html = self.get_data(data_paths['result'])
        self.url = data_paths['url']
        self.url_file = data_paths['url_file']
        self.path_to_saved_file = data_paths['path_to_file']
        self.path_to_saved_page = data_paths['name_result_file']
        self.file_type = data_paths['content-type']

    def get_fixture_path(self, file_name):
        current = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current, 'fixtures', file_name)

    def get_data(self, path, mode="r"):
        path = self.get_fixture_path(path)
        with open(path, mode) as file:
            data = file.read()
        return data

    def mock_adresses(self, func):
        def inner():
            func(self.url, headers={'content-type': 'text/html; charset=utf-8',
                                    'content-length': '100'},
                 text=self.initital_html)
            if self.mode == 'r':
                func(self.url_file, headers={'content-type': self.file_type,
                                             'content-length': '100'},
                     text=self.content)
            else:
                func(self.url_file, headers={'content-type': self.file_type,
                                             'content-length': '100'},
                     content=self.content)
        return inner


@pytest.fixture(scope="session", params=(HTML_LOAD_PATHS,
                                         PNG_LOAD_PATHS,
                                         CSS_LOAD_PATHS))
def fake_urls(request):
    return FakeRequest(request.param)


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
