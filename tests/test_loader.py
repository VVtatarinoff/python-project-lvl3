import requests_mock
import os
from page_loader.loader import download
import tempfile


def test_loader(get_html):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get('https://test.com', text=get_html)
            download('https://test.com', temp_dir)
            file_name = 'test-com.html'
            with open(os.path.join(temp_dir, file_name)) as file:
                created_html = file.read()
            assert created_html == get_html
