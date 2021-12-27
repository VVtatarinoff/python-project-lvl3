import requests
import pytest
import os
from page_loader.loader import download


def test_no_directory(fake_urls, temp_directory, requests_mock):
    wrong_dir = os.path.join(temp_directory.name, '/test')
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    with pytest.raises(FileNotFoundError) as e:
        download(fake_urls.url, wrong_dir)
    assert e.match(wrong_dir)


def test_no_permission(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    os.chmod(temp_directory.name, 444)
    with pytest.raises(PermissionError) as e:
        download(fake_urls.url, temp_directory.name)
    assert e.match(temp_directory.name)


def test_no_connection(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url,
                      exc=requests.exceptions.ConnectionError)
    with pytest.raises(requests.exceptions.ConnectionError) as e:
        download(fake_urls.url, temp_directory.name)
    assert e.match(fake_urls.url)


@pytest.mark.parametrize('code', [404, 500])
def test_loader_status_wrong(fake_urls, temp_directory, requests_mock, code):
    url_dictionary = fake_urls.mock_page_data
    url_dictionary['status_code'] = code
    requests_mock.get(fake_urls.url, **url_dictionary)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    with pytest.raises(requests.exceptions.HTTPError) as e:
        download(fake_urls.url, temp_directory.name)
    assert e.match('status-code ' + str(code))
