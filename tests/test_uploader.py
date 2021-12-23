import requests_mock
import os
import pytest
from bs4 import BeautifulSoup
from page_loader.uploader import Uploader


def test_uploader_wrong_adress(fake_urls, temp_directory):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            fake_urls.mock_adresses(m.get)()
            test_load = Uploader(fake_urls.url[:-3], temp_directory.name)
            test_load.save_from_web()
        assert 'MyError' in str(excinfo)


def test_uploader_wrong_path(fake_urls):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            fake_urls.mock_adresses(m.get)()
            test_wrong = Uploader(fake_urls.url, '/asdadaasd')
            test_wrong.save_from_web()
        assert 'MyError' in str(excinfo)


def test_uploader(fake_urls, temp_directory):
    with requests_mock.Mocker() as m:
        fake_urls.mock_adresses(m.get)()
        test_load = Uploader(fake_urls.url, temp_directory.name)
        test_load.save_from_web()
        file_name = fake_urls.path_to_saved_page
        with open(os.path.join(temp_directory.name, file_name)) as file:
            text = file.read()
        created_html = BeautifulSoup(text, "html.parser").prettify()
        required_html = BeautifulSoup(fake_urls.initial_html,
                                      "html.parser").prettify()
        assert created_html == required_html
