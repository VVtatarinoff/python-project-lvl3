import requests
import os
from bs4 import BeautifulSoup
from page_loader.uploader import Uploader


def test_uploader_wrong_adress(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url, exc=requests.exceptions.ConnectionError)
    test_load = Uploader(fake_urls.url, temp_directory.name)
    assert not test_load.load_content()


def test_uploader(fake_urls, temp_directory, requests_mock):
    fake_urls.mock_adresses(requests_mock.get)()
    test_load = Uploader(fake_urls.url, temp_directory.name)
    test_load.save_from_web()
    file_name = fake_urls.path_to_saved_page
    with open(os.path.join(temp_directory.name, file_name)) as file:
        text = file.read()
    created_html = BeautifulSoup(text, "html.parser").prettify()
    required_html = BeautifulSoup(fake_urls.initial_html,
                                  "html.parser").prettify()
    assert created_html == required_html
