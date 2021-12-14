import os
import pytest
from tests.fixtures.test_data import HTML_LOAD_PATHS
from tests.fixtures.test_data import PNG_LOAD_PATHS
from tests.fixtures.test_data import CSS_LOAD_PATHS


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ATTR_TO_LOAD = {'initial_html', 'result', 'file_directory'}


def get_fixture_path(file_name):
    return os.path.join(CURRENT_DIR, 'fixtures', file_name)


@pytest.fixture(scope="session", params=(HTML_LOAD_PATHS,
                                         PNG_LOAD_PATHS,
                                         CSS_LOAD_PATHS))
def html_check(request):
    data = dict()
    data['text'] = ""
    data['content'] = None
    for attr in request.param:
        if attr in ATTR_TO_LOAD:
            full_path = get_fixture_path(request.param[attr])
            if attr == 'file_directory':
                mode = request.param['read_mode']
                attr_name = 'content' if mode == "rb" else 'text'
                with open(full_path, mode) as file:
                    data[attr_name] = file.read()
            else:
                with open(full_path) as file:
                    data[attr] = file.read()
        else:
            data[attr] = request.param[attr]
    return data


@pytest.fixture(scope="session")
def wrong_html_domin_subadress():
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
        'response_code': '404'}
    return result
