import sys

import pytest

from page_loader.scripts.upload_page import main


def test_main_normal(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    sys.argv = ['page-loader', '-o', temp_directory.name, fake_urls.url]
    with pytest.raises(SystemExit) as s:
        main()
    assert s.value.code == 0


def test_main_wrong_dir(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    with pytest.raises(SystemExit) as s:
        sys.argv = ['page-loader', '-o', temp_directory.name + 'ff',
                    fake_urls.url]
        main()
    assert s.value.code == 1


def test_main_wrong_url(fake_urls, temp_directory, requests_mock):
    requests_mock.get(fake_urls.url + 'test',
                      **fake_urls.mock_page_data)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    with pytest.raises(SystemExit) as s:
        sys.argv = ['page-loader', '-o', temp_directory.name, fake_urls.url]
        main()
    assert s.value.code == 1
