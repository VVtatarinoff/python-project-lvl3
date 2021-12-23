import requests_mock
import os
import pytest
import tempfile
from bs4 import BeautifulSoup
from page_loader.uploader import Uploader


def test_uploader_wrong_adress(fake_urls):
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(Exception) as excinfo:
            with requests_mock.Mocker() as m:
                fake_urls.mock_adresses(m.get)()
                test_load = Uploader(fake_urls.url[:-3], temp_dir)
                test_load.save_from_web()
            assert 'MyError' in str(excinfo)


def test_uploader_wrong_path(fake_urls):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            fake_urls.mock_adresses(m.get)()
            test_wrong = Uploader(fake_urls.url, '/asdadaasd')
            test_wrong.save_from_web()
        assert 'MyError' in str(excinfo)


def test_uploader(fake_urls):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            fake_urls.mock_adresses(m.get)()
            test_load = Uploader(fake_urls.url, temp_dir)
            test_load.save_from_web()
            file_name = fake_urls.path_to_saved_page
            with open(os.path.join(temp_dir, file_name)) as file:
                text = file.read()
            created_html = BeautifulSoup(text, "html.parser").prettify()
            required_html = BeautifulSoup(fake_urls.initital_html,
                                          "html.parser").prettify()
            assert created_html == required_html
