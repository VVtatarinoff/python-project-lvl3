import requests_mock
import os
from page_loader.loader import copy_html_to_path
import tempfile
from bs4 import BeautifulSoup


def test_loader(get_html):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get('https://test.com', headers={'content-type': ' html'},
                  text=get_html)
            copy_html_to_path('https://test.com', temp_dir)
            file_name = 'test-com.html'
            print(os.path.exists(temp_dir))
            with open(os.path.join(temp_dir, file_name)) as file:
                text = file.read()
                created_html = BeautifulSoup(text, "html.parser").prettify()
            required_html = BeautifulSoup(get_html, "html.parser").prettify()
            assert created_html == required_html
