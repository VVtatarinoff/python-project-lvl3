import requests
import pytest
import os
from page_loader.loader import download
from page_loader.errors import NoPermission, NoDirectory
from page_loader.errors import NoConnection, WrongStatusCode


@pytest.mark.xfail(raises=NoDirectory, strict=True)
def test_no_directory(fake_urls, temp_directory):
    wrong_dir = os.path.join(temp_directory.name, '/test')
    download(fake_urls.url, wrong_dir)


@pytest.mark.xfail(raises=NoPermission, strict=True)
def test_no_permission(fake_urls, temp_directory, requests_mock):
    os.chmod(temp_directory.name, 444)
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    download(fake_urls.url, temp_directory.name)


@pytest.mark.xfail(raises=NoConnection, strict=True)
def test_no_connection(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url,
                      exc=requests.exceptions.ConnectionError)
    download(fake_urls.url, temp_directory.name)


@pytest.mark.parametrize('code', [404, 500])
@pytest.mark.xfail(raises=WrongStatusCode, strict=True)
def test_loader_status_wrong(fake_urls, temp_directory, requests_mock, code):
    url_dictionary = fake_urls.mock_page_data
    url_dictionary['status_code'] = code
    requests_mock.get(fake_urls.url, **url_dictionary)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    download(fake_urls.url, temp_directory.name)
