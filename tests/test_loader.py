import requests_mock
import requests
import pytest
import os
from page_loader.loader import download
from bs4 import BeautifulSoup


def test_loader(fake_urls, temp_directory, requests_mock):
    # ссылка на исходную страницу
    fake_urls.mock_adresses(requests_mock.get)()
    download(fake_urls.url, temp_directory.name)
    # проверка основго файла
    file_name = fake_urls.path_to_saved_page
    with open(os.path.join(temp_directory.name, file_name)) as file:
        text = file.read()
    created_html = BeautifulSoup(text, "html.parser").prettify()
    required_html = BeautifulSoup(fake_urls.modified_html,
                                  "html.parser").prettify()
    assert created_html == required_html
    # проверка файла в *_files директории
    file_name = fake_urls.path_to_saved_file
    with open(os.path.join(temp_directory.name, file_name),
              fake_urls.read_mode) as file:
        assert fake_urls.file_content == file.read()


def test_loader_wrong(wrong_domain_subadress, temp_directory):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            m.get(wrong_domain_subadress['url'],
                  headers={'content-type': 'text/html',
                           'content-length': '100'},
                  text=wrong_domain_subadress['html'])
            m.get(wrong_domain_subadress['url_file'],
                  status_code=wrong_domain_subadress['response_code'])
            download(wrong_domain_subadress['url'], temp_directory.name)
            directory = os.path.join(temp_directory.name,
                                     wrong_domain_subadress['directory'])
            assert os.path.exists(directory)
            assert len(os.listdir(directory)) == 0
            file = os.path.join(directory, wrong_domain_subadress['file'])
            assert not os.path.exists(os.path.join(directory, file))
        assert 'MyError' in str(excinfo)


def test_no_directory(fake_urls, temp_directory):
    wrong_dir = os.path.join(temp_directory.name, '/test')
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            # ссылка на исходную страницу
            fake_urls.mock_adresses(m.get)()
            download(fake_urls.url, wrong_dir)
    assert 'MyError' in str(excinfo)


def test_no_page(fake_urls, temp_directory):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            m.get(fake_urls.url, exc=requests.exceptions.ConnectionError)
            download(fake_urls.url, temp_directory.name)
    assert 'MyError' in str(excinfo)
