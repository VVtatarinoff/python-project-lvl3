import os
import requests

from bs4 import BeautifulSoup
from page_loader.uploader import save_from_web


def test_uploader_wrong_adress(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url, exc=requests.exceptions.ConnectionError)
    file_name = save_from_web(fake_urls.url, temp_directory.name)
    assert not file_name


def test_uploader(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    file_name = save_from_web(fake_urls.url, temp_directory.name)
    with open(os.path.join(temp_directory.name, file_name)) as file:
        text = file.read()
    created_html = BeautifulSoup(text, "html.parser").prettify()
    required_html = BeautifulSoup(fake_urls.initial_html,
                                  "html.parser").prettify()
    assert created_html == required_html
