import requests_mock
import requests
import pytest
import os
import sys
from page_loader.loader import download
import tempfile
from bs4 import BeautifulSoup


def test_loader(fake_urls):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            # ссылка на исходную страницу
            fake_urls.mock_adresses(m.get)()
            download(fake_urls.url, temp_dir)
            # проверка основго файла
            file_name = fake_urls.path_to_saved_page
            with open(os.path.join(temp_dir, file_name)) as file:
                text = file.read()
            created_html = BeautifulSoup(text, "html.parser").prettify()
            required_html = BeautifulSoup(fake_urls.modified_html,
                                          "html.parser").prettify()
            assert created_html == required_html
            # проверка файла в *_files директории
            file_name = fake_urls.path_to_saved_file
            with open(os.path.join(temp_dir, file_name),
                      fake_urls.mode) as file:
                assert fake_urls.content == file.read()


def test_loader_wrong(wrong_html_domain_subadress):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get(wrong_html_domain_subadress['url'],
                  headers={'content-type': 'text/html'},
                  text=wrong_html_domain_subadress['html'])
            m.get(wrong_html_domain_subadress['url_file'],
                  status_code=wrong_html_domain_subadress['response_code'])
            download(wrong_html_domain_subadress['url'], temp_dir)
            directory = os.path.join(temp_dir,
                                     wrong_html_domain_subadress['directory'])
            assert os.path.exists(directory)
            assert len(os.listdir(directory)) == 0
            file = os.path.join(directory, wrong_html_domain_subadress['file'])
            assert not os.path.exists(os.path.join(directory, file))


def test_no_directory(fake_urls):
    with tempfile.TemporaryDirectory() as temp_dir:
        wrong_dir = os.path.join(temp_dir, '/test')
        with pytest.raises(Exception) as excinfo:
            with requests_mock.Mocker() as m:
                # ссылка на исходную страницу
                fake_urls.mock_adresses(m.get)()
                download(fake_urls.url, wrong_dir)
        print(sys.exc_info())
        assert 'NoDirectory' in str(excinfo)


def test_no_page(fake_urls):
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(Exception) as excinfo:
            with requests_mock.Mocker() as m:
                m.get(fake_urls.url, exc=requests.exceptions.ConnectionError)
                download(fake_urls.url, temp_dir)
        print(sys.exc_info())
        assert 'NoConnection' in str(excinfo)
